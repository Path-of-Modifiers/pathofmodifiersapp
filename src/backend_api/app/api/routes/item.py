from typing import Annotated

import backend_api.app.core.schemas as schemas
from backend_api.app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from backend_api.app.api.params import FilterParams
from backend_api.app.crud import CRUD_item
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()


item_prefix = "item"


@router.get(
    "/",
    response_model=schemas.Item | list[schemas.Item],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_items(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all items.

    Returns a list of all items.
    """

    all_items = await CRUD_item.get(db=db, filter_params=filter_params)

    return all_items


@router.post(
    "/",
    response_model=list[schemas.Item],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_item(
    items: list[schemas.ItemCreate],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new items.

    Returns the created item or list of items.
    """

    return await CRUD_item.create_items(db=db, new_items=items)


@router.patch(
    "/availability/",
    response_model=list[schemas.ItemAvailability],
    dependencies=[Depends(get_current_active_superuser)],
)
async def patch_expired_availability(
    expired_availability: list[schemas.ItemAvailabilityExpired],
    db: Session = Depends(get_db),
):
    return await CRUD_item.patch_expired_availability(
        db, expired_availability=expired_availability
    )


@router.put(
    "/availability/",
    response_model=list[schemas.ItemAvailability],
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_availability(
    updated_availability: list[schemas.ItemAvailabilityUpdated],
    db: Session = Depends(get_db),
):
    return await CRUD_item.update_availability(
        db, updated_availability=updated_availability
    )
