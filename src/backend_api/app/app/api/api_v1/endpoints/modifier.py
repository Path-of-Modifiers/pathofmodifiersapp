from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Union

from app.api.deps import get_db

from app.crud import CRUD_modifier

import app.core.schemas as schemas

from sqlalchemy.orm import Session

from app.core.security import verification
from app.api.api_v1.utils import get_delete_return_message


router = APIRouter()


modifier_prefix = "modifier"


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


@router.get(
    "/grouped_modifiers_by_effect/",
    response_model=Union[
        schemas.GroupedModifierByEffect, List[schemas.GroupedModifierByEffect]
    ],
)
async def get_grouped_modifier_by_effect(db: Session = Depends(get_db)):
    """
    Get all grouped modifiers by effect.

    Returns a list of all grouped modifiers by effect.
    """
    all_grouped_modifiers_by_effect = (
        await CRUD_modifier.get_grouped_modifier_by_effect(db=db)
    )

    return all_grouped_modifiers_by_effect


@router.post(
    "/",
    response_model=Union[schemas.ModifierCreate, List[schemas.ModifierCreate]],
)
async def create_modifier(
    modifier: Union[schemas.ModifierCreate, List[schemas.ModifierCreate]],
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Create one or a list of new modifiers.

    Returns the created modifier or list of modifiers.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {create_modifier.__name__}",
        )

    return await CRUD_modifier.create(db=db, obj_in=modifier)


@router.put("/{modifierId}", response_model=schemas.Modifier)
async def update_modifier(
    modifierId: int,
    position: int,
    modifier_update: schemas.ModifierUpdate,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Update a modifier by key and value for "modifierId" and "position".

    Dominant key is "modifierId".

    Returns the updated modifier.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {update_modifier.__name__}",
        )

    modifier_map = {"modifierId": modifierId, "position": position}
    modifier = await CRUD_modifier.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_modifier.update(db_obj=modifier, obj_in=modifier_update, db=db)


@router.delete("/{modifierId}", response_model=str)
async def delete_modifier(
    modifierId: int,
    position: Optional[int] = None,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Delete a modifier by key and value for "modifierId"
    and optional "position".

    Dominant key is "modifierId".

    Returns a message that the modifier was deleted.
    Always deletes one modifier.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {delete_modifier.__name__}",
        )

    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    await CRUD_modifier.remove(db=db, filter=modifier_map)

    return get_delete_return_message(modifier_prefix, "modifierId", modifierId)
