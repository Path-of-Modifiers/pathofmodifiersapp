from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import ColumnElement, and_, func, or_

from app.api.params import FilterParams
from app.core.models.models import CurrencyPrice as model_CurrencyPrice
from app.core.models.models import CurrencyType as model_CurrencyType
from app.core.schemas.currency import (
    Currency,
    CurrencyPrice,
    CurrencyPriceCreate,
    CurrencyPriceUpdate,
    CurrencyQuery,
    CurrencyType,
    CurrencyTypeCreate,
    CurrencyTypeUpdate,
)
from app.crud.base import CRUDBase


class CRUDCurrency:
    def __init__(self):
        self.crud_price = CRUDBase[
            model_CurrencyPrice, CurrencyPrice, CurrencyPriceCreate, CurrencyPriceUpdate
        ](
            model=model_CurrencyPrice,
            schema=CurrencyPrice,
            create_schema=CurrencyPriceCreate,
        )
        self.crud_type = CRUDBase[
            model_CurrencyType, CurrencyType, CurrencyTypeCreate, CurrencyTypeUpdate
        ](
            model=model_CurrencyType,
            schema=CurrencyType,
            create_schema=CurrencyTypeCreate,
        )

        self.latest_hours_validate = TypeAdapter(dict[int, int]).validate_python
        self.currency_list_validate = TypeAdapter(list[Currency]).validate_python

    async def get_prices(self, *args, **kwargs):
        return await self.crud_price.get(*args, **kwargs)

    async def get_types(self, *args, **kwargs):
        return await self.crud_type.get(*args, **kwargs)

    async def create_prices(self, *args, **kwargs):
        return await self.crud_price.create(*args, **kwargs)

    async def create_types(self, *args, **kwargs):
        return await self.crud_type.create(*args, **kwargs)

    async def update_type(self, *args, **kwargs):
        return await self.crud_type.update(*args, **kwargs)

    def _latest_hours_stmt(self, league_ids: list[int]):
        return (
            select(
                model_CurrencyPrice.leagueId,
                func.max(model_CurrencyPrice.createdHoursSinceLaunch).label(
                    "latest_hour"
                ),
            )
            .where(model_CurrencyPrice.leagueId.in_(league_ids))
            .group_by(model_CurrencyPrice.leagueId)
        )

    async def get_latest_hours(
        self, db: Session, league_ids: list[int]
    ) -> dict[int, int]:
        stmt = self._latest_hours_stmt(league_ids)

        objs = db.execute(stmt).mappings().all()
        id_hour_map = {obj["leagueId"]: obj["latest_hour"] for obj in objs}

        return self.latest_hours_validate(id_hour_map)

    async def get_latest_currencies(
        self, db: Session, league_ids: list[int]
    ) -> list[Currency]:
        latest_hours = self._latest_hours_stmt(league_ids).subquery()

        stmt = (
            select(
                model_CurrencyType.currencyId,
                model_CurrencyType.name,
                model_CurrencyType.tradeName,
                model_CurrencyPrice.leagueId,
                model_CurrencyPrice.createdHoursSinceLaunch,
                model_CurrencyPrice.valueInChaos,
            )
            .join(
                latest_hours,
                (model_CurrencyPrice.leagueId == latest_hours.c.leagueId)
                & (
                    model_CurrencyPrice.createdHoursSinceLaunch
                    == latest_hours.c.latest_hour
                ),
            )
            .join(
                model_CurrencyType,
                model_CurrencyPrice.currencyId == model_CurrencyType.currencyId,
            )
        )
        currencies = db.execute(stmt).mappings().all()

        return self.currency_list_validate(currencies)

    async def get_currency_from_query(
        self,
        db: Session,
        query_list: list[CurrencyQuery] | None = None,
        filter_params: FilterParams | None = None,
    ) -> list[Currency]:
        stmt = select(
            model_CurrencyType.currencyId,
            model_CurrencyType.name,
            model_CurrencyType.tradeName,
            model_CurrencyPrice.leagueId,
            model_CurrencyPrice.createdHoursSinceLaunch,
            model_CurrencyPrice.valueInChaos,
        ).join(
            model_CurrencyType,
            model_CurrencyPrice.currencyId == model_CurrencyType.currencyId,
        )
        if query_list:
            filters = list[ColumnElement[bool]]()
            for query in query_list:
                sub_filter = list[ColumnElement[bool]]()
                if query.createdHoursSinceLaunch is not None:
                    sub_filter.append(
                        model_CurrencyPrice.createdHoursSinceLaunch
                        == query.createdHoursSinceLaunch
                    )

                if query.tradeName is not None:
                    sub_filter.append(model_CurrencyType.tradeName == query.tradeName)

                if query.leagueId is not None:
                    sub_filter.append(model_CurrencyPrice.leagueId == query.leagueId)

                if sub_filter:
                    filters.append(and_(*sub_filter))

            stmt = stmt.where(or_(*filters))

        if filter_params is not None:
            if filter_params.skip is not None:
                stmt = stmt.offset(filter_params.skip)
            if filter_params.limit is not None:
                stmt = stmt.limit(filter_params.limit)

        currencies = db.execute(stmt).mappings().all()

        if filter_params is not None:
            currencies = self.crud_price._sort_objects(
                currencies, filter_params.sort_key, filter_params.sort_method
            )

        return self.currency_list_validate(currencies)
