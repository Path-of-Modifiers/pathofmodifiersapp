from __future__ import annotations
import fastapi as _fastapi
from typing import TYPE_CHECKING, List


import schemas as _schemas
import services as _services


import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()


@app.post("/api/currencys/", response_model=_schemas.Currency)
async def create_currency(
    currency: _schemas.CreateCurrency,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.create_currency(currency=currency, db=db)


@app.get("/api/currencys/", response_model=List[_schemas.Currency])
async def get_currencys(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_currencys(db=db)


@app.get("/api/currencys/{currencyName}", response_model=_schemas.Currency)
async def get_currency(
    currencyName: str, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    currency = await _services.get_currency(currencyName=currencyName, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")
    return currency


@app.delete("/api/currencys/{currencyName}")
async def delete_currency(
    currencyName: str, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    currency = await _services.get_currency(currencyName=currencyName, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")
    await _services.delete_currency(currency, db=db)

    return "currency deleted successfully"


@app.put("/api/currencys/{currencyName}", response_model=_schemas.Currency)
async def update_currency(
    currencyName: str,
    currency_data: _schemas.CreateCurrency,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    currency = await _services.get_currency(currencyName=currencyName, db=db)
    if currency is None:
        raise _fastapi.HTTPException(status_code=404, detail="currency not found")

    return await _services.update_currency(
        currency_data=currency_data, currency=currency, db=db
    )
