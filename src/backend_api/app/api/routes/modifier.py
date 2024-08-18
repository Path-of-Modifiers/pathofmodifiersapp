from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import get_db
from app.api.utils import get_delete_return_message
from app.crud import CRUD_modifier

router = APIRouter()


modifier_prefix = "modifier"


@router.get(
    "/{modifierId}",
    response_model=schemas.Modifier | list[schemas.Modifier],
)
async def get_modifier(
    modifierId: int,
    db: Session = Depends(get_db),
):
    """
    Get modifier or list of modifiers by key and
    value for "modifierId"

    Dominant key is "modifierId".

    Returns one or a list of modifiers.
    """

    modifier_map = {"modifierId": modifierId}
    modifier = await CRUD_modifier.get(db=db, filter=modifier_map)

    return modifier


@router.get("/", response_model=schemas.Modifier | list[schemas.Modifier])
async def get_all_modifiers(
    db: Session = Depends(get_db),
):
    """
    Get all modifiers.

    Returns a list of all modifiers.
    """

    all_modifiers = await CRUD_modifier.get(db=db)

    return all_modifiers


@router.get(
    "/grouped_modifiers_by_effect/",
    response_model=schemas.GroupedModifierByEffect
    | list[schemas.GroupedModifierByEffect],
)
async def get_grouped_modifier_by_effect(
    db: Session = Depends(get_db),
):
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
    response_model=schemas.ModifierCreate | list[schemas.ModifierCreate],
)
async def create_modifier(
    modifier: schemas.ModifierCreate | list[schemas.ModifierCreate],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new modifiers.

    Returns the created modifier or list of modifiers.
    """

    return await CRUD_modifier.create(db=db, obj_in=modifier)


@router.put("/", response_model=schemas.Modifier)
async def update_modifier(
    modifierId: int,
    modifier_update: schemas.ModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a modifier by key and value for "modifierId"

    Dominant key is "modifierId".

    Returns the updated modifier.
    """

    modifier_map = {"modifierId": modifierId}

    modifier = await CRUD_modifier.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_modifier.update(db_obj=modifier, obj_in=modifier_update, db=db)


@router.delete("/{modifierId}", response_model=str)
async def delete_modifier(
    modifierId: int,
    db: Session = Depends(get_db),
):
    """
    Delete a modifier by key and value for "modifierId"

    Returns a message that the modifier was deleted.
    Always deletes one modifier.
    """

    modifier_map = {"modifierId": modifierId}
    await CRUD_modifier.remove(db=db, filter=modifier_map)

    return get_delete_return_message(modifier_prefix, modifier_map)
