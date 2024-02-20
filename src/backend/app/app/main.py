from __future__ import annotations
import fastapi as _fastapi
from typing import List, Union

import app.core.models.models as _models
import app.api.deps as _deps

import app.crud.base as _crud

import app.core.schemas as _schemas


import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Welcome to Path of Modifiers API!"}


currencyCRUD = _crud.CRUDBase[
    _models.Currency,
    _schemas.Currency,
    _schemas.CurrencyCreate,
    _schemas.CurrencyUpdate,
](model=_models.Currency, schema=_schemas.Currency)


@app.post(
    "/api/currency/",
    response_model=Union[_schemas.CurrencyCreate, List[_schemas.CurrencyCreate]],
)
async def create_currency(
    currency: Union[_schemas.CurrencyCreate, List[_schemas.CurrencyCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await currencyCRUD.create(db=db, obj_in=currency)


@app.get("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def get_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_mapped = {"currencyId": currencyId}
    currency = await currencyCRUD.get(db=db, id=currency_mapped)
    return currency


@app.get("/api/currency/", response_model=List[_schemas.Currency])
async def get_all_currency(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_currency = await currencyCRUD.get_all(db=db)
    return all_currency


@app.delete("/api/currency/{currencyName}")
async def delete_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_mapped = {"currencyId": currencyId}
    await currencyCRUD.remove(id=currency_mapped, db=db)

    return f"currency with id {currencyId} deleted successfully"


@app.put("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def update_currency(
    currencyId: str,
    currency_update: _schemas.CurrencyUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    currency_map = {"currencyId": currencyId}
    currency = await currencyCRUD.get(
        db=db,
        id=currency_map,
    )

    return await currencyCRUD.update(db_obj=currency, obj_in=currency_update, db=db)


accountCRUD = _crud.CRUDBase[
    _models.Account,
    _schemas.Account,
    _schemas.AccountCreate,
    _schemas.AccountUpdate,
](model=_models.Account, schema=_schemas.Account)


@app.post(
    "/api/account/",
    response_model=Union[_schemas.AccountCreate, List[_schemas.AccountCreate]],
)
async def create_account(
    account: Union[_schemas.AccountCreate, List[_schemas.AccountCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await accountCRUD.create(db=db, obj_in=account)


@app.get("/api/account/{accountName}", response_model=_schemas.Account)
async def get_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    account = await accountCRUD.get(db=db, id=account_map)
    return account


@app.get("/api/account/", response_model=List[_schemas.Account])
async def get_all_accounts(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_accounts = await accountCRUD.get_all(db=db)
    return all_accounts


@app.delete("/api/account/{accountName}")
async def delete_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    await accountCRUD.remove(db=db, id=account_map)

    return "Account deleted successfully"


@app.put("/api/account/{accountName}", response_model=_schemas.Account)
async def update_account(
    accountName: str,
    account_update: _schemas.AccountUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    account_mapped = {"accountName": accountName}
    account = await accountCRUD.get(
        db=db,
        id=account_mapped,
    )

    return await accountCRUD.update(db_obj=account, obj_in=account_update, db=db)
