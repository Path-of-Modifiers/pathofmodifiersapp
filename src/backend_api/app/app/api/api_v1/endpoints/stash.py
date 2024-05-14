from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

from app.crud import CRUD_stash

import app.core.schemas as schemas

from sqlalchemy.orm import Session

from app.core.security import verification


router = APIRouter()


@router.get(
    "/{stashId}",
    response_model=Union[schemas.Stash, List[schemas.Stash]],
)
async def get_stash(stashId: str, db: Session = Depends(get_db)):
    """
    Get stash by key and value for "stashId".

    Always returns one stash.
    """
    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(db=db, filter=stash_map)

    return stash


@router.get("/", response_model=Union[schemas.Stash, List[schemas.Stash]])
async def get_all_stashes(db: Session = Depends(get_db)):
    """
    Get all stashes.

    Returns a list of all stashes.
    """
    all_stashes = await CRUD_stash.get(db=db)

    return all_stashes


@router.post(
    "/",
    response_model=Union[schemas.StashCreate, List[schemas.StashCreate]],
)
async def create_stash(
    stash: Union[schemas.StashCreate, List[schemas.StashCreate]],
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Create one or a list of new stashes.

    Returns the created stash or list of stashes.
    """
    if not verification:
        return f"Unauthorized to access API in {create_stash.__name__}"

    return await CRUD_stash.create(db=db, obj_in=stash)


@router.put("/{stashId}", response_model=schemas.Stash)
async def update_stash(
    stashId: str,
    stash_update: schemas.StashUpdate,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Update a stash by key and value for "stashId".

    Returns the updated stash.
    """
    if not verification:
        return f"Unauthorized to access API in {update_stash.__name__}"

    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(
        db=db,
        filter=stash_map,
    )

    return await CRUD_stash.update(db_obj=stash, obj_in=stash_update, db=db)


@router.delete("/{stashId}", response_model=str)
async def delete_stash(
    stashId: str,
    db: Session = Depends(get_db),
    verification: bool = Depends(verification),
):
    """
    Delete a stash by key and value for "stashId".

    Returns a message that the stash was deleted successfully.
    Always deletes one stash.
    """
    if not verification:
        return f"Unauthorized to access API in {delete_stash.__name__}"

    stash_map = {"stashId": stashId}
    await CRUD_stash.remove(db=db, filter=stash_map)

    return f"Stash with mapping ({stash_map}) deleted successfully"
