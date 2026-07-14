from collections import defaultdict

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_, func, or_

from app.core.models.models import Currency as model_Currency
from app.core.schemas.currency import (
    Currency,
    CurrencyCreate,
    CurrencyQuery,
    CurrencyUpdate,
)
from app.crud.base import CRUDBase


class CRUDCurrency(
    CRUDBase[
        model_Currency,
        Currency,
        CurrencyCreate,
        CurrencyUpdate,
    ]
):
    async def get_latest_currency_id(self, db: Session) -> int:
        stmt = select(
            func.max(model_Currency.currencyId).label("latestCurrencyId")
        ).limit(1)

        db_latest_currency_id = db.execute(stmt).mappings().first()
        if db_latest_currency_id is not None:
            latest_currency_id = db_latest_currency_id["latestCurrencyId"]
        else:
            latest_currency_id = 1

        validate = TypeAdapter(int).validate_python

        return validate(latest_currency_id)

    def _latest_hours_stmt(self, league_ids: list[int]):
        return (
            select(
                model_Currency.leagueId,
                func.max(model_Currency.createdHoursSinceLaunch).label("latest_hour"),
            )
            .where(model_Currency.leagueId.in_(league_ids))
            .group_by(model_Currency.leagueId)
        )

    async def get_latest_hours(
        self, db: Session, league_ids: list[int]
    ) -> dict[int, int]:
        stmt = self._latest_hours_stmt(league_ids)

        objs = db.execute(stmt).mappings().all()
        id_hour_map = {obj["leagueId"]: obj["latest_hour"] for obj in objs}

        validate = TypeAdapter(dict[int, int]).validate_python

        return validate(id_hour_map)

    async def get_latest_currencies(
        self, db: Session, league_ids: list[int]
    ) -> dict[int, list[Currency]]:
        latest_hours = self._latest_hours_stmt(league_ids).subquery()

        stmt = select(model_Currency).join(
            latest_hours,
            (model_Currency.leagueId == latest_hours.c.leagueId)
            & (model_Currency.createdHoursSinceLaunch == latest_hours.c.latest_hour),
        )
        currencies = db.scalars(stmt).all()

        latest_currencies: dict[int, list[Currency]] = defaultdict(list)
        for currency in currencies:
            latest_currencies[currency.leagueId].append(currency)

        validate = TypeAdapter(dict[int, list[Currency]]).validate_python

        return validate(latest_currencies)

    async def get_currency_from_query(
        self, db: Session, query_list: list[CurrencyQuery]
    ) -> list[Currency]:
        filters = []
        for query in query_list:
            sub_filter = []
            if query.createdHoursSinceLaunch is not None:
                sub_filter.append(
                    model_Currency.createdHoursSinceLaunch
                    == query.createdHoursSinceLaunch
                )

            if query.tradeName is not None:
                sub_filter.append(model_Currency.tradeName == query.tradeName)

            if query.leagueId is not None:
                sub_filter.append(model_Currency.leagueId == query.leagueId)

            if sub_filter:
                filters.append(and_(*sub_filter))
        stmt = select(model_Currency).where(or_(*filters))

        currencies = db.execute(stmt).scalars().all()

        validate = TypeAdapter(list[Currency]).validate_python

        return validate(currencies)
