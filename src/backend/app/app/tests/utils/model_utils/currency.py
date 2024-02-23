from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency
from app.core.schemas import CurrencyCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_float



def create_random_currency(db: Session) -> Currency:
    currencyName = random_lower_string()
    valueInChaos = random_float()
    iconUrl = random_lower_string()
    currency = CurrencyCreate(
        currencyName=currencyName,
        valueInChaos=valueInChaos,
        iconUrl=iconUrl,
    )
    return crud.CRUD_currency.create(db, obj_in=currency)