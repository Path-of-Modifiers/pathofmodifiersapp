from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_item

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{itemId}",
    response_model=Union[schemas.Item, List[schemas.Item]],
)
async def get_item(itemId: str, db: Session = Depends(get_db)):
    """
    Get item by key and value for "itemId".

    Always returns one item.
    """
    item_map = {"itemId": itemId}
    item = await CRUD_item.get(db=db, filter=item_map)

    return item


@router.get("/latest_item_id/", response_model=int, tags=["latest_item_id"])
async def get_latest_item_id(db: Session = Depends(get_db)):
    """
    TODO
    """
    all_items = await CRUD_item.get(db=db)

    return len(all_items)


@router.get("/", response_model=Union[schemas.Item, List[schemas.Item]])
async def get_all_items(db: Session = Depends(get_db)):
    """
    Get all items.

    Returns a list of all items.
    """
    all_items = await CRUD_item.get(db=db)

    return all_items


@router.post(
    "/",
    response_model=Union[schemas.ItemCreate, List[schemas.ItemCreate]],
)
async def create_item(
    item: Union[schemas.ItemCreate, List[schemas.ItemCreate]],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new items.

    Returns the created item or list of items.
    """
    return await CRUD_item.create(db=db, obj_in=item)


@router.put("/{itemId}", response_model=schemas.Item)
async def update_item(
    itemId: str,
    item_update: schemas.ItemUpdate,
    db: Session = Depends(get_db),
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


@router.delete("/{itemId}", response_model=str)
async def delete_item(itemId: str, db: Session = Depends(get_db)):
    """
    Delete an item by key and value for "itemId".

    Returns a message indicating the item was deleted.
    Always deletes one item.
    """
    item_map = {"itemId": itemId}
    await CRUD_item.remove(db=db, filter=item_map)

    return f"Item with mapping ({item_map}) deleted successfully"
