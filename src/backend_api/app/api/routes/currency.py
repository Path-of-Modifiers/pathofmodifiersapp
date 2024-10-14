from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.core.config import settings
from app.core.models.models import Currency
from app.crud import CRUD_currency
from app.limiter import apply_user_rate_limits

router = APIRouter()


currency_prefix = "currency"


@router.get(
    "/{currencyId}",
    response_model=schemas.Currency,
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_currency(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
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


@router.get(
    "/",
    response_model=schemas.Currency | list[schemas.Currency],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_all_currencies(
    db: Session = Depends(get_db),
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
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_latest_currency_id(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
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
    response_model=schemas.CurrencyCreate | list[schemas.CurrencyCreate] | None,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_currency(
    currency: schemas.CurrencyCreate | list[schemas.CurrencyCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """

    return await CRUD_currency.create(
        db=db, obj_in=currency, return_nothing=return_nothing
    )


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


@router.delete(
    "/{currencyId}",
    response_model=str,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
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

    return get_delete_return_msg(
        model_table_name=Currency.__tablename__, filter=currency_map
    ).message
