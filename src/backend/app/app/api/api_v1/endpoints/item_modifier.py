from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Optional, Union

from app.api.deps import get_db

from app.crud import CRUD_itemModifier

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{itemId}",
    response_model=Union[schemas.ItemModifier, List[schemas.ItemModifier]],
)
async def get_item_modifier(
    itemId: int,
    modifierId: Optional[int] = None,
    position: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Get item modifier or list of item modifiers by key and 
    value for "itemId", optional "modifierId" and optional "position".

    Returns one or a list of item modifiers.
    """
    itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if position is not None:
        itemModifier_map["position"] = position

    itemModifier = await CRUD_itemModifier.get(db=db, filter=itemModifier_map)
    return itemModifier


@router.get("/", response_model=Union[schemas.ItemModifier, List[schemas.ItemModifier]])
async def get_all_item_modifiers(db: Session = Depends(get_db)):
    """
    Get all item modifiers.
    
    Returns a list of all item modifiers.
    """
    all_itemModifiers = await CRUD_itemModifier.get(db=db)

    return all_itemModifiers


@router.post(
    "/",
    response_model=Union[schemas.ItemModifierCreate, List[schemas.ItemModifierCreate]],
)
async def create_item_modifier(
    itemModifier: Union[schemas.ItemModifierCreate, List[schemas.ItemModifierCreate]],
    db: Session = Depends(get_db),
):
    """
    Create one or a list item modifiers.
    
    Returns the created item modifier or list of item modifiers.
    """
    return await CRUD_itemModifier.create(db=db, obj_in=itemModifier)


@router.put("/item={itemId}", response_model=schemas.ItemModifier)
async def update_item_modifier(
    itemId: int,
    modifierId: int,
    position: int,
    itemModifier_update: schemas.ItemModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an item modifier by key and value for 
    "itemId", optional "modifierId" and optional "position".

    Returns the updated item modifier.
    """
    itemModifier_map = {
        "itemId": itemId,
        "modifierId": modifierId,
        "position": position,
    }
    itemModifier = await CRUD_itemModifier.get(
        db=db,
        filter=itemModifier_map,
    )

    return await CRUD_itemModifier.update(
        db_obj=itemModifier, obj_in=itemModifier_update, db=db
    )


@router.delete("/item={itemId}")
async def delete_item_modifier(
    itemId: int,
    modifierId: Optional[int] = None,
    position: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Delete an item modifier by key and value for 
    "itemId", optional "modifierId" and optional "position".
    
    Returns a message that the item modifier was deleted successfully.
    Always deletes one item modifier.
    """
    itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if position is not None:
        itemModifier_map["position"] = position

    await CRUD_itemModifier.remove(db=db, filter=itemModifier_map)

    return f"ItemModifier with mapping ({itemModifier_map}) was deleted successfully"
