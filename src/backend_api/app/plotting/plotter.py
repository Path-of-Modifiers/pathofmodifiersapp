import pandas as pd
from pydantic import TypeAdapter
from sqlalchemy import BinaryExpression, ColumnElement, Result, and_, or_, select, text
from sqlalchemy.dialects import postgresql
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
from app.logs.logger import plot_logger
from app.utils.timing_tracker import async_timing_tracker, sync_timing_tracker


class Plotter:
    def __init__(self):
        self.validate = TypeAdapter(PlotData).validate_python

    def _init_stmt(
        self, query: PlotQuery, *, start: int | None, end: int | None
    ) -> Select:
        if len(query.wantedModifiers) == 0:
            raise PlotNoModifiersProvidedError(
                query_data=query,
                function_name=self._init_stmt.__name__,
                class_name=self.__class__.__name__,
            )

        statement = select(
            model_Item.itemId,
            model_Item.createdHoursSinceLaunch,
            model_Item.league,
            model_Item.itemBaseTypeId,
            model_Item.currencyId,
            model_Item.currencyAmount,
            model_Currency.tradeName,
            model_Currency.valueInChaos,
            model_Currency.createdHoursSinceLaunch.label(
                "currencyCreatedHoursSinceLaunch"
            ),
        ).join_from(model_Item, model_Currency)

        if "|" in query.league:
            statement.where(
                or_([model_Item.league == league for league in query.league.split("|")])
            )
        else:
            statement.where(model_Item.league == query.league)

        if start is not None:
            statement = statement.where(model_Item.createdHoursSinceLaunch >= start)
        if end is not None:
            statement = statement.where(model_Item.createdHoursSinceLaunch <= end)

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
        start: int | None,
        end: int | None,
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
                    if start is not None:
                        and_conditions.append(
                            model_ItemModifier.createdHoursSinceLaunch >= start
                        )

                    if end is not None:
                        and_conditions.append(
                            model_ItemModifier.createdHoursSinceLaunch <= end
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
                if start is not None:
                    and_conditions.append(
                        model_ItemModifier.createdHoursSinceLaunch >= start
                    )
                if end is not None:
                    and_conditions.append(
                        model_ItemModifier.createdHoursSinceLaunch <= end
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
        start: int | None,
        end: int | None,
    ) -> Select:
        statement = self._add_wanted_modifiers(
            statement,
            wanted_modifier_query=query.wantedModifiers,
            start=start,
            end=end,
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
            # item_specifications += [
            #     (
            #         model_Item.influences[key].isnot(None).cast(Boolean)
            #         if model_Item.influences[key].is_not(None)
            #         else model_Item.influences[key]
            #         == item_spec_query.influences.__dict__[key]
            #     )
            #     for key in item_spec_query.influences.model_fields
            #     if item_spec_query.influences.__dict__[key] is not None
            # ]
            # TODO: Fix influences query and uncomment above
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
        start: int | None,
        end: int | None,
    ) -> Select:
        """
        Prioritizes filtering the largest amount of rows
        """
        statement = self._apply_priority_filters(
            statement, query=query, start=start, end=end
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
        start, end = query.start, query.end
        statement = self._init_stmt(query, start=start, end=end)
        statement = self._filter_from_query(
            statement, query=query, start=start, end=end
        )
        print(
            statement.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
            ).string
        )
        full_statement = text(
            f"""
            WITH baseQuery AS (
                {statement.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
            ).string}
            ), mostCommon AS (
                SELECT baseQuery."tradeName" AS "mostCommonTradeName", COUNT(baseQuery."tradeName") AS "nameCount"
                FROM baseQuery
                GROUP BY baseQuery.league, baseQuery."tradeName"
                ORDER BY "nameCount" DESC
                LIMIT 1
            ), mostCommonIds AS (
                SELECT baseQuery."createdHoursSinceLaunch", MAX(baseQuery."currencyId") AS "mostCommonCurrencyId"
                FROM baseQuery
                WHERE baseQuery."tradeName" = (SELECT "mostCommonTradeName" FROM mostCommon)
                GROUP BY baseQuery."createdHoursSinceLaunch"
            ), mostCommonPrices AS (
                SELECT baseQuery."createdHoursSinceLaunch", MIN(baseQuery."valueInChaos") AS "mostCommonValueInChaos", MIN(baseQuery."tradeName") AS "mostCommonCurrencyUsed"
                FROM baseQuery NATURAL JOIN mostCommonIds
                WHERE baseQuery."currencyId" = mostCommonIds."mostCommonCurrencyId"
                GROUP BY baseQuery."createdHoursSinceLaunch"
            ), prices AS (
                SELECT baseQuery."createdHoursSinceLaunch", baseQuery.league, baseQuery."currencyAmount"*baseQuery."valueInChaos" AS "valueInChaos", baseQuery."currencyAmount"*baseQuery."valueInChaos" / mostCommonPrices."mostCommonValueInChaos" AS "valueInMostCommonCurrencyUsed", mostCommonPrices."mostCommonCurrencyUsed"
                FROM baseQuery JOIN mostCommonPrices ON baseQuery."createdHoursSinceLaunch" = mostCommonPrices."createdHoursSinceLaunch"
            ), rankedPrices AS (
                SELECT prices.*,
                    RANK() OVER
                        (PARTITION BY prices."createdHoursSinceLaunch" ORDER BY prices."valueInChaos" ASC) AS pos
                FROM prices
            ), filteredPrices AS (
            SELECT r."createdHoursSinceLaunch", r.league, r."valueInChaos", r."valueInMostCommonCurrencyUsed", r."mostCommonCurrencyUsed",
                    CASE
                        WHEN r.pos < 10 THEN 'low'
                        WHEN r.pos < 15 THEN 'medium'
                        ELSE 'high'
                    END as confidence
                FROM rankedPrices r
                WHERE r.pos <=20
                ORDER BY r."createdHoursSinceLaunch", r."valueInChaos"
            )

            SELECT filteredPrices."createdHoursSinceLaunch" AS "hoursSinceLaunch", filteredPrices.league, AVG(filteredPrices."valueInChaos") AS "valueInChaos", AVG(filteredPrices."valueInMostCommonCurrencyUsed") AS "valueInMostCommonCurrencyUsed", MIN(filteredPrices."mostCommonCurrencyUsed") AS "mostCommonCurrencyUsed", MIN(filteredPrices.confidence) AS confidence
            FROM filteredPrices
            GROUP BY filteredPrices."createdHoursSinceLaunch", filteredPrices.league
            """
        )

        async with db.begin():
            result = await db.execute(full_statement)

        return result

    @sync_timing_tracker
    def _convert_result_to_df(self, result: Result) -> pd.DataFrame:
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=result.keys())
        return df

    @sync_timing_tracker
    def _create_plot_data(self, df: pd.DataFrame) -> dict[str, list[dict] | str]:
        mostCommonCurrencyUsed: str = df["mostCommonCurrencyUsed"].get(0)
        data = []
        for league in df["league"].unique():
            league_df: pd.DataFrame = df.loc[df["league"] == league]
            timeseries_data = {
                "name": league,
                "confidenceRating": league_df["confidence"].mode()[0],
                "data": league_df[
                    [
                        "hoursSinceLaunch",
                        "valueInChaos",
                        "valueInMostCommonCurrencyUsed",
                        "confidence",
                    ]
                ].to_dict("records"),
            }
            data.append(timeseries_data)

        return {"mostCommonCurrencyUsed": mostCommonCurrencyUsed, "data": data}

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

        plot_data = self._create_plot_data(df)

        return self.validate(plot_data)
