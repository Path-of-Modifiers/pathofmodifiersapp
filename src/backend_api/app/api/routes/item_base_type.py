from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_db_obj_already_exists_msg,
    get_delete_return_msg,
)
from app.api.deps import (
    SessionDep,
    get_current_active_superuser,
    get_current_active_user,
)
from app.core.models.models import ItemBaseType
from app.crud import CRUD_itemBaseType

router = APIRouter()


item_base_type_prefix = "itemBaseType"


@router.get(
    "/{baseType}",
    response_model=schemas.ItemBaseType,
    dependencies=[Depends(get_current_active_user)],
)
async def get_item_base_type(baseType: str, db: SessionDep):
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
async def get_all_item_base_types(db: SessionDep):
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
async def get_base_types(db: SessionDep):
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
async def get_unique_categories(
    db: SessionDep,
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
async def get_unique_sub_categories(db: SessionDep):
    """
    Get all unique sub categories.

    Returns a list of all sub categories.
    """

    all_sub_categories = await CRUD_itemBaseType.get_unique_item_sub_categories(db=db)

    return all_sub_categories


@router.post(
    "/",
    response_model=schemas.ItemBaseTypeCreate | list[schemas.ItemBaseTypeCreate],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_item_base_type(
    itemBaseType: schemas.ItemBaseTypeCreate | list[schemas.ItemBaseTypeCreate],
    db: SessionDep,
):
    """
    Create one or a list of new item base types.

    Returns the created item base type or list of item base types.
    """
    db_item_base_type = db.get(ItemBaseType, itemBaseType.baseType)
    if db_item_base_type:
        raise HTTPException(
            status_code=400,
            detail=get_db_obj_already_exists_msg(
                item_base_type_prefix, db_item_base_type.baseType
            ).message,
        )

    return await CRUD_itemBaseType.create(db=db, obj_in=itemBaseType)


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
    db: SessionDep,
):
    """
    Update an item base type by key and value for "baseType".

    Returns the updated item base type.
    """
    db_item_base_type_update = db.get(ItemBaseType, item_base_type_update.baseType)
    if db_item_base_type_update and db_item_base_type_update.baseType != baseType:
        raise HTTPException(
            status_code=400,
            detail=get_db_obj_already_exists_msg(
                item_base_type_prefix, db_item_base_type_update.baseType
            ).message,
        )

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
    db: SessionDep,
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
        model_table_name=ItemBaseType.__tablename__, mapping=item_base_type_map
    ).message
