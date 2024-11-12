from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
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
from app.api.params import FilterParams
from app.core.models.models import ItemBaseType
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from app.crud import CRUD_itemBaseType

router = APIRouter()


item_base_type_prefix = "itemBaseType"


@router.get(
    "/{itemBaseTypeId}",
    response_model=schemas.ItemBaseType,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_item_base_type(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    itemBaseTypeId: str,
    db: Session = Depends(get_db),
):
    """
    Get item base type by key and value for "itemBaseTypeId".

    Always returns one item base type.
    """

    item_base_type_map = {"itemBaseTypeId": itemBaseTypeId}
    itemBaseType = await CRUD_itemBaseType.get(db=db, filter=item_base_type_map)

    return itemBaseType


@router.get(
    "/",
    response_model=schemas.ItemBaseType | list[schemas.ItemBaseType],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_item_base_types(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all item base types.

    Returns a list of all item base types.
    """

    all_item_base_types = await CRUD_itemBaseType.get(
        db=db, filter_params=filter_params
    )

    return all_item_base_types


@router.post(
    "/",
    response_model=schemas.ItemBaseTypeCreate | list[schemas.ItemBaseTypeCreate] | None,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_item_base_type(
    itemBaseType: schemas.ItemBaseTypeCreate | list[schemas.ItemBaseTypeCreate],
    on_duplicate_pkey_do_nothing: bool | None = None,
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new item base types.

    Returns the created item base type or list of item base types.
    """
    return await CRUD_itemBaseType.create(
        db=db,
        obj_in=itemBaseType,
        on_duplicate_pkey_do_nothing=on_duplicate_pkey_do_nothing,
        on_conflict_constraint=f"{ItemBaseType.__tablename__}_baseType_key",  # REF:"item_base_type_baseType_key" UNIQUE CONSTRAINT, btree ("baseType")
        return_nothing=return_nothing,
    )


@router.put(
    "/{itemBaseTypeId}",
    response_model=schemas.ItemBaseType,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def update_item_base_type(
    itemBaseTypeId: int,
    item_base_type_update: schemas.ItemBaseTypeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an item base type by key and value for "itemBaseTypeId".

    Returns the updated item base type.
    """
    item_base_type_map = {"itemBaseTypeId": itemBaseTypeId}
    itemBaseType = await CRUD_itemBaseType.get(
        db=db,
        filter=item_base_type_map,
    )

    return await CRUD_itemBaseType.update(
        db_obj=itemBaseType, obj_in=item_base_type_update, db=db
    )


@router.delete(
    "/{itemBaseTypeId}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_item_base_type(
    itemBaseTypeId: int,
    db: Session = Depends(get_db),
):
    """
    Delete an item base type by key and value for "itemBaseTypeId".

    Returns a message that the item base type was deleted successfully.
    Always deletes one item base type.
    """

    item_base_type_map = {"itemBaseTypeId": itemBaseTypeId}
    await CRUD_itemBaseType.remove(
        db=db,
        filter=item_base_type_map,
    )

    return get_delete_return_msg(
        model_table_name=ItemBaseType.__tablename__, filter=item_base_type_map
    ).message
