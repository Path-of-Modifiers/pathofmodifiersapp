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

    async def get_latest_hour(self, db: Session) -> int:
        stmt = (
            select(model_Currency.createdHoursSinceLaunch)
            .order_by(model_Currency.currencyId.desc())
            .limit(1)
        )

        db_latest_hour = db.execute(stmt).mappings().first()
        if db_latest_hour is not None:
            latest_hour = db_latest_hour["createdHoursSinceLaunch"]
        else:
            latest_hour = -1

        validate = TypeAdapter(int).validate_python

        return validate(latest_hour)

    async def get_latest_currencies(self, db: Session) -> list[Currency]:
        latest_hour = await self.get_latest_hour(db)

        # All rows from that hour, plus the next lower currencyId
        hour_rows = (
            select(
                model_Currency.currencyId,
                model_Currency.createdHoursSinceLaunch,
                func.lead(model_Currency.currencyId)
                .over(order_by=model_Currency.currencyId.desc())
                .label("next_id"),
            ).where(model_Currency.createdHoursSinceLaunch == latest_hour)
        ).cte("hour_rows")

        # The first place where the IDs stop being consecutive
        boundary = (
            select(hour_rows.c.next_id)
            .where(hour_rows.c.currencyId - hour_rows.c.next_id > 1)
            .order_by(hour_rows.c.currencyId.desc())
            .limit(1)
            .scalar_subquery()
        )
        # If no gap exists, include all rows for that hour
        min_id = func.coalesce(
            boundary,
            select(func.min(hour_rows.c.currencyId)).scalar_subquery(),
        )
        stmt = (
            select(model_Currency.__table__)
            .where(
                model_Currency.createdHoursSinceLaunch == latest_hour,
                model_Currency.currencyId >= min_id,
            )
            .order_by(model_Currency.currencyId.desc())
        )
        latest_currencies = db.execute(stmt).mappings().all()

        validate = TypeAdapter(list[Currency]).validate_python

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
