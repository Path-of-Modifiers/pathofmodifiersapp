from typing import Annotated

from backend_api.app.api.api_message_util import (
    get_delete_return_msg,
)
from backend_api.app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from backend_api.app.api.params import FilterParams
from backend_api.app.core.models.models import UniqueItem
from backend_api.app.core.rate_limit.rate_limit_config import rate_limit_settings
from backend_api.app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from backend_api.app.crud import CRUD_uniqueItem
from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

import app.core.schemas as schemas

router = APIRouter()


unique_item_prefix = "uniqueItem"


@router.get(
    "/{uniqueItemId}",
    response_model=schemas.UniqueItem | list[schemas.UniqueItem],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_unique(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    uniqueItemId: int,
    db: Session = Depends(get_db),
):
    """
    Get unique or list of uniques by key and
    value for "uniqueItemId"

    Dominant key is "uniqueItemId".

    Returns one or a list of uniques.
    """

    unique_map = {"uniqueItemId": uniqueItemId}
    unique = await CRUD_uniqueItem.get(db=db, filter=unique_map)

    return unique


@router.get(
    "/",
    response_model=schemas.UniqueItem | list[schemas.UniqueItem],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_uniques(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all uniques.

    Returns a list of all uniques.
    """

    all_uniques = await CRUD_uniqueItem.get(db=db, filter_params=filter_params)

    return all_uniques


@router.post(
    "/",
    response_model=list[schemas.UniqueItem],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_unique(
    uniques: list[schemas.UniqueItemCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create a list of new uniques.
    """

    return await CRUD_uniqueItem.create(
        db=db, obj_in=uniques, return_nothing=return_nothing
    )


@router.put(
    "/{uniqueItemId}",
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_unique(
    uniqueItemId: int,
    unique_item_update: schemas.UniqueItemUpdate,
    db: Session = Depends(get_db),
):
    """
    Returns the updated unique.
    """

    unique_item_map = {"uniqueItemId": uniqueItemId}

    unique_item = await CRUD_uniqueItem.get(
        db=db,
        filter=unique_item_map,
    )

    return await CRUD_uniqueItem.update(
        db_obj=unique_item, obj_in=unique_item_update, db=db
    )


@router.delete(
    "/",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_unique(
    uniqueItemId: int,
    db: Session = Depends(get_db),
):
    """
    Delete a unique by key and value for "uniqueItemId"

    Returns a message that the unique was deleted.
    Always deletes one unique.
    """

    unique_map = {"uniqueItemId": uniqueItemId}
    await CRUD_uniqueItem.remove(db=db, filter=unique_map)

    return get_delete_return_msg(
        model_table_name=UniqueItem.__tablename__, filter=unique_map
    ).message
