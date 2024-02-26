from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

import app.api.deps as deps

from app.crud import CRUD_currency

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{currencyId}",
    response_model=Union[schemas.Currency, List[schemas.Currency]],
)
async def get_currency(currencyId: str, db: Session = Depends(get_db)):
    """
    Get currency by "currencyId".
    """
    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(db=db, filter=currency_map)

    return currency


@router.get("/", response_model=Union[schemas.Currency, List[schemas.Currency]])
async def get_all_currencies(db: Session = Depends(get_db)):
    """
    Get all currencies.
    """
    all_currencies = await CRUD_currency.get(db=db)

    return all_currencies


@router.post(
    "/",
    response_model=Union[schemas.CurrencyCreate, List[schemas.CurrencyCreate]],
)
async def create_currency(
    currency: Union[schemas.CurrencyCreate, List[schemas.CurrencyCreate]],
    db: Session = Depends(get_db),
):
    """
    Create a new currency.
    """
    return await CRUD_currency.create(db=db, obj_in=currency)


@router.put("/{currencyId}", response_model=schemas.Currency)
async def update_currency(
    currencyId: str,
    currency_update: schemas.CurrencyUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update an currency by "currencyId".
    """
    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(
        db=db,
        filter=currency_map,
    )

    return await CRUD_currency.update(db_obj=currency, obj_in=currency_update, db=db)


@router.delete("/{currencyId}", response_model=str)
async def delete_currency(currencyId: str, db: Session = Depends(get_db)):
    """
    Delete a currency by "currencyId".
    """
    currency_map = {"currencyId": currencyId}
    await CRUD_currency.remove(db=db, filter=currency_map)

    return f"Currency with mapping ({currency_map}) deleted successfully"
