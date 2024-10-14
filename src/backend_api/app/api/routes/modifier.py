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
from app.core.models.models import Modifier
from app.crud import CRUD_modifier
from app.limiter import apply_user_rate_limits

router = APIRouter()


modifier_prefix = "modifier"


@router.get(
    "/{modifierId}",
    response_model=schemas.Modifier | list[schemas.Modifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_modifier(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    modifierId: int,
    db: Session = Depends(get_db),
):
    """
    Get modifier or list of modifiers by key and
    value for "modifierId"

    Dominant key is "modifierId".

    Returns one or a list of modifiers.
    """

    modifier_map = {"modifierId": modifierId}
    modifier = await CRUD_modifier.get(db=db, filter=modifier_map)

    return modifier


@router.get(
    "/",
    response_model=schemas.Modifier | list[schemas.Modifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_modifiers(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Get all modifiers.

    Returns a list of all modifiers.
    """

    all_modifiers = await CRUD_modifier.get(db=db)

    return all_modifiers


@router.get(
    "/grouped_modifiers_by_effect/",
    response_model=schemas.GroupedModifierByEffect
    | list[schemas.GroupedModifierByEffect],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_grouped_modifier_by_effect(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Get all grouped modifiers by effect.

    Returns a list of all grouped modifiers by effect.
    """

    all_grouped_modifiers_by_effect = (
        await CRUD_modifier.get_grouped_modifier_by_effect(db=db)
    )

    return all_grouped_modifiers_by_effect


@router.post(
    "/",
    response_model=schemas.ModifierCreate | list[schemas.ModifierCreate] | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_modifier(
    modifier: schemas.ModifierCreate | list[schemas.ModifierCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new modifiers.

    Returns the created modifier or list of modifiers.
    """

    return await CRUD_modifier.create(
        db=db, obj_in=modifier, return_nothing=return_nothing
    )


@router.put(
    "/",
    response_model=schemas.Modifier,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_modifier(
    modifierId: int,
    modifier_update: schemas.ModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a modifier by key and value for "modifierId"

    Dominant key is "modifierId".

    Returns the updated modifier.
    """

    modifier_map = {"modifierId": modifierId}

    modifier = await CRUD_modifier.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_modifier.update(db_obj=modifier, obj_in=modifier_update, db=db)


@router.delete(
    "/{modifierId}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_modifier(
    modifierId: int,
    db: Session = Depends(get_db),
):
    """
    Delete a modifier by key and value for "modifierId"

    Returns a message that the modifier was deleted.
    Always deletes one modifier.
    """

    modifier_map = {"modifierId": modifierId}
    await CRUD_modifier.remove(db=db, filter=modifier_map)

    return get_delete_return_msg(
        model_table_name=Modifier.__tablename__, filter=modifier_map
    ).message
