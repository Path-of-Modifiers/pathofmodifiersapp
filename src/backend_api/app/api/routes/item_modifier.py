from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

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
    itemId: int | None = None,
    modifierId: int | None = None,
    orderId: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Get item modifier or list of item modifiers by key and
    value for optional "itemId", optional "modifierId" and optional "orderId".
    One key must be provided.

    Returns one or a list of item modifiers.
    """

    if itemId is None and modifierId is None and orderId is None:
        # Needs to be changed to custom exception
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Please provide at least one key.",
        )
    if itemId is not None:
        itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if orderId is not None:
        itemModifier_map["orderId"] = orderId

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
    orderId: int,
    itemModifier_update: schemas.ItemModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an item modifier by key and value for
    "itemId", "modifierId" and "orderId".

    Returns the updated item modifier.
    """

    itemModifier_map = {
        "itemId": itemId,
        "modifierId": modifierId,
        "orderId": orderId,
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
    modifierId: int | None = None,
    orderId: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Delete an item modifier by key and value for "itemId", optional "modifierId" and optional "orderId".

    Can delete multiple item modifiers one one request if not modifierId or orderId is provided.

    Dominant key is "itemId".

    Returns a message that the item modifier was deleted successfully.
    """

    itemModifier_map = {"itemId": itemId}
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if orderId is not None:
        itemModifier_map["orderId"] = orderId

    await CRUD_itemModifier.remove(db=db, filter=itemModifier_map)

    return get_delete_return_msg(
        model_table_name=ItemModifier.__tablename__, filter=itemModifier_map
    ).message
