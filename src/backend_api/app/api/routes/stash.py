from __future__ import annotations

from fastapi import APIRouter, Depends

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    SessionDep,
    get_current_active_superuser,
    get_current_active_user,
)
from app.core.models.models import Stash
from app.crud import CRUD_stash

router = APIRouter()


stash_prefix = "stash"


@router.get(
    "/{stashId}",
    response_model=schemas.Stash,
    dependencies=[Depends(get_current_active_user)],
)
async def get_stash(
    stashId: str,
    db: SessionDep,
):
    """
    Get stash by key and value for "stashId".

    Always returns one stash.
    """

    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(db=db, filter=stash_map)

    return stash


@router.get(
    "/",
    response_model=schemas.Stash | list[schemas.Stash],
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_all_stashes(
    db: SessionDep,
):
    """
    Get all stashes.

    Returns a list of all stashes.
    """

    all_stashes = await CRUD_stash.get(db=db)

    return all_stashes


@router.post(
    "/",
    response_model=schemas.StashCreate | list[schemas.StashCreate],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_stash(
    stash: schemas.StashCreate | list[schemas.StashCreate],
    db: SessionDep,
):
    """
    Create one or a list of new stashes.

    Returns the created stash or list of stashes.
    """

    return await CRUD_stash.create(db=db, obj_in=stash)


@router.put(
    "/{stashId}",
    response_model=schemas.Stash,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_stash(
    stashId: str,
    stash_update: schemas.StashUpdate,
    db: SessionDep,
):
    """
    Update a stash by key and value for "stashId".

    Returns the updated stash.
    """

    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(
        db=db,
        filter=stash_map,
    )

    return await CRUD_stash.update(db_obj=stash, obj_in=stash_update, db=db)


@router.delete(
    "/{stashId}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_stash(
    stashId: str,
    db: SessionDep,
):
    """
    Delete a stash by key and value for "stashId".

    Returns a message that the stash was deleted successfully.
    Always deletes one stash.
    """

    stash_map = {"stashId": stashId}
    await CRUD_stash.remove(db=db, filter=stash_map)

    return get_delete_return_msg(
        model_table_name=Stash.__tablename__, filter=stash_map
    ).message
