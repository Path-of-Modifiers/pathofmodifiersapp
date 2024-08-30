from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from app.core.models.models import ItemModifier
from app.crud import CRUD_itemModifier

router = APIRouter()


item_modifier_prefix = "itemModifier"


@router.get(
    "/{itemId}",
    response_model=schemas.ItemModifier | list[schemas.ItemModifier],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_item_modifier(
    itemId: int,
    db: Session = Depends(get_db),
    modifierId: int | None = None,
    position: int | None = None,
):
    """
    Get item modifier or list of item modifiers by key and
    value for "itemId", optional "modifierId" and optional "position".

    Dominant key is "itemId".

    Returns one or a list of item modifiers.
    """

    itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if position is not None:
        itemModifier_map["position"] = position

    itemModifier = await CRUD_itemModifier.get(db=db, filter=itemModifier_map)
    return itemModifier


@router.get(
    "/",
    response_model=schemas.ItemModifier | list[schemas.ItemModifier],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_item_modifiers(
    db: Session = Depends(get_db),
):
    """
    Get all item modifiers.

    Returns a list of all item modifiers.
    """

    all_itemModifiers = await CRUD_itemModifier.get(db=db)

    return all_itemModifiers


@router.post(
    "/",
    response_model=schemas.ItemModifierCreate | list[schemas.ItemModifierCreate],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_item_modifier(
    itemModifier: schemas.ItemModifierCreate | list[schemas.ItemModifierCreate],
    db: Session = Depends(get_db),
):
    """
    Create one or a list item modifiers.

    Returns the created item modifier or list of item modifiers.
    """

    return await CRUD_itemModifier.create(db=db, obj_in=itemModifier)


@router.put(
    "/",
    response_model=schemas.ItemModifier,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def update_item_modifier(
    itemId: int,
    modifierId: int,
    itemModifier_update: schemas.ItemModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an item modifier by key and value for
    "itemId", optional "modifierId" and optional "position".

    Dominant key is "itemId".

    Returns the updated item modifier.
    """

    itemModifier_map = {
        "itemId": itemId,
        "modifierId": modifierId,
    }
    itemModifier = await CRUD_itemModifier.get(
        db=db,
        filter=itemModifier_map,
    )

    return await CRUD_itemModifier.update(
        db_obj=itemModifier, obj_in=itemModifier_update, db=db
    )


@router.delete(
    "/{itemId}",
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_item_modifier(
    itemId: int,
    db: Session = Depends(get_db),
    modifierId: int | None = None,
):
    """
    Delete an item modifier by key and value for
    "itemId", optional "modifierId" and optional "position".

    Dominant key is "itemId".

    Returns a message that the item modifier was deleted successfully.
    Always deletes one item modifier.
    """

    itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId

    await CRUD_itemModifier.remove(db=db, filter=itemModifier_map)

    return get_delete_return_msg(
        model_table_name=ItemModifier.__tablename__, filter=itemModifier_map
    ).message
