from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Optional, Union

from app.api.deps import get_db

from app.crud import CRUD_modifier

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{modifierId}",
    response_model=Union[schemas.Modifier, List[schemas.Modifier]],
)
async def get_modifier(
    modifierId: str, position: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Get modifier or list of modifiers by key and 
    value for "modifierId" and optional "position" 
    
    Dominant key is "modifierId".

    Returns one or a list of modifiers.
    """
    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    modifier = await CRUD_modifier.get(db=db, filter=modifier_map)

    return modifier


@router.get("/", response_model=Union[schemas.Modifier, List[schemas.Modifier]])
async def get_all_modifiers(db: Session = Depends(get_db)):
    """
    Get all modifiers.
    
    Returns a list of all modifiers.
    """
    all_modifiers = await CRUD_modifier.get(db=db)

    return all_modifiers


@router.post(
    "/",
    response_model=Union[schemas.ModifierCreate, List[schemas.ModifierCreate]],
)
async def create_modifier(
    modifier: Union[schemas.ModifierCreate, List[schemas.ModifierCreate]],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new modifiers.
    
    Returns the created modifier or list of modifiers.
    """
    return await CRUD_modifier.create(db=db, obj_in=modifier)


@router.put("/{modifierId}", response_model=schemas.Modifier)
async def update_modifier(
    modifierId: int,
    position: int,
    modifier_update: schemas.ModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a modifier by key and value for "modifierId" and "position".
    
    Dominant key is "modifierId".
    
    Returns the updated modifier.
    """
    modifier_map = {"modifierId": modifierId, "position": position}
    modifier = await CRUD_modifier.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_modifier.update(db_obj=modifier, obj_in=modifier_update, db=db)


@router.delete("/{modifierId}", response_model=str)
async def delete_modifier(
    modifierId: int, position: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Delete a modifier by key and value for "modifierId" 
    and optional "position".
    
    Dominant key is "modifierId".
    
    Returns a message that the modifier was deleted.
    Always deletes one modifier.
    """
    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    await CRUD_modifier.remove(db=db, filter=modifier_map)

    return f"Modifier with mapping ({modifier_map}) deleted successfully"
