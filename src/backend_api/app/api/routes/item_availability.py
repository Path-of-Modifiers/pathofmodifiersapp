from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from app.api.params import FilterParams
from app.crud import CRUD_itemAvailability

router = APIRouter()


item_availability_prefix = "itemAvailability"


@router.get(
    "/",
    response_model=schemas.ItemAvailability | list[schemas.ItemAvailability],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_item_modifiers(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all available items.

    Returns a list of all available items.
    """

    all_item_availability = await CRUD_itemAvailability.get(
        db=db, filter_params=filter_params
    )

    return all_item_availability
