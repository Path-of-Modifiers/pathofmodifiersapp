from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import get_db
from app.api.utils import get_delete_return_message
from app.crud import CRUD_currency

router = APIRouter()


currency_prefix = "currency"


@router.get(
    "/{currencyId}",
    response_model=schemas.Currency | list[schemas.Currency],
)
async def get_currency(
    currencyId: int,
    db: Session = Depends(get_db),
):
    """
    Get currency by key and value for "currencyId".

    Always returns one currency.
    """

    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(db=db, filter=currency_map)

    return currency


@router.get("/", response_model=schemas.Currency | list[schemas.Currency])
async def get_all_currencies(
    db: Session = Depends(get_db),
):
    """
    Get all currencies.

    Returns a list of all currencies.
    """

    all_currencies = await CRUD_currency.get(db=db)

    return all_currencies


@router.get("/latest_currency_id/", response_model=int, tags=["latest_currency_id"])
async def get_latest_currency_id(
    db: Session = Depends(get_db),
):
    """
    Get the latest currencyId

    Can only be used safely on an empty table or directly after an insertion.
    """

    result = db.execute(text("""SELECT MAX("currencyId") FROM currency""")).fetchone()
    if result:
        return int(result[0])
    else:
        return 1


@router.post(
    "/",
    response_model=schemas.CurrencyCreate | list[schemas.CurrencyCreate],
)
async def create_currency(
    currency: schemas.CurrencyCreate | list[schemas.CurrencyCreate],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """

    return await CRUD_currency.create(db=db, obj_in=currency)


@router.put("/{currencyId}", response_model=schemas.Currency)
async def update_currency(
    currencyId: int,
    currency_update: schemas.CurrencyUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a currency by key and value for "currencyId".

    Returns the updated currency.
    """

    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(
        db=db,
        filter=currency_map,
    )

    return await CRUD_currency.update(db_obj=currency, obj_in=currency_update, db=db)


@router.delete("/{currencyId}", response_model=str)
async def delete_currency(
    currencyId: int,
    db: Session = Depends(get_db),
):
    """
    Delete a currency by key and value for "currencyId".

    Returns a message indicating the currency was deleted.
    Always deletes one currency.
    """

    currency_map = {"currencyId": currencyId}
    await CRUD_currency.remove(db=db, filter=currency_map)

    return get_delete_return_message(currency_prefix, currency_map)
