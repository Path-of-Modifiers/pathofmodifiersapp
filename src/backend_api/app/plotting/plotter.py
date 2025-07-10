from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import pandas as pd
from pydantic import TypeAdapter
from sqlalchemy import (
    BinaryExpression,
    ColumnElement,
    Label,
    Result,
    and_,
    or_,
    select,
    text
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.expression import Select

from app.core.models.database import engine
from app.core.models.models import (
    Currency as model_Currency,
)
from app.core.models.models import (
    Item as model_Item,
)
from app.core.models.models import (
    ItemBaseType as model_ItemBaseType,
)
from app.core.models.models import (
    ItemModifier as model_ItemModifier,
)
from app.core.models.models import (
    UnidentifiedItem as model_UniItem,
)
from app.core.models.models import (
    UnidentifiedItem as model_UnidentifiedItem,
)
from app.core.schemas.plot import (
    BasePlotQuery,
    IdentifiedPlotQuery,
    ItemSpecs,
    ModifierLimitations,
    PlotData,
    PlotQuery,
    UnidentifiedPlotQuery,
    WantedModifier,
)
from app.exceptions.model_exceptions.plot_exception import (
    PlotQueryDataNotFoundError,
    PlotQueryInvalidError,
)
from app.logs.logger import plot_logger
from app.utils.timing_tracker import async_timing_tracker, sync_timing_tracker

Q = TypeVar("Q", bound=PlotQuery)


class _BasePlotter(ABC, Generic[Q]):
    "Base for plotting strategies"

    def __init__(self):
        self.validate = TypeAdapter(PlotData).validate_python

    @abstractmethod
    def _raise_invalid_query(self, query: Q) -> None:
        "Raise PlotQueryInvalidError exception if the query is invalid"

    @abstractmethod
    def _convert_plot_query_type(self, query: Q) -> Q:
        "Converts to correct query type based on query specifications"

    @abstractmethod
    def _create_plot_statement(self, query: Q) -> Select:
        "Creates SQLAlchmy select statement from the plot query"

    @abstractmethod
    async def _plot_execute(self, db: AsyncSession, *, statement: Select) -> tuple:
        "Executes statement to the database. Returns result as rows."

    @abstractmethod
    async def plot(self, db: AsyncSession, *, query: Q) -> PlotData:
        "Main orchestrator. Performs all necessary actions to perform plot query and return plot data"

    def _init_stmt(
        self,
        query: Q,
        *,
        item_model: type[model_Item | model_UniItem],
        start: int | None,
        end: int | None,
        query_select_args: list[Any] | None = None,  # optional additions to select
    ) -> Select:
        select_args: list[InstrumentedAttribute[Any] | Label[Any]] = [
            item_model.itemId,
            item_model.createdHoursSinceLaunch,
            item_model.league,
            item_model.itemBaseTypeId,
            item_model.currencyId,
            item_model.currencyAmount,
            model_Currency.tradeName,
            model_Currency.valueInChaos,
            model_Currency.createdHoursSinceLaunch.label(
                "currencyCreatedHoursSinceLaunch"
            ),
        ]
        if query_select_args:
            select_args.extend(query_select_args)

        stmt = (
            select(*select_args)
            .join(model_Currency, item_model.currencyId == model_Currency.currencyId)
        )

        if isinstance(query.league, list):
            stmt = stmt.where(
                or_(*[model_Item.league == league for league in query.league])
            )
        else:
            stmt = stmt.where(model_Item.league == query.league)

        if start is not None:
            stmt = stmt.where(item_model.createdHoursSinceLaunch >= start)
        if end is not None:
            stmt = stmt.where(item_model.createdHoursSinceLaunch <= end)

        return stmt

    def _filter_base_specs(
        self,
        statement: Select,
        *,
        item_model: type[model_Item | model_UniItem],
        query: Q,
    ) -> Select:
        base_spec_query = query.baseSpecifications
        if base_spec_query is not None:
            if base_spec_query.itemBaseTypeId is not None:
                return statement.where(
                    item_model.itemBaseTypeId == base_spec_query.itemBaseTypeId
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
                subquery = subquery.where(and_(True, *base_spec_conditions))

                return statement.where(item_model.itemBaseTypeId.in_(subquery))

        else:
            return statement

    def filter_item_lvl(
        self,
        statement: Select,
        *,
        item_model: type[model_Item | model_UniItem],
        query: Q,
    ) -> Select:
        item_spec_query = query.itemSpecifications
        item_lvls = []
        if item_spec_query:
            if item_spec_query.minIlvl is not None:
                item_lvls.append(item_model.ilvl >= item_spec_query.minIlvl)
            if item_spec_query.maxIlvl is not None:
                item_lvls.append(item_model.ilvl <= item_spec_query.maxIlvl)

        return statement.where(and_(True, *item_lvls))

    @sync_timing_tracker
    def _convert_result_to_df(self, result: Result) -> pd.DataFrame:
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=result.keys())
        return df

    @async_timing_tracker
    async def _perform_plot_db_stmt(
        self, db: AsyncSession, *, statement: Select
    ) -> Result:
        async with db.begin():
            result = await db.execute(statement)

        return result
    
    @sync_timing_tracker
    def _create_plot_data(self, df: pd.DataFrame) -> PlotData:
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

        return self.validate({"mostCommonCurrencyUsed": mostCommonCurrencyUsed, "data": data})



class IdentifiedPlotter(_BasePlotter):
    "Plotter strategy for identified items"

    def _raise_invalid_query(self, query: PlotQuery) -> None:
        if not query.wantedModifiers or len(query.wantedModifiers) == 0:
            detail = (
                "Could not perform plot. Query does not have `wantedModifiers` "
                "specified (wrong for this strategy)"
            )
            raise PlotQueryInvalidError(
                detail=detail,
                query_data=str(query),
                function_name=self._raise_invalid_query.__name__,
                class_name=self.__class__.__name__,
            )
        elif (
            query.wantedModifiers
            and query.itemSpecifications
            and query.itemSpecifications.identified is False
        ):
            detail = (
                "Could not perform plot. Query has `identified`=False "
                "with modifiers specified (wrong for this strategy)"
            )
            raise PlotQueryInvalidError(
                detail=detail,
                query_data=str(query),
                function_name=self._raise_invalid_query.__name__,
                class_name=self.__class__.__name__,
            )

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
            return and_(True, *and_conditions)

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
        wanted_modifier = None  # Gets set to the last mod after loop below
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
                                True,
                                *and_conditions,
                            )
                        )
                        .exists()
                    )

            if wanted_modifier and not modifier_roll_limitation_found:
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
                    select(1).where(and_(True, *and_conditions)).exists()
                )

        return statement.where(and_(True, *exists_conditions))

    def _filter_item_names(
        self,
        statement: Select,
        *,
        query: IdentifiedPlotQuery,
    ) -> Select:
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

    def _filter_item_specs(
        self, statement: Select, *, item_spec_query: ItemSpecs
    ) -> Select:
        item_spec_query_fields = item_spec_query.model_fields.copy()
        item_specifications = []

        if item_spec_query.name is not None:
            # name has already been applied
            item_spec_query_fields.pop("name")

        # ilvl has already been applied
        if item_spec_query.minIlvl is not None:
            item_spec_query_fields.pop("minIlvl")
        if item_spec_query.maxIlvl is not None:
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

        return statement.where(and_(True, *item_specifications))

    def _filter_properties(
        self,
        statement: Select,
        *,
        query: IdentifiedPlotQuery,
        start: int | None,
        end: int | None,
    ) -> Select:
        """
        Prioritizes filtering the largest amount of rows
        """
        statement = self._add_wanted_modifiers(
            statement,
            wanted_modifier_query=query.wantedModifiers,
            start=start,
            end=end,
        )

        if query.itemSpecifications is not None:
            statement = self._filter_item_specs(
                statement, item_spec_query=query.itemSpecifications
            )

        return statement

    def _create_plot_statement(self, query: IdentifiedPlotQuery) -> Select:
        start, end = query.start, query.end
        statement = self._init_stmt(query, item_model=model_Item, start=start, end=end)
        statement = self._filter_base_specs(
            statement, item_model=model_Item, query=query
        )
        statement = self._filter_item_names(statement, query=query)
        statement = self.filter_item_lvl(statement, item_model=model_Item, query=query)
        statement = self._filter_properties(
            statement, query=query, start=start, end=end
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
                ORDER BY r."createdHoursSinceLaunch"
            )

            SELECT filteredPrices."createdHoursSinceLaunch" AS "hoursSinceLaunch", filteredPrices.league, AVG(filteredPrices."valueInChaos") AS "valueInChaos", AVG(filteredPrices."valueInMostCommonCurrencyUsed") AS "valueInMostCommonCurrencyUsed", MIN(filteredPrices."mostCommonCurrencyUsed") AS "mostCommonCurrencyUsed", MIN(filteredPrices.confidence) AS confidence
            FROM filteredPrices
            GROUP BY filteredPrices."createdHoursSinceLaunch", filteredPrices.league
            """
        )
        return full_statement

    async def _plot_execute(self, db: AsyncSession, *, statement: Select) -> PlotData:
        result = await self._perform_plot_db_stmt(db, statement=statement)
        df = self._convert_result_to_df(result)

        if df.empty:
            raise PlotQueryDataNotFoundError(
                query_data=str(statement),
                function_name=self.plot.__name__,
                class_name=self.__class__.__name__,
            )

        return self._create_plot_data(df)

    def _convert_plot_query_type(self, query: PlotQuery) -> IdentifiedPlotQuery:
        query_dump = query.model_dump()
        return IdentifiedPlotQuery(**query_dump)

    @async_timing_tracker
    async def plot(self, db: AsyncSession, *, query: PlotQuery) -> PlotData:
        self._raise_invalid_query(query)

        # Convert to make sure wantedModifiers are specified for identified items
        identified_query = self._convert_plot_query_type(query)

        statement = self._create_plot_statement(identified_query)
        # Logs statement in nice format
        log_stmt = statement.compile(engine, compile_kwargs={"literal_binds": True})
        plot_logger.info(f"{log_stmt}")
        return await self._plot_execute(db, statement=statement)


class UnidentifiedPlotter(_BasePlotter):
    "Plotter strategy for unidentified items"

    def _raise_invalid_query(self, query: PlotQuery) -> None:
        if (
            query.itemSpecifications
            and query.itemSpecifications.identified is not False
        ):
            detail = (
                f"Could not plot unidentified item, because `identified`!=False. "
                f"Value: {query.itemSpecifications.identified} (wrong for this plot strategy)"
            )
            raise PlotQueryInvalidError(
                query_data=str(query),
                detail=detail,
                function_name=self._raise_invalid_query.__name__,
                class_name=self.__class__.__name__,
            )
        elif query.wantedModifiers:
            detail = (
                f"Could not plot unidentified item, because `wantedModifiers` are specified. "
                f"Value: {query.wantedModifiers} (wrong for this plot strategy)"
            )
            raise PlotQueryInvalidError(
                query_data=str(query),
                detail=detail,
                function_name=self._raise_invalid_query.__name__,
                class_name=self.__class__.__name__,
            )

    def _filter_unidentified_agg(self, statement: Select) -> Select:
        statement = statement.where(
            and_(
                True,
                model_UnidentifiedItem.identified.is_(False),
                model_UnidentifiedItem.aggregated.is_(True),
            )
        )

        return statement
    
    def _convert_plot_query_type(self, query: PlotQuery) -> UnidentifiedPlotQuery:
        query_dump = query.model_dump()
        return UnidentifiedPlotQuery(**query_dump)

    def _create_plot_statement(self, query: UnidentifiedPlotQuery) -> Select:
        start, end = query.start, query.end
        q_add_args = [model_UnidentifiedItem.nItems]
        statement = self._init_stmt(
            query,
            item_model=model_UnidentifiedItem,
            start=start,
            end=end,
            query_select_args=q_add_args,
        )
        statement = self._filter_base_specs(
            statement, item_model=model_UnidentifiedItem, query=query
        )
        statement = self.filter_item_lvl(
            statement, item_model=model_UnidentifiedItem, query=query
        )
        statement = self._filter_unidentified_agg(statement)

        full_statement = text(
            f"""
            WITH baseQuery AS (
                {statement.compile(
                dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
            ).string}
            )

            SELECT baseQuery."createdHoursSinceLaunch" AS "hoursSinceLaunch", baseQuery.league, baseQuery."currencyAmount" * baseQuery."valueInChaos", baseQuery."currencyAmount" AS "valueInMostCommonCurrencyUsed", baseQuery."tradeName" AS "mostCommonCurrencyUsed", 
                CASE 
                    WHEN baseQuery."nItems" < 10 THEN 'low'
                    WHEN baseQuery."nItems" < 15 THEN 'medium'
                    ELSE 'high'
                END AS confidence
            FROM baseQuery
            ORDER BY baseQuery."createdHoursSinceLaunch"

            """)

        return full_statement

    async def _plot_execute(
        self, db: AsyncSession, *, statement: Select
    ) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series, str]:
        result = await self._perform_plot_db_stmt(db, statement=statement)
        df = self._convert_result_to_df(result)

        if df.empty:
            raise PlotQueryDataNotFoundError(
                query_data=str(statement),
                function_name=self.plot.__name__,
                class_name=self.__class__.__name__,
            )

        return self.validate(self._create_plot_data(df))
        
    async def plot(self, db: AsyncSession, *, query: PlotQuery) -> PlotData:
        self._raise_invalid_query(query)

        unidentified_query = self._convert_plot_query_type(query)

        statement = self._create_plot_statement(unidentified_query)
        # Logs statement in nice format
        log_stmt = statement.compile(engine, compile_kwargs={"literal_binds": True})
        plot_logger.info(f"{log_stmt}")

        return await self._plot_execute(db, statement=statement)


def configure_plotter_by_query(
    query: PlotQuery,
) -> _BasePlotter:
    "Determines which plotting strategy to use based on the query"

    wants_mods = getattr(query, "wantedModifiers", None)
    if (
        query.itemSpecifications
        and not wants_mods
        and query.itemSpecifications.identified is False
    ):
        # NB: identified must be False for this plotter strategy
        # identified = None does not trigger this strategy
        return UnidentifiedPlotter()
    else:
        return IdentifiedPlotter()


class PlotterService:
    "Performs plotter strategy methods based on plotter configuration"

    async def plot(
        self, plotter: _BasePlotter, db: AsyncSession, query: BasePlotQuery
    ) -> PlotData:
        return await plotter.plot(db, query=query)
