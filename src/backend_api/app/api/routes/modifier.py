from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy import text
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
from app.core.models.models import Modifier
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_ip_rate_limits,
    apply_user_rate_limits,
)
from app.crud import CRUD_modifier

router = APIRouter()


modifier_prefix = "modifier"


@router.get(
    "/{modifierId}",
    response_model=schemas.Modifier | list[schemas.Modifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
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
    "/latest-dynamically-created/",
    response_model=str | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def modifier_latest_dynamic_created_datetime(
    db: Session = Depends(get_db),
):
    """
    Delete a list of carantene modifier by list of key "caranteneModifierId" and values.

    Returns a message that the carantene modifier was deleted.
    """
    result = db.execute(
        text(
            """SELECT MAX("createdAt") FROM modifier WHERE "dynamicallyCreated" IS TRUE"""
        )
    ).fetchone()

    if not result or not result[0]:
        return None

    return str(result[0])


@router.get(
    "/",
    response_model=schemas.Modifier | list[schemas.Modifier],
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_modifiers(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all modifiers.

    Returns a list of all modifiers.
    """

    all_modifiers = await CRUD_modifier.get(db=db, filter_params=filter_params)

    return all_modifiers


@router.get(
    "/grouped_modifiers_by_effect/",
    response_model=schemas.GroupedModifierByEffect
    | list[schemas.GroupedModifierByEffect],
)
@apply_ip_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
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


@router.put(
    "/update-related-uniques/",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_related_unique_modifiers(
    modifier_related_uniques_update: list[schemas.ModifierRelatedUniquesMap],
    db: Session = Depends(get_db),
):
    """
    Update a modifier by key and value for "modifierId"

    Dominant key is "modifierId".

    Returns the updated modifier.
    """

    for update_rel_modifier in modifier_related_uniques_update:
        modifier_map = {"modifierId": update_rel_modifier.modifierId}

        modifier = await CRUD_modifier.get(
            db=db,
            filter=modifier_map,
        )
        assert not isinstance(modifier, list) and modifier is not None

        update_modifier = schemas.ModifierUpdate(
            position=modifier.position,
            relatedUniques=update_rel_modifier.relatedUniques,
            minRoll=modifier.minRoll,
            maxRoll=modifier.maxRoll,
            textRolls=modifier.textRolls,
            static=modifier.static,
            effect=modifier.effect,
            regex=modifier.regex,
            implicit=modifier.implicit,
            explicit=modifier.explicit,
            delve=modifier.delve,
            fractured=modifier.fractured,
            synthesised=modifier.synthesised,
            unique=modifier.unique,
            corrupted=modifier.corrupted,
            enchanted=modifier.enchanted,
            veiled=modifier.veiled,
            dynamicallyCreated=modifier.dynamicallyCreated,
        )

        await CRUD_modifier.update(db_obj=modifier, obj_in=update_modifier, db=db)
    return f"Updated related uniques for count={len(modifier_related_uniques_update)} modifiers"


@router.post(
    "/initial-dynamically-created/",
    response_model=str,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_initial_dynamically_created_mod(db: Session = Depends(get_db)) -> str:
    await CRUD_modifier.create_initial_dynamically_created_mod(db)

    return "Successfully created or updated initial dynamically created modifier to mininum 3 days since created at"
