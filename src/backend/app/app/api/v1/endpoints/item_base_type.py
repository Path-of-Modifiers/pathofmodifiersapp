from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

import app.api.deps as deps

from app.crud import CRUD_itemBaseType

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{baseType}",
    response_model=Union[schemas.ItemBaseType, List[schemas.ItemBaseType]],
)
async def get_item_base_type(baseType: str, db: Session = Depends(get_db)):
    """
    Get itemBaseType by "baseType".
    """
    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(db=db, filter=item_base_type_map)

    return itemBaseType


@router.get("/", response_model=Union[schemas.ItemBaseType, List[schemas.ItemBaseType]])
async def get_all_item_base_types(db: Session = Depends(get_db)):
    """
    Get all itemBaseTypes.
    """
    all_item_base_types = await CRUD_itemBaseType.get(db=db)

    return all_item_base_types


@router.post(
    "/",
    response_model=Union[schemas.ItemBaseTypeCreate, List[schemas.ItemBaseTypeCreate]],
)
async def create_item_base_type(
    itemBaseType: Union[schemas.ItemBaseTypeCreate, List[schemas.ItemBaseTypeCreate]],
    db: Session = Depends(get_db),
):
    """
    Create a new itemBaseType.
    """
    return await CRUD_itemBaseType.create(db=db, obj_in=itemBaseType)


@router.put("/{baseType}", response_model=schemas.ItemBaseType)
async def update_item_base_type(
    baseType: str,
    item_base_type_update: schemas.ItemBaseTypeUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update an itemBaseType by "baseType".
    """
    item_base_type_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(
        db=db,
        filter=item_base_type_map,
    )

    return await CRUD_itemBaseType.update(
        db_obj=itemBaseType, obj_in=item_base_type_update, db=db
    )


@router.delete("/{baseType}", response_model=str)
async def delete_item_base_type(baseType: str, db: Session = Depends(get_db)):
    """
    Delete an itemBaseType by "baseType".
    """
    item_base_type_map = {"baseType": baseType}
    await CRUD_itemBaseType.remove(db=db, filter=item_base_type_map)

    return f"ItemBaseType with mapping ({item_base_type_map}) deleted successfully"
