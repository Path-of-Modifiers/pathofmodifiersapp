from typing import Annotated

import backend_api.app.core.schemas as schemas
from backend_api.app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from backend_api.app.api.params import FilterParams
from backend_api.app.crud import CRUD_itemAvailability
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

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
