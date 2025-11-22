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
from app.core.models.models import CaranteneModifier
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from app.crud import CRUD_carantene_modifier

router = APIRouter()


carantene_modifier_prefix = "carantene_modifier"


@router.get(
    "/{caranteneModifierId}",
    response_model=schemas.CaranteneModifier | list[schemas.CaranteneModifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_carantene_modifier(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    caranteneModifierId: int,
    db: Session = Depends(get_db),
):
    """
    Get carantene modifier or list of carantene modifiers by key and
    value for "caranteneModifierId"

    Returns one or a list of carantene_modifiers.
    """

    carantene_modifier_map = {"caranteneModifierId": caranteneModifierId}
    carantene_modifier = await CRUD_carantene_modifier.get(
        db=db, filter=carantene_modifier_map
    )

    return carantene_modifier


@router.get(
    "/",
    response_model=schemas.CaranteneModifier | list[schemas.CaranteneModifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_carantene_modifiers(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all carantene_modifiers.

    Returns a list of all carantene_modifiers.
    """

    all_carantene_modifiers = await CRUD_carantene_modifier.get(
        db=db, filter_params=filter_params
    )

    return all_carantene_modifiers


@router.post(
    "/",
    response_model=schemas.CaranteneModifierCreate
    | list[schemas.CaranteneModifierCreate]
    | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_carantene_modifier(
    carantene_modifier: schemas.CaranteneModifierCreate
    | list[schemas.CaranteneModifierCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new carantene_modifiers.

    Returns the created carantene_modifier or list of carantene_modifiers.
    """

    return await CRUD_carantene_modifier.create(
        db=db, obj_in=carantene_modifier, return_nothing=return_nothing
    )


@router.put(
    "/",
    response_model=schemas.CaranteneModifier,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_carantene_modifier(
    caranteneModifierId: int,
    carantene_modifier_update: schemas.CaranteneModifierUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a carantene_modifier by key and value for "caranteneModifierId"

    Dominant key is "caranteneModifierId".

    Returns the updated carantene modifier.
    """

    carantene_modifier_map = {"caranteneModifierId": caranteneModifierId}

    carantene_modifier = await CRUD_carantene_modifier.get(
        db=db,
        filter=carantene_modifier_map,
    )

    return await CRUD_carantene_modifier.update(
        db_obj=carantene_modifier, obj_in=carantene_modifier_update, db=db
    )


@router.delete(
    "/{caranteneModifierId}",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_carantene_modifier(
    caranteneModifierId: int,
    db: Session = Depends(get_db),
):
    """
    Delete a carantene modifier by key and value for "caranteneModifierId"

    Returns a message that the carantene modifier was deleted.
    Always deletes one carantene_modifier.
    """

    carantene_modifier_map = {"caranteneModifierId": caranteneModifierId}
    await CRUD_carantene_modifier.remove(db=db, filter=carantene_modifier_map)

    return get_delete_return_msg(
        model_table_name=CaranteneModifier.__tablename__, filter=carantene_modifier_map
    ).message


@router.delete(
    "/bulk-delete/",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def bulk_delete_carantene_modifier(
    caranteneModifierIds: list[schemas.CaranteneModifiersPK],
    db: Session = Depends(get_db),
):
    """
    Delete a list of carantene modifier by list of key "caranteneModifierId" and values.

    Returns a message that the carantene modifier was deleted.
    """
    filter = [car_id.caranteneModifierId for car_id in caranteneModifierIds]
    await CRUD_carantene_modifier.remove(
        db=db,
        filter=filter,
        max_deletion_limit=99999999999,
        deletion_key="caranteneModifierId",
    )

    return get_delete_return_msg(
        model_table_name=CaranteneModifier.__tablename__,
        filter=caranteneModifierIds,
    ).message
