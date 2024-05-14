from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_itemBaseType

import app.core.schemas as schemas

from sqlalchemy.orm import Session

from app.core.security import verification


router = APIRouter()


@router.get(
    "/{baseType}",
    response_model=Union[schemas.ItemBaseType, List[schemas.ItemBaseType]],
)
async def get_item_base_type(baseType: str, db: Session = Depends(get_db)):
    """
    Get item base type by key and value for "baseType".

    Always returns one item base type.
    """
    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(db=db, filter=item_base_type_map)

    return itemBaseType


@router.get("/", response_model=Union[schemas.ItemBaseType, List[schemas.ItemBaseType]])
async def get_all_item_base_types(db: Session = Depends(get_db)):
    """
    Get all item base types.

    Returns a list of all item base types.
    """
    all_item_base_types = await CRUD_itemBaseType.get(db=db)

    return all_item_base_types


@router.get(
    "/baseTypes/", response_model=Union[schemas.BaseType, List[schemas.BaseType]]
)
async def get_base_types(db: Session = Depends(get_db)):
    """
    Get all base types.

    Returns a list of all base types.
    """
    all_base_types = await CRUD_itemBaseType.get_base_types(db=db)

    return all_base_types


@router.get(
    "/uniqueCategories/",
    response_model=Union[
        schemas.ItemBaseTypeCategory, List[schemas.ItemBaseTypeCategory]
    ],
)
async def get_unique_categories(db: Session = Depends(get_db)):
    """
    Get all unique categories.

    Returns a list of all categories.
    """
    all_categories = await CRUD_itemBaseType.get_unique_item_categories(db=db)

    return all_categories


@router.get(
    "/uniqueSubCategories/",
    response_model=Union[
        schemas.ItemBaseTypeSubCategory, List[schemas.ItemBaseTypeSubCategory]
    ],
)
async def get_unique_sub_categories(db: Session = Depends(get_db)):
    """
    Get all unique sub categories.

    Returns a list of all sub categories.
    """
    all_sub_categories = await CRUD_itemBaseType.get_unique_item_sub_categories(db=db)

    return all_sub_categories


@router.post(
    "/",
    response_model=Union[schemas.ItemBaseTypeCreate, List[schemas.ItemBaseTypeCreate]],
)
async def create_item_base_type(
    itemBaseType: Union[schemas.ItemBaseTypeCreate, List[schemas.ItemBaseTypeCreate]],
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Create one or a list of new item base types.

    Returns the created item base type or list of item base types.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {create_item_base_type.__name__}",
        )

    return await CRUD_itemBaseType.create(db=db, obj_in=itemBaseType)


@router.put("/{baseType}", response_model=schemas.ItemBaseType)
async def update_item_base_type(
    baseType: str,
    item_base_type_update: schemas.ItemBaseTypeUpdate,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Update an item base type by key and value for "baseType".

    Returns the updated item base type.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {update_item_base_type.__name__}",
        )

    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(
        db=db,
        filter=item_base_type_map,
    )

    return await CRUD_itemBaseType.update(
        db_obj=itemBaseType, obj_in=item_base_type_update, db=db
    )


@router.delete("/{baseType}", response_model=str)
async def delete_item_base_type(
    baseType: str,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Delete an item base type by key and value for "baseType".

    Returns a message that the item base type was deleted successfully.
    Always deletes one item base type.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {delete_item_base_type.__name__}",
        )

    item_base_type_map = {"baseType": baseType}
    await CRUD_itemBaseType.remove(db=db, filter=item_base_type_map)

    return f"Ttem base type with mapping ({item_base_type_map}) deleted successfully"
