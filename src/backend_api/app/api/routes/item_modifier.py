from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from app.api.params import FilterParams
from app.crud import CRUD_itemModifier

router = APIRouter()


item_modifier_prefix = "itemModifier"


@router.get(
    "/",
    response_model=schemas.ItemModifier | list[schemas.ItemModifier],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_item_modifiers(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all item modifiers.

    Returns a list of all item modifiers.
    """

    all_itemModifiers = await CRUD_itemModifier.get(db=db, filter_params=filter_params)

    return all_itemModifiers


@router.post(
    "/",
    response_model=schemas.ItemModifierCreate | list[schemas.ItemModifierCreate] | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_item_modifier(
    itemModifier: schemas.ItemModifierCreate | list[schemas.ItemModifierCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list item modifiers.

    Returns the created item modifier or list of item modifiers.
    """

    return await CRUD_itemModifier.create(
        db=db,
        obj_in=itemModifier,
        return_nothing=return_nothing,
    )
