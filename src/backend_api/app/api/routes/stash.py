from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

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
from app.core.models.models import Stash
from app.crud import CRUD_stash
from app.limiter import apply_user_rate_limits

router = APIRouter()


stash_prefix = "stash"


@router.get(
    "/{stashId}",
    response_model=schemas.Stash,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_stash(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    stashId: str,
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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
