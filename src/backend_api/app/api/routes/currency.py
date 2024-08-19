from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    SessionDep,
    get_current_active_superuser,
    get_current_active_user,
)
from app.core.models.models import Currency
from app.crud import CRUD_currency

router = APIRouter()


currency_prefix = "currency"


@router.get(
    "/{currencyId}",
    response_model=schemas.Currency,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_currency(
    currencyId: int,
    db: SessionDep,
):
    """
    Get currency by key and value for "currencyId".

    Always returns one currency.
    """

    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(db=db, filter=currency_map)

    return currency


@router.get(
    "/",
    response_model=schemas.Currency | list[schemas.Currency],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_all_currencies(
    db: SessionDep,
):
    """
    Get all currencies.

    Returns a list of all currencies.
    """

    all_currencies = await CRUD_currency.get(db=db)

    return all_currencies


@router.get(
    "/latest_currency_id/",
    response_model=int,
    tags=["latest_currency_id"],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
async def get_latest_currency_id(
    db: SessionDep,
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
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_currency(
    currency: schemas.CurrencyCreate | list[schemas.CurrencyCreate],
    db: SessionDep,
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """

    return await CRUD_currency.create(db=db, obj_in=currency)


@router.put(
    "/{currencyId}",
    response_model=schemas.Currency,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def update_currency(
    currencyId: int,
    currency_update: schemas.CurrencyUpdate,
    db: SessionDep,
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


@router.delete(
    "/{currencyId}",
    response_model=str,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def delete_currency(
    currencyId: int,
    db: SessionDep,
):
    """
    Delete a currency by key and value for "currencyId".

    Returns a message indicating the currency was deleted.
    Always deletes one currency.
    """

    currency_map = {"currencyId": currencyId}
    await CRUD_currency.remove(db=db, filter=currency_map)

    return get_delete_return_msg(
        model_table_name=Currency.__tablename__, mapping=currency_map
    ).message
