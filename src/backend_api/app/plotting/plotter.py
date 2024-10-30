import pandas as pd
from pydantic import TypeAdapter
from sqlalchemy import Boolean, Result, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import CompoundSelect, Select

from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.schemas.plot import BaseSpecs, ItemSpecs, PlotData, PlotQuery
from app.exceptions.model_exceptions.plot_exception import (
    PlotNoModifiersProvidedError,
    PlotQueryDataNotFoundError,
)
from app.plotting.utils import find_conversion_value, summarize_function
from app.utils.timing_tracker import async_timing_tracker, sync_timing_tracker


class Plotter:
    def __init__(self):
        self.validate = TypeAdapter(PlotData).validate_python

    def _create_wanted_modifier_subquery(self, query: PlotQuery):
        if len(query.wantedModifiers) == 0:
            raise PlotNoModifiersProvidedError(
                query_data=query,
                function_name=self._init_query.__name__,
                class_name=self.__class__.__name__,
            )

        subquery_stmt = select(model_ItemModifier.itemId.label("itemModifierItemId"))

        wanted_modifier_conditions = []
        for wanted_modifier in query.wantedModifiers:
            modifier_id = wanted_modifier.modifierId
            modifier_limitation = wanted_modifier.modifierLimitations

            limitations = []
            if modifier_limitation is not None:
                # Adds limitations if they exist
                if wanted_modifier.modifierLimitations.minRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        >= wanted_modifier.modifierLimitations.minRoll
                    )
                if wanted_modifier.modifierLimitations.maxRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        <= wanted_modifier.modifierLimitations.maxRoll
                    )
                if wanted_modifier.modifierLimitations.textRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        == (wanted_modifier.modifierLimitations.textRoll)
                    )
            intersect_wanted_modifier_statement = subquery_stmt.where(
                model_ItemModifier.modifierId == modifier_id, *limitations
            )
            wanted_modifier_conditions.append(intersect_wanted_modifier_statement)

        subquery_stmt = subquery_stmt.intersect(*wanted_modifier_conditions)

        return subquery_stmt

    def _init_query(self, query: PlotQuery, *, subquery: CompoundSelect) -> Select:
        league = query.league

        statement = (
            select(
                model_Item.itemId,
                model_Item.createdAt,
                model_Item.baseType,
                model_Item.currencyId,
                model_Item.currencyAmount,
                model_Currency.tradeName,
                model_Currency.valueInChaos,
                model_Currency.createdAt.label("currencyCreatedAt"),
            )
            .join_from(model_Currency, model_Item)
            .where(and_(model_Item.itemId.in_(subquery), model_Item.league == league))
        )

        return statement

    def _apply_base_specs(
        self, statement: Select, *, base_spec_query: BaseSpecs
    ) -> Select:
        base_spec_conditions = []
        if base_spec_query.baseType is not None:
            # Using baseType without joining saves performance
            base_spec_conditions.append(model_Item.baseType == base_spec_query.baseType)
        if (
            base_spec_query.category is not None
            or base_spec_query.subCategory is not None
        ):
            statement = statement.join(model_ItemBaseType)
            if base_spec_query.category is not None:
                base_spec_conditions.append(
                    model_ItemBaseType.category == base_spec_query.category
                )

            if base_spec_query.subCategory is not None:
                base_spec_conditions.append(
                    model_ItemBaseType.subCategory == base_spec_query.subCategory
                )

        return statement.where(and_(*base_spec_conditions))

    def _apply_item_specs(
        self, statement: Select, *, item_spec_query: ItemSpecs
    ) -> Select:
        item_spec_query_fields = item_spec_query.model_fields.copy()
        item_specifications = []

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

        if not any(item_specifications):
            item_specifications += [
                model_Item.__dict__[key] == item_spec_query.__dict__[key]
                for key in item_spec_query_fields
                if (item_spec_query.__dict__[key] is not None)
            ]

        return statement.where(and_(*item_specifications))

    def _filter_from_query(self, statement: Select, *, query: PlotQuery) -> Select:
        """
        Prioritizes filtering the largest amount of rows
        """
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
        subquery_stmt = self._create_wanted_modifier_subquery(query)
        statement = self._init_query(query, subquery=subquery_stmt)
        statement = self._filter_from_query(statement, query=query)
        async with db.begin():
            result = await db.execute(statement)

        return result

    @sync_timing_tracker
    def _convert_result_to_df(self, result: Result) -> pd.DataFrame:
        rows = result.mappings().all()
        return pd.DataFrame(rows)

    @sync_timing_tracker
    def _create_plot_data(self, df: pd.DataFrame) -> tuple:
        # Sort values by date
        df.sort_values(by="createdAt", inplace=True)

        # Find most common currency
        most_common_currency_used = df.tradeName.mode()[0]

        # Find value in chaos
        value_in_chaos = df["currencyAmount"] * df["valueInChaos"]

        # Get timestamps of when the items were retrieved
        time_stamps = df["createdAt"]

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
        grouped_by_date_df = df.groupby(pd.Grouper(key="timeStamp", axis=0, freq="h"))

        # Aggregate by custom function
        agg_by_date_df = grouped_by_date_df.agg(
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
