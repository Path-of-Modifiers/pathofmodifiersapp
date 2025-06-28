from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.api.params import FilterParams
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_user_rate_limits
from app.crud import CRUD_unidentifiedItem

router = APIRouter()


unidentified_item_prefix = "unidentifiedItem"


@router.get(
    "/latest_item_id/",
    response_model=int | None,
    tags=["latest_item_id"],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_latest_item_id(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Get the latest "itemId"

    Can only be used safely on an empty table or directly after an insertion.
    """

    result = db.execute(
        text("""SELECT MAX("itemId") FROM unidentified_item""")
    ).fetchone()
    if not result or not result[0]:
        return None

    return int(result[0])


@router.get(
    "/",
    response_model=schemas.UnidentifiedItem | list[schemas.UnidentifiedItem],
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

    all_items = await CRUD_unidentifiedItem.get(db=db, filter_params=filter_params)

    return all_items


@router.post(
    "/",
    response_model=schemas.UnidentifiedItemCreate
    | list[schemas.UnidentifiedItemCreate]
    | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_item(
    item: schemas.UnidentifiedItemCreate | list[schemas.UnidentifiedItemCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new items.

    Returns the created item or list of items.
    """

    return await CRUD_unidentifiedItem.create(
        db=db, obj_in=item, return_nothing=return_nothing
    )
