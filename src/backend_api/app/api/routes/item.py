from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import get_db
from app.api.utils import get_delete_return_message
from app.core.security import verification
from app.crud import CRUD_item

router = APIRouter()


item_prefix = "item"


@router.get(
    "/{itemId}",
    response_model=schemas.Item | list[schemas.Item],
)
async def get_item(
    itemId: int,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Get item by key and value for "itemId".

    Always returns one item.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {get_item.__name__}",
        )

    item_map = {"itemId": itemId}
    item = await CRUD_item.get(db=db, filter=item_map)

    return item


@router.get("/latest_item_id/", response_model=int, tags=["latest_item_id"])
async def get_latest_item_id(
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Get the latest "itemId"

    Can only be used safely on an empty table or directly after an insertion.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {get_latest_item_id.__name__}",
        )

    result = db.execute(text("""SELECT MAX("itemId") FROM item""")).fetchone()
    if result:
        return int(result[0])
    else:
        return 1


@router.get("/", response_model=schemas.Item | list[schemas.Item])
async def get_all_items(
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Get all items.

    Returns a list of all items.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {get_all_items.__name__}",
        )

    all_items = await CRUD_item.get(db=db)

    return all_items


@router.post(
    "/",
    response_model=schemas.ItemCreate | list[schemas.ItemCreate],
)
async def create_item(
    item: schemas.ItemCreate | list[schemas.ItemCreate],
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Create one or a list of new items.

    Returns the created item or list of items.
    """
    if not verification:
        return HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {create_item.__name__}",
        )

    return await CRUD_item.create(db=db, obj_in=item)


@router.put("/{itemId}", response_model=schemas.Item)
async def update_item(
    itemId: int,
    item_update: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Update an item by key and value for "itemId".

    Returns the updated item.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {update_item.__name__}",
        )

    item_map = {"itemId": itemId}
    item = await CRUD_item.get(
        db=db,
        filter=item_map,
    )

    return await CRUD_item.update(db_obj=item, obj_in=item_update, db=db)


@router.delete("/{itemId}", response_model=str)
async def delete_item(
    itemId: int,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Delete an item by key and value for "itemId".

    Returns a message indicating the item was deleted.
    Always deletes one item.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized API access for {delete_item.__name__}",
        )

    item_map = {"itemId": itemId}
    await CRUD_item.remove(db=db, filter=item_map)

    return get_delete_return_message(item_prefix, item_map)
