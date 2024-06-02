from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_currency

import app.core.schemas as schemas

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.security import verification


router = APIRouter()


currency_prefix = "currency"


@router.get(
    "/{currencyId}",
    response_model=Union[schemas.Currency, List[schemas.Currency]],
)
async def get_currency(currencyId: str, db: Session = Depends(get_db)):
    """
    Get currency by key and value for "currencyId".

    Always returns one currency.
    """
    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(db=db, filter=currency_map)

    return currency


@router.get("/", response_model=Union[schemas.Currency, List[schemas.Currency]])
async def get_all_currencies(db: Session = Depends(get_db)):
    """
    Get all currencies.

    Returns a list of all currencies.
    """
    all_currencies = await CRUD_currency.get(db=db)

    return all_currencies


@router.get("/latest_currency_id/", response_model=int, tags=["latest_currency_id"])
async def get_latest_currency_id(db: Session = Depends(get_db)):
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
    response_model=Union[schemas.CurrencyCreate, List[schemas.CurrencyCreate]],
)
async def create_currency(
    currency: Union[schemas.CurrencyCreate, List[schemas.CurrencyCreate]],
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {create_currency.__name__}",
        )

    return await CRUD_currency.create(db=db, obj_in=currency)


@router.put("/{currencyId}", response_model=schemas.Currency)
async def update_currency(
    currencyId: str,
    currency_update: schemas.CurrencyUpdate,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Update a currency by key and value for "currencyId".

    Returns the updated currency.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {update_currency.__name__}",
        )

    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(
        db=db,
        filter=currency_map,
    )

    return await CRUD_currency.update(db_obj=currency, obj_in=currency_update, db=db)


@router.delete("/{currencyId}", response_model=str)
async def delete_currency(
    currencyId: str,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Delete a currency by key and value for "currencyId".

    Returns a message indicating the currency was deleted.
    Always deletes one currency.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {delete_currency.__name__}",
        )

    currency_map = {"currencyId": currencyId}
    await CRUD_currency.remove(db=db, filter=currency_map)

    return f"{currency_prefix} with mapping ({currency_map}) deleted successfully"
