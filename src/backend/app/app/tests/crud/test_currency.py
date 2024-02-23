from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.currency import CurrencyUpdate
from backend.app.app.tests.utils.model_utils.currency import (
    create_random_currency,
    create_random_currency_list,
)
from backend.app.app.tests.utils.utils import (
    random_float,
    random_lower_string,
    random_url,
)


async def test_create_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    stored_created_currency = await crud.CRUD_currency.create(db, obj_in=currency)
    assert stored_created_currency
    assert stored_created_currency.currencyName == currency.currencyName
    assert stored_created_currency.valueInChaos == currency.valueInChaos
    assert stored_created_currency.iconUrl == currency.iconUrl


async def test_get_currency(db: Session) -> None:
    currency = await create_random_currency(db)
    currency_name_map = {"currencyName": currency.currencyName}
    stored_currency = await crud.CRUD_currency.get(db, filter=currency_name_map)
    assert stored_currency
    assert stored_currency.currencyName == currency.currencyName
    assert stored_currency.valueInChaos == currency.valueInChaos
    assert stored_currency.iconUrl == currency.iconUrl


async def test_create_multiple_currencys(db: Session) -> None:
    currencys = await create_random_currency_list(db=db, count=5)
    stored_currencys = await crud.CRUD_currency.get(db)
    assert len(stored_currencys) == 5
    for stored_currency in stored_currencys:
        assert stored_currency in currencys


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
    assert deleted_currency.currencyName == currency.currencyName
    assert deleted_currency.valueInChaos == currency.valueInChaos
    assert deleted_currency.iconUrl == currency.iconUrl
