from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
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
from app.api.params import FilterParams
from app.core.models.models import Stash
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_user_rate_limits
from app.crud import CRUD_stash

router = APIRouter()


stash_prefix = "stash"


@router.get(
    "/{stashId}",
    response_model=schemas.Stash,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
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
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all stashes.

    Returns a list of all stashes.
    """

    all_stashes = await CRUD_stash.get(db=db, filter_params=filter_params)

    return all_stashes


@router.post(
    "/",
    response_model=schemas.StashCreate | list[schemas.StashCreate] | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_stash(
    stash: schemas.StashCreate | list[schemas.StashCreate],
    on_duplicate_pkey_do_nothing: bool | None = None,
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new stashes.

    Returns the created stash or list of stashes.
    """

    return await CRUD_stash.create(
        db=db,
        obj_in=stash,
        on_duplicate_pkey_do_nothing=on_duplicate_pkey_do_nothing,
        return_nothing=return_nothing,
    )


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
