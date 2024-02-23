from typing import List

from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency
from app.core.schemas import CurrencyCreate
from backend.app.app.tests.utils.utils import random_lower_string
from backend.app.app.tests.utils.utils import random_float
from backend.app.app.tests.utils.utils import random_url


async def create_random_currency(db: Session) -> Currency:
    currencyName = random_lower_string()
    valueInChaos = random_float()
    iconUrl = random_url()

    currency = CurrencyCreate(
        currencyName=currencyName,
        valueInChaos=valueInChaos,
        iconUrl=iconUrl,
    )
    return await crud.CRUD_currency.create(db, obj_in=currency)


def create_random_currency_list(db: Session, count: int = 10) -> List[Currency]:
    return [create_random_currency(db) for _ in range(count)]


async def get_random_currency(session: Session) -> Currency:
    random_currency = session.query(Currency).order_by(func.random()).first()

    if random_currency:
        print(
            f"Found already existing currency. random_currency.currencyName: {random_currency.currencyName}"
        )
    else:
        random_currency = create_random_currency(session)
    return random_currency