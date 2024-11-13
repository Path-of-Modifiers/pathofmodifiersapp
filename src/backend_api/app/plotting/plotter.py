import pandas as pd
from pydantic import TypeAdapter
from sqlalchemy import (
    BinaryExpression,
    Boolean,
    ColumnElement,
    Result,
    and_,
    or_,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.schemas.plot import (
    BaseSpecs,
    ItemSpecs,
    ModifierLimitations,
    PlotData,
    PlotQuery,
    WantedModifier,
)
from app.exceptions.model_exceptions.plot_exception import (
    PlotNoModifiersProvidedError,
    PlotQueryDataNotFoundError,
)
from app.plotting.utils import find_conversion_value, summarize_function
from app.utils.timing_tracker import async_timing_tracker, sync_timing_tracker
from app.logs.logger import plot_logger


class Plotter:
    def __init__(self):
        self.validate = TypeAdapter(PlotData).validate_python

    def _init_stmt(
        self, query: PlotQuery, *, before: int | None, after: int | None
    ) -> Select:
        if len(query.wantedModifiers) == 0:
            raise PlotNoModifiersProvidedError(
                query_data=query,
                function_name=self._init_stmt.__name__,
                class_name=self.__class__.__name__,
            )

        league = query.league

        statement = (
            select(
                model_Item.itemId,
                model_Item.createdHoursSinceLaunch,
                model_Item.itemBaseTypeId,
                model_Item.currencyId,
                model_Item.currencyAmount,
                model_Currency.tradeName,
                model_Currency.valueInChaos,
                model_Currency.createdHoursSinceLaunch.label(
                    "currencyCreatedHoursSinceLaunch"
                ),
            )
            .join_from(model_Currency, model_Item)
            .where(model_Item.league == league)
        )

        if before is not None:
            statement = statement.where(
                model_ItemModifier.createdHoursSinceLaunch <= before
            )
        if after is not None:
            statement = statement.where(
                model_ItemModifier.createdHoursSinceLaunch >= after
            )

        return statement

    def _check_rolls(
        self, modifier_limitations: ModifierLimitations
    ) -> ColumnElement[bool] | BinaryExpression[bool]:
        if modifier_limitations.textRoll is not None:
            return model_ItemModifier.roll == modifier_limitations.textRoll
        else:
            and_conditions = []
            if modifier_limitations.minRoll is not None:
                and_conditions.append(
                    model_ItemModifier.roll >= modifier_limitations.minRoll
                )
            if modifier_limitations.maxRoll is not None:
                and_conditions.append(
                    model_ItemModifier.roll <= modifier_limitations.maxRoll
                )
            return and_(*and_conditions)

    def _add_wanted_modifiers(
        self,
        statement: Select,
        *,
        wanted_modifier_query: list[list[WantedModifier]],
        before: int | None,
        after: int | None,
    ) -> Select:
        """
        Uses as few modifier ids as possible to filter. One modifier effect has multiple
        modifier ids assosiated with it. Here, the ones with a roll limitation from the user
        are prioritized. If none are found (modifier_roll_limitation_found=False), a random
        one is chosen.
        """
        exists_conditions = []
        for grouped_wanted_modifier in wanted_modifier_query:
            modifier_roll_limitation_found = False
            for wanted_modifier in grouped_wanted_modifier:
                if wanted_modifier.modifierLimitations is not None:
                    modifier_roll_limitation_found = True
                    roll_condition = self._check_rolls(
                        wanted_modifier.modifierLimitations
                    )
                    and_conditions = [
                        model_Item.itemId == model_ItemModifier.itemId,
                        model_ItemModifier.modifierId == wanted_modifier.modifierId,
                        roll_condition,
                    ]
                    if before is not None:
                        and_conditions.append(
                            model_ItemModifier.createdHoursSinceLaunch <= before
                        )
                    if after is not None:
                        and_conditions.append(
                            model_ItemModifier.createdHoursSinceLaunch >= after
                        )

                    exists_conditions.append(
                        select(1)
                        .where(
                            and_(
                                *and_conditions,
                            )
                        )
                        .exists()
                    )

            if not modifier_roll_limitation_found:
                and_conditions = [
                    model_Item.itemId == model_ItemModifier.itemId,
                    model_ItemModifier.modifierId == wanted_modifier.modifierId,
                ]
                if before is not None:
                    and_conditions.append(
                        model_ItemModifier.createdHoursSinceLaunch <= before
                    )
                if after is not None:
                    and_conditions.append(
                        model_ItemModifier.createdHoursSinceLaunch >= after
                    )
                exists_conditions.append(
                    select(1).where(and_(*and_conditions)).exists()
                )

        return statement.where(and_(*exists_conditions))

    def _apply_priority_filters(
        self,
        statement: Select,
        *,
        query: PlotQuery,
        before: int | None,
        after: int | None,
    ) -> Select:
        statement = self._add_wanted_modifiers(
            statement,
            wanted_modifier_query=query.wantedModifiers,
            before=before,
            after=after,
        )
        if query.itemSpecifications is not None:
            if query.itemSpecifications.name is not None:
                if "|" in query.itemSpecifications.name:
                    name_filter = or_(
                        *[
                            model_Item.name == name
                            for name in query.itemSpecifications.name.split("|")
                        ]
                    )
                else:
                    name_filter = model_Item.name == query.itemSpecifications.name
                statement = statement.where(name_filter)

        return statement

    def _apply_base_specs(
        self, statement: Select, *, base_spec_query: BaseSpecs
    ) -> Select:
        if base_spec_query.itemBaseTypeId is not None:
            return statement.where(
                model_Item.itemBaseTypeId == base_spec_query.itemBaseTypeId
            )

        elif (
            base_spec_query.category is not None
            or base_spec_query.subCategory is not None
        ):
            subquery = select(model_ItemBaseType.itemBaseTypeId)
            base_spec_conditions = []
            if base_spec_query.category is not None:
                base_spec_conditions.append(
                    model_ItemBaseType.category == base_spec_query.category
                )

            if base_spec_query.subCategory is not None:
                base_spec_conditions.append(
                    model_ItemBaseType.subCategory == base_spec_query.subCategory
                )
            subquery = subquery.where(and_(*base_spec_conditions))

            return statement.where(model_Item.itemBaseTypeId.in_(subquery))

        else:
            return statement

    def _apply_item_specs(
        self, statement: Select, *, item_spec_query: ItemSpecs
    ) -> Select:
        item_spec_query_fields = item_spec_query.model_fields.copy()
        item_specifications = []

        if item_spec_query.name is not None:
            # name has already been applied
            item_spec_query_fields.pop("name")

        if item_spec_query.minIlvl is not None:
            item_specifications.append(model_Item.ilvl >= item_spec_query.minIlvl)
            item_spec_query_fields.pop("minIlvl")

        if item_spec_query.maxIlvl is not None:
            item_specifications.append(model_Item.ilvl <= item_spec_query.maxIlvl)
            item_spec_query_fields.pop("maxIlvl")

        if item_spec_query.influences is not None:
            item_specifications += [
                model_Item.influences[key].cast(Boolean)
                == item_spec_query.influences.__dict__[key]
                for key in item_spec_query.influences.model_fields
                if (item_spec_query.influences.__dict__[key] is not None)
            ]
            item_spec_query_fields.pop("influences")

        item_specifications += [
            model_Item.__dict__[key] == item_spec_query.__dict__[key]
            for key in item_spec_query_fields
            if (item_spec_query.__dict__[key] is not None)
        ]

        return statement.where(and_(*item_specifications))

    def _filter_from_query(
        self,
        statement: Select,
        *,
        query: PlotQuery,
        before: int | None,
        after: int | None,
    ) -> Select:
        """
        Prioritizes filtering the largest amount of rows
        """
        statement = self._apply_priority_filters(
            statement, query=query, before=before, after=after
        )
        if query.baseSpecifications is not None:
            statement = self._apply_base_specs(
                statement, base_spec_query=query.baseSpecifications
            )

        if query.itemSpecifications is not None:
            statement = self._apply_item_specs(
                statement, item_spec_query=query.itemSpecifications
            )

        return statement

    @async_timing_tracker
    async def _perform_plot_db_query(
        self, db: AsyncSession, *, query: PlotQuery
    ) -> Result:
        before, after = query.before, query.after
        statement = self._init_stmt(query, before=before, after=after)
        statement = self._filter_from_query(
            statement, query=query, before=before, after=after
        )

        async with db.begin():
            result = await db.execute(statement)

        return result

    @sync_timing_tracker
    def _convert_result_to_df(self, result: Result) -> pd.DataFrame:
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=result.keys())
        return df

    @sync_timing_tracker
    def _create_plot_data(self, df: pd.DataFrame) -> tuple:
        # Sort values by date
        df.sort_values(by="createdHoursSinceLaunch", inplace=True)

        # Find most common currency
        most_common_currency_used = df.tradeName.mode()[0]

        # Find value in chaos
        value_in_chaos = df["currencyAmount"] * df["valueInChaos"]

        # Get timestamps of when the items were retrieved
        time_stamps = df["createdHoursSinceLaunch"]

        # Find conversion value between chaos and most common currency
        conversion_value = find_conversion_value(
            df,
            value_in_chaos=value_in_chaos,
            most_common_currency_used=most_common_currency_used,
        )
        value_in_most_common_currency_used = value_in_chaos / conversion_value

        return (
            value_in_chaos,
            time_stamps,
            value_in_most_common_currency_used,
            most_common_currency_used,
        )

    @sync_timing_tracker
    def _summarize_plot_data(
        self,
        value_in_chaos: pd.Series,
        time_stamps: pd.Series,
        value_in_most_common_currency_used: pd.Series,
        mostCommonCurrencyUsed: str,
    ) -> dict[str, pd.Series | str]:
        # Convert to dict
        plot_data = {
            "valueInChaos": value_in_chaos,
            "timeStamp": time_stamps,
            "valueInMostCommonCurrencyUsed": value_in_most_common_currency_used,
            "mostCommonCurrencyUsed": mostCommonCurrencyUsed,
        }
        # Then as a dataframe
        df = pd.DataFrame(plot_data)

        # Group by hour
        grouped_by_created_hours_since_launch_df = df.groupby("timeStamp")

        # Aggregate by custom function
        agg_by_date_df = grouped_by_created_hours_since_launch_df.agg(
            {
                "valueInChaos": lambda values: summarize_function(values, 2),
                "valueInMostCommonCurrencyUsed": lambda values: summarize_function(
                    values, 2
                ),
            }
        )
        agg_by_date_df = agg_by_date_df.loc[~agg_by_date_df["valueInChaos"].isna()]

        # Update the values in the dict
        plot_data["timeStamp"] = agg_by_date_df.index
        plot_data["valueInChaos"] = agg_by_date_df["valueInChaos"].values
        plot_data["valueInMostCommonCurrencyUsed"] = agg_by_date_df[
            "valueInMostCommonCurrencyUsed"
        ].values

        return plot_data

    @async_timing_tracker
    async def plot(self, db: AsyncSession, *, query: PlotQuery) -> PlotData:
        plot_logger.info(f"plot_query_executed={query}")
        result = await self._perform_plot_db_query(db, query=query)
        df = self._convert_result_to_df(result)

        if df.empty:
            raise PlotQueryDataNotFoundError(
                query_data=query,
                function_name=self.plot.__name__,
                class_name=self.__class__.__name__,
            )
        else:
            (
                value_in_chaos,
                time_stamps,
                value_in_most_common_currency_used,
                mostCommonCurrencyUsed,
            ) = self._create_plot_data(df)

        plot_data = self._summarize_plot_data(
            value_in_chaos,
            time_stamps,
            value_in_most_common_currency_used,
            mostCommonCurrencyUsed,
        )

        return self.validate(plot_data)
