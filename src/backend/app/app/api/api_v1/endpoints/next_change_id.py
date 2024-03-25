from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_next_change_id

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{nextChangeId}",
    response_model=Union[schemas.NextChangeId, List[schemas.NextChangeId]],
)
async def get_next_change_id(nextChangeId: str, db: Session = Depends(get_db)):
    """
    Get the next_change_id by mapping with key and value for "nextChangeId" .

    Always returns one next_change_id.
    """
    next_change_id_map = {"nextChangeId": nextChangeId}
    next_change_id = await CRUD_next_change_id.get(db=db, filter=next_change_id_map)

    return next_change_id


@router.get("/", response_model=Union[schemas.NextChangeId, List[schemas.NextChangeId]])
async def get_all_next_change_ids(db: Session = Depends(get_db)):
    """
    Get all next_change_ids.

    Returns a list of all next_change_ids.
    """
    all_next_change_ids = await CRUD_next_change_id.get(db=db)

    return all_next_change_ids


@router.post(
    "/",
    response_model=Union[schemas.NextChangeIdCreate, List[schemas.NextChangeIdCreate]],
)
async def create_next_change_id(
    next_change_id: Union[schemas.NextChangeIdCreate, List[schemas.NextChangeIdCreate]],
    db: Session = Depends(get_db),
):
    """
    Create one or a list of next_change_ids.

    Returns the created next_change_id or list of next_change_ids.
    """
    return await CRUD_next_change_id.create(db=db, obj_in=next_change_id)


@router.put("/{nextChangeId}", response_model=schemas.NextChangeId)
async def update_next_change_id(
    nextChangeId: str,
    next_change_id_update: schemas.NextChangeIdUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an next_change_id by key and value for "nextChangeId".

    Returns the updated next_change_id.
    """
    next_change_id_map = {"nextChangeId": nextChangeId}
    next_change_id = await CRUD_next_change_id.get(
        db=db,
        filter=next_change_id_map,
    )

    return await CRUD_next_change_id.update(
        db_obj=next_change_id, obj_in=next_change_id_update, db=db
    )


@router.delete("/{nextChangeId}", response_model=str)
async def delete_next_change_id(nextChangeId: str, db: Session = Depends(get_db)):
    """
    Delete an next_change_id by key and value "nextChangeId".

    Returns a message indicating the next_change_id was deleted.
    Always deletes one next_change_id.
    """
    next_change_id_map = {"nextChangeId": nextChangeId}
    await CRUD_next_change_id.remove(db=db, filter=next_change_id_map)

    return f"NextChangeId with mapping ({next_change_id_map}) deleted successfully"
