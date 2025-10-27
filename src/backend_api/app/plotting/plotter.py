from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import pandas as pd
from pydantic import TypeAdapter
from pydantic.fields import FieldInfo
from sqlalchemy import (
    BinaryExpression,
    ColumnElement,
    Label,
    Result,
    and_,
    case,
    desc,
    func,
    literal,
    or_,
    select,
)
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
    async def _plot_execute(self, db: AsyncSession, *, statement: Select) -> PlotData:
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

        stmt = select(*select_args).join(
            model_Currency, item_model.currencyId == model_Currency.currencyId
        )

        if isinstance(query.league, list):
            stmt = stmt.where(
                or_(*[item_model.league == league for league in query.league])
            )
        else:
            stmt = stmt.where(model_Item.league == query.league)

        if start is not None:
            stmt = stmt.where(item_model.createdHoursSinceLaunch >= start)
        if end is not None:
            stmt = stmt.where(item_model.createdHoursSinceLaunch <= end)

        return stmt

    def _filter_item_names(
        self,
        statement: Select,
        *,
        item_model: type[model_Item | model_UniItem],
        query: Q,
    ) -> Select:
        if query.itemSpecifications is not None:
            if query.itemSpecifications.name is not None:
                if "|" in query.itemSpecifications.name:
                    name_filter = or_(
                        *[
                            item_model.name == name
                            for name in query.itemSpecifications.name.split("|")
                        ]
                    )
                else:
                    name_filter = item_model.name == query.itemSpecifications.name
                statement = statement.where(name_filter)

        return statement

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
                statement = statement.where(
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

                statement = statement.where(item_model.itemBaseTypeId.in_(subquery))

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
        df = pd.DataFrame(rows, columns=result.keys())  # type: ignore
        return df

    @async_timing_tracker
    async def _perform_plot_db_statement(
        self, db: AsyncSession, *, statement: Select
    ) -> Result:
        async with db.begin():
            result = await db.execute(statement)

        return result

    @sync_timing_tracker
    def _create_plot_data(self, df: pd.DataFrame) -> PlotData:
        mostCommonCurrencyUsed = df["mostCommonCurrencyUsed"].get(
            0, "divine"
        )  # TODO: set enum
        data = []
        for league in df["league"].unique():
            league_df: pd.DataFrame = df.loc[df["league"] == league]
            league_data = league_df[
                [
                    "hoursSinceLaunch",
                    "valueInChaos",
                    "valueInMostCommonCurrencyUsed",
                    "confidence",
                ]
            ].to_dict(orient="records")  # type: ignore
            timeseries_data = {
                "name": league,
                "confidenceRating": league_df["confidence"].mode()[0],
                "data": league_data,
            }
            data.append(timeseries_data)

        return self.validate(
            {"mostCommonCurrencyUsed": mostCommonCurrencyUsed, "data": data}
        )


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

    def _filter_item_specs(
        self, statement: Select, *, item_spec_query: ItemSpecs
    ) -> Select:
        item_spec_query_fields: dict[
            str, FieldInfo
        ] = item_spec_query.__class__.model_fields.copy()
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
        statement = self._init_stmt(
            query,
            item_model=model_Item,
            start=start,
            end=end,
            query_select_args=[model_Item.gameItemId],
        )
        statement = self._filter_base_specs(
            statement, item_model=model_Item, query=query
        )
        statement = self._filter_item_names(
            statement, item_model=model_Item, query=query
        )
        statement = self.filter_item_lvl(statement, item_model=model_Item, query=query)
        statement = self._filter_properties(
            statement, query=query, start=start, end=end
        )
        base_query = statement.cte("baseQuery")

        most_common = (
            select(
                base_query.c["tradeName"].label("mostCommonTradeName"),
                func.count(base_query.c["tradeName"]).label("nameCount"),
            )
            .group_by(base_query.c["league"], base_query.c["tradeName"])
            .order_by(desc("nameCount"))  # Can use literal_column in complex cases
            .limit(1)
            .cte("mostCommon")
        )

        most_common_ids = (
            select(
                base_query.c["createdHoursSinceLaunch"],
                func.max(base_query.c["currencyId"]).label("mostCommonCurrencyId"),
            )
            .where(
                base_query.c["tradeName"]
                == select(most_common.c["mostCommonTradeName"]).scalar_subquery()
            )
            .group_by(base_query.c["createdHoursSinceLaunch"])
            .cte("mostCommonIds")
        )

        most_common_prices = (
            select(
                base_query.c["createdHoursSinceLaunch"],
                func.min(base_query.c["valueInChaos"]).label("mostCommonValueInChaos"),
                func.min(base_query.c["tradeName"]).label("mostCommonCurrencyUsed"),
            )
            .select_from(
                base_query.join(
                    most_common_ids,
                    and_(
                        base_query.c["createdHoursSinceLaunch"]
                        == most_common_ids.c["createdHoursSinceLaunch"],
                        base_query.c["currencyId"]
                        == most_common_ids.c["mostCommonCurrencyId"],
                    ),
                )
            )
            .group_by(base_query.c["createdHoursSinceLaunch"])
            .cte("mostCommonPrices")
        )

        prices = (
            select(
                base_query.c["createdHoursSinceLaunch"],
                base_query.c["league"],
                base_query.c["gameItemId"],
                (base_query.c["currencyAmount"] * base_query.c["valueInChaos"]).label(
                    "valueInChaos"
                ),
                (
                    base_query.c["currencyAmount"]
                    * base_query.c["valueInChaos"]
                    / most_common_prices.c["mostCommonValueInChaos"]
                ).label("valueInMostCommonCurrencyUsed"),
                most_common_prices.c["mostCommonCurrencyUsed"],
            )
            .select_from(base_query)
            .join(
                most_common_prices,
                base_query.c["createdHoursSinceLaunch"]
                == most_common_prices.c["createdHoursSinceLaunch"],
            )
            .cte("prices")
        )
        ranked_prices = select(
            prices,
            func.rank()
            .over(
                partition_by=prices.c["createdHoursSinceLaunch"],
                order_by=prices.c["valueInChaos"].asc(),
            )
            .label("pos"),
        ).cte("rankedPrices")

        filtered_prices = (
            select(
                ranked_prices.c["createdHoursSinceLaunch"],
                ranked_prices.c["league"],
                ranked_prices.c["gameItemId"],
                ranked_prices.c["valueInChaos"],
                ranked_prices.c["valueInMostCommonCurrencyUsed"],
                ranked_prices.c["mostCommonCurrencyUsed"],
            )
            .where(ranked_prices.c["pos"] <= 5)
            .order_by(ranked_prices.c["createdHoursSinceLaunch"])
            .cte("filteredPrices")
        )

        # overall_most_common_currency_used = (
        overall_most_common_currency_used_unordered = (
            select(
                literal(0).label("join_variable"),
                filtered_prices.c["mostCommonCurrencyUsed"],
                func.count().label("currencyCount"),
            )
            .group_by(filtered_prices.c["mostCommonCurrencyUsed"])
            .cte("overallMostCommonCurrencyUsedUnordered")
        )

        overall_most_common_currency_used = (
            select(overall_most_common_currency_used_unordered)
            .order_by(
                overall_most_common_currency_used_unordered.c["currencyCount"].desc()
            )
            .limit(1)
            .cte("overallMostCommonCurrencyUsed")
        )

        items_per_id = (
            select(filtered_prices.c["gameItemId"], func.count().label("itemCount"))
            .group_by(filtered_prices.c["gameItemId"])
            .cte("itemsPerId")
        )

        prices_per_game_item_id = (
            select(
                filtered_prices.c["gameItemId"],
                func.json_agg(
                    func.json_build_object(
                        "hoursSinceLaunch",
                        filtered_prices.c["createdHoursSinceLaunch"],
                        "valueInChaos",
                        filtered_prices.c["valueInChaos"],
                        "valueInMostCommonCurrencyUsed",
                        filtered_prices.c["valueInMostCommonCurrencyUsed"],
                    )
                ).label("data"),
            )
            .select_from(filtered_prices)
            .join(
                items_per_id,
                filtered_prices.c["gameItemId"] == items_per_id.c["gameItemId"],
            )
            .where(items_per_id.c["itemCount"] > 1)
            .group_by(filtered_prices.c["gameItemId"])
            .cte("pricesPerGameItemId")
        )

        linked_prices = (
            select(
                filtered_prices.c["league"],
                func.json_agg(
                    func.json_build_object(
                        "gameItemId",
                        filtered_prices.c["gameItemId"],
                        "data",
                        prices_per_game_item_id.c["data"],
                    )
                ).label("linkedPrices"),
            )
            .select_from(prices_per_game_item_id)
            .join(
                filtered_prices,
                prices_per_game_item_id.c["gameItemId"]
                == filtered_prices.c["gameItemId"],
            )
            .group_by(filtered_prices.c["league"])
            .cte("linkedPrices")
        )

        unlinked_prices = (
            select(
                filtered_prices.c["league"],
                func.json_agg(
                    func.json_build_object(
                        "hoursSinceLaunch",
                        filtered_prices.c["createdHoursSinceLaunch"],
                        "valueInChaos",
                        filtered_prices.c["valueInChaos"],
                        "valueInMostCommonCurrencyUsed",
                        filtered_prices.c["valueInMostCommonCurrencyUsed"],
                    )
                ).label("unlinkedPrices"),
            )
            .select_from(filtered_prices)
            .join(
                items_per_id,
                filtered_prices.c["gameItemId"] == items_per_id.c["gameItemId"],
            )
            .where(
                or_(
                    filtered_prices.c["gameItemId"].is_(None),
                    items_per_id.c["itemCount"] == 1,
                )
            )
            .group_by(filtered_prices.c["league"])
            .cte("unlinkedPrices")
        )

        league_data = (
            select(
                literal(0).label("join_variable"),
                linked_prices.c["league"],
                linked_prices.c["linkedPrices"],
                unlinked_prices.c["unlinkedPrices"],
            )
            .select_from(linked_prices)
            .join(
                unlinked_prices,
                linked_prices.c["league"] == unlinked_prices.c["league"],
            )
            .cte("leagueData")
        )

        final_query = (
            select(
                overall_most_common_currency_used.c["mostCommonCurrencyUsed"],
                func.json_agg(
                    func.json_build_object(
                        "league",
                        league_data.c["league"],
                        "linkedPrices",
                        league_data.c["linkedPrices"],
                        "unlinkedPrices",
                        league_data.c["unlinkedPrices"],
                    )
                ).label("data"),
            )
            .select_from(overall_most_common_currency_used)
            .join(
                league_data,
                overall_most_common_currency_used.c["join_variable"]
                == league_data.c["join_variable"],
            )
            .group_by(overall_most_common_currency_used.c["mostCommonCurrencyUsed"])
        )

        return final_query

    async def _plot_execute(self, db: AsyncSession, *, statement: Select) -> PlotData:
        result = await self._perform_plot_db_statement(db, statement=statement)
        json_result = result.first()
        if not json_result:
            raise PlotQueryDataNotFoundError(
                query_data=str(statement),
                function_name=self.plot.__name__,
                class_name=self.__class__.__name__,
            )
        return json_result

    def _convert_plot_query_type(self, query: PlotQuery) -> IdentifiedPlotQuery:
        query_dump = query.model_dump()
        return IdentifiedPlotQuery(**query_dump)

    @async_timing_tracker
    async def plot(self, db: AsyncSession, *, query: PlotQuery) -> PlotData:
        self._raise_invalid_query(query)

        # Convert to make sure wantedModifiers are specified for identified items
        identified_query = self._convert_plot_query_type(query)

        stmt = self._create_plot_statement(identified_query)
        # Logs statement in nice format
        log_clause = stmt.compile(engine, compile_kwargs={"literal_binds": True})
        plot_logger.info(f"{log_clause}")

        return await self._plot_execute(db, statement=stmt)


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
        statement = self._filter_item_names(
            statement, item_model=model_UnidentifiedItem, query=query
        )
        statement = self._filter_base_specs(
            statement, item_model=model_UnidentifiedItem, query=query
        )
        statement = self.filter_item_lvl(
            statement, item_model=model_UnidentifiedItem, query=query
        )
        statement = self._filter_unidentified_agg(statement)

        base_query = statement.cte("baseQuery")

        calc_value = select(
            base_query,
            (base_query.c["currencyAmount"] * base_query.c["valueInChaos"]).label(
                "itemValueInChaos"
            ),
        ).cte("calcValue")

        ranked_cheap = select(
            calc_value,
            func.rank()
            .over(
                partition_by=[
                    calc_value.c["createdHoursSinceLaunch"],
                    calc_value.c["league"],
                ],
                order_by=calc_value.c["itemValueInChaos"].asc(),
            )
            .label("cheap"),
        ).cte("rankedCheap")

        final_query = (
            select(
                ranked_cheap.c["createdHoursSinceLaunch"].label("hoursSinceLaunch"),
                ranked_cheap.c["league"],
                (
                    ranked_cheap.c["currencyAmount"]
                    * ranked_cheap.c["itemValueInChaos"]
                ).label("valueInChaos"),
                ranked_cheap.c["currencyAmount"].label("valueInMostCommonCurrencyUsed"),
                ranked_cheap.c["tradeName"].label("mostCommonCurrencyUsed"),
                case(
                    (ranked_cheap.c["nItems"] < 10, "low"),
                    (ranked_cheap.c["nItems"] < 15, "medium"),
                    else_="high",
                ).label("confidence"),
            )
            .where(ranked_cheap.c["cheap"] == 1)
            .order_by(ranked_cheap.c["createdHoursSinceLaunch"])
        )

        return final_query

    async def _plot_execute(self, db: AsyncSession, *, statement: Select) -> PlotData:
        result = await self._perform_plot_db_statement(db, statement=statement)
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
        log_clause = statement.compile(engine, compile_kwargs={"literal_binds": True})
        plot_logger.info(f"{log_clause}")

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
