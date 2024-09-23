from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.core.models.models import ItemBaseType
from app.crud import CRUD_itemBaseType
from app.limiter import apply_user_rate_limits

router = APIRouter()


item_base_type_prefix = "itemBaseType"


@router.get(
    "/{baseType}",
    response_model=schemas.ItemBaseType,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_item_base_type(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    baseType: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get item base type by key and value for "baseType".

    Always returns one item base type.
    """

    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(db=db, filter=item_base_type_map)

    return itemBaseType


@router.get(
    "/",
    response_model=schemas.ItemBaseType | list[schemas.ItemBaseType],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_item_base_types(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: AsyncSession = Depends(get_db),
):
    """
    Get all item base types.

    Returns a list of all item base types.
    """

    all_item_base_types = await CRUD_itemBaseType.get(db=db)

    return all_item_base_types


@router.get(
    "/baseTypes/",
    response_model=schemas.BaseType | list[schemas.BaseType],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_base_types(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all base types.

    Returns a list of all base types.
    """
    all_base_types = await CRUD_itemBaseType.get_base_types(db=db)

    return all_base_types


@router.get(
    "/uniqueCategories/",
    response_model=schemas.ItemBaseTypeCategory | list[schemas.ItemBaseTypeCategory],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_unique_categories(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: AsyncSession = Depends(get_db),
):
    """
    Get all unique categories.

    Returns a list of all categories.
    """

    all_categories = await CRUD_itemBaseType.get_unique_item_categories(db=db)

    return all_categories


@router.get(
    "/uniqueSubCategories/",
    response_model=schemas.ItemBaseTypeSubCategory
    | list[schemas.ItemBaseTypeSubCategory],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_unique_sub_categories(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all unique sub categories.

    Returns a list of all sub categories.
    """

    all_sub_categories = await CRUD_itemBaseType.get_unique_item_sub_categories(db=db)

    return all_sub_categories


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
    db: AsyncSession = Depends(get_db),
):
    """
    Create one or a list of new item base types.

    Returns the created item base type or list of item base types.
    """
    return await CRUD_itemBaseType.create(
        db=db,
        obj_in=itemBaseType,
        on_duplicate_pkey_do_nothing=on_duplicate_pkey_do_nothing,
    )


@router.put(
    "/{baseType}",
    response_model=schemas.ItemBaseType,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def update_item_base_type(
    baseType: str,
    item_base_type_update: schemas.ItemBaseTypeUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an item base type by key and value for "baseType".

    Returns the updated item base type.
    """
    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(
        db=db,
        filter=item_base_type_map,
    )

    return await CRUD_itemBaseType.update(
        db_obj=itemBaseType, obj_in=item_base_type_update, db=db
    )


@router.delete(
    "/{baseType}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_item_base_type(
    baseType: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an item base type by key and value for "baseType".

    Returns a message that the item base type was deleted successfully.
    Always deletes one item base type.
    """

    item_base_type_map = {"baseType": baseType}
    await CRUD_itemBaseType.remove(
        db=db,
        filter=item_base_type_map,
    )

    return get_delete_return_msg(
        model_table_name=ItemBaseType.__tablename__, filter=item_base_type_map
    ).message
