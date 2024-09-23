from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.core.config import settings
from app.core.models.models import Item
from app.crud import CRUD_item
from app.limiter import apply_user_rate_limits

router = APIRouter()


item_prefix = "item"


@router.get(
    "/{itemId}",
    response_model=schemas.Item,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_item(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    itemId: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get item by key and value for "itemId".

    Always returns one item.
    """

    item_map = {"itemId": itemId}
    item = await CRUD_item.get(db=db, filter=item_map)

    return item


@router.get(
    "/latest_item_id/",
    response_model=int | None,
    tags=["latest_item_id"],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_latest_item_id(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: AsyncSession = Depends(get_db),
):
    """
    Get the latest "itemId"

    Can only be used safely on an empty table or directly after an insertion.
    """

    result = await db.execute(text("""SELECT MAX("itemId") FROM item"""))
    item_id = result.fetchone()
    if not item_id or not item_id[0]:
        return None

    return int(item_id[0])


@router.get(
    "/",
    response_model=schemas.Item | list[schemas.Item],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_items(
    db: AsyncSession = Depends(get_db),
):
    """
    Get all items.

    Returns a list of all items.
    """

    all_items = await CRUD_item.get(db=db)

    return all_items


@router.post(
    "/",
    response_model=schemas.ItemCreate | list[schemas.ItemCreate],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_item(
    item: schemas.ItemCreate | list[schemas.ItemCreate],
    db: AsyncSession = Depends(get_db),
):
    """
    Create one or a list of new items.

    Returns the created item or list of items.
    """

    return await CRUD_item.create(db=db, obj_in=item)


@router.put(
    "/{itemId}",
    response_model=schemas.Item,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_item(
    itemId: int,
    item_update: schemas.ItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an item by key and value for "itemId".

    Returns the updated item.
    """

    item_map = {"itemId": itemId}
    item = await CRUD_item.get(
        db=db,
        filter=item_map,
    )

    return await CRUD_item.update(db_obj=item, obj_in=item_update, db=db)


@router.delete(
    "/{itemId}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_item(
    itemId: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an item by key and value for "itemId".

    Returns a message indicating the item was deleted.
    Always deletes one item.
    """
    item_map = {"itemId": itemId}
    await CRUD_item.remove(db=db, filter=item_map)

    return get_delete_return_msg(
        model_table_name=Item.__tablename__, filter=item_map
    ).message
