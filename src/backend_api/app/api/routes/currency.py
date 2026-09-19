from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.api.params import FilterParams
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from app.core.schemas.currency import CurrencyQuery
from app.crud import CRUD_currency

router = APIRouter()


currency_prefix = "currency"


@router.get(
    "/price/",
    response_model=schemas.CurrencyPrice | list[schemas.CurrencyPrice],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
async def get_all_currency_prices(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all currencies.

    Returns a list of all currencies.
    """

    all_currencies = await CRUD_currency.get_prices(db=db, filter_params=filter_params)

    return all_currencies


@router.get(
    "/type/",
    response_model=schemas.CurrencyType | list[schemas.CurrencyType],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
async def get_all_currency_types(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all currencies.

    Returns a list of all currencies.
    """

    all_currencies = await CRUD_currency.get_types(db=db, filter_params=filter_params)

    return all_currencies


@router.get(
    "/",
    response_model=list[schemas.Currency],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
async def get_all_currency(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all currencies.

    Returns a list of all currencies.
    """

    all_currencies = await CRUD_currency.get_currency_from_query(
        db=db, filter_params=filter_params
    )

    return all_currencies


@router.get(
    "/latest_hours/",
    response_model=dict[int, int],
    tags=["latest_hours"],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_latest_hours(
    league_ids: Annotated[list[int], Query(min_length=1)],
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Returns a dict mapping league id to the most recent hour relating to that league. Dict is empty if no currencies exist.

    Does not guarantee an entry for every league id.
    """
    return await CRUD_currency.get_latest_hours(db, league_ids)


@router.get(
    "/price/latest/",
    response_model=list[schemas.Currency],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_latest_currencies(
    league_ids: Annotated[list[int], Query(min_length=1)],
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Returns a list of currencies for all queried leagues (if data exists).
    """
    return await CRUD_currency.get_latest_currencies(db, league_ids)


@router.post(
    "/from_query/",
    response_model=list[schemas.Currency],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_currency_from_query(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    query_list: list[CurrencyQuery],
    db: Session = Depends(get_db),
):
    """
    Returns a list of currencies that match any of the queries
    """
    return await CRUD_currency.get_currency_from_query(db, query_list)


@router.post(
    "/type/",
    response_model=schemas.CurrencyTypeCreate | list[schemas.CurrencyTypeCreate] | None,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_currency_type(
    currency: schemas.CurrencyTypeCreate | list[schemas.CurrencyTypeCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """

    return await CRUD_currency.create_types(
        db=db, obj_in=currency, return_nothing=return_nothing
    )


@router.post(
    "/price/",
    response_model=schemas.CurrencyPriceCreate
    | list[schemas.CurrencyPriceCreate]
    | None,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_currency_price(
    currency: schemas.CurrencyPriceCreate | list[schemas.CurrencyPriceCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of currencies.

    Returns the created currency or list of currencies.
    """

    return await CRUD_currency.create_prices(
        db=db, obj_in=currency, return_nothing=return_nothing
    )


@router.put(
    "/type/",
    response_model=schemas.CurrencyType,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_modifier(
    currencyId: int,
    currency_type_update: schemas.CurrencyTypeUpdate,
    db: Session = Depends(get_db),
):
    currency_type_map = {"currencyId": currencyId}

    currency_type = await CRUD_currency.get_types(
        db=db,
        filter=currency_type_map,
    )

    return await CRUD_currency.update_type(
        db_obj=currency_type, obj_in=currency_type_update, db=db
    )
