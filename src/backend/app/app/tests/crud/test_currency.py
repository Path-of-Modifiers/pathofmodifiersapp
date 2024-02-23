from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.currency import Currency, CurrencyCreate, CurrencyUpdate
from app import crud
from backend.app.app.tests.utils.model_utils.currency import create_random_currency
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url


async def test_create_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    assert currency.currencyName == currency.currencyName
    assert currency.valueInChaos == currency.valueInChaos
    assert currency.iconUrl == currency.iconUrl


async def test_get_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    assert stored_currency
    assert currency.currencyName == stored_currency.currencyName
    assert currency.valueInChaos == stored_currency.valueInChaos
    assert currency.iconUrl == stored_currency.iconUrl


async def test_get_all_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    assert stored_currency
    all_currencys = crud.CRUD_currency.get(db)
    assert stored_currency in all_currencys


async def test_update_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    random_currency_name = random_lower_string()
    random_icon_url = random_url()
    random_valueInChaos = random_float()
    currency_update = CurrencyUpdate(
        currencyName=random_currency_name,
        valueInChaos=random_valueInChaos,
        iconUrl=random_icon_url,
    )
    updated_currency = await crud.CRUD_currency.update(
        db, db_obj=stored_currency, obj_in=currency_update
    )
    assert updated_currency
    assert updated_currency.currencyName == random_currency_name
    assert updated_currency.valueInChaos == random_valueInChaos
    assert updated_currency.iconUrl == random_icon_url


async def test_delete_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    deleted_currency = await crud.CRUD_currency.remove(db, filter=currency_name_map)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    assert stored_currency is None
    assert deleted_currency
    assert currency.currencyName == deleted_currency.currencyName
    assert currency.valueInChaos == deleted_currency.valueInChaos
    assert currency.iconUrl == deleted_currency.iconUrl
