from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.api.params import FilterParams
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from app.crud import CRUD_league

router = APIRouter()


league_prefix = "league"


@router.get(
    "/{leagueId}",
    response_model=schemas.League,
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_league(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    leagueId: int,
    db: Session = Depends(get_db),
):
    """
    Get league by key and value for "leagueId".

    Always returns one league.
    """

    league_map = {"leagueId": leagueId}
    league = await CRUD_league.get(db=db, filter=league_map)

    return league


@router.get(
    "/",
    response_model=schemas.League | list[schemas.League],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_all_leagues(
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all leagues.

    Returns a list of all leagues.
    """

    all_leagues = await CRUD_league.get(db=db, filter_params=filter_params)

    return all_leagues


@router.get(
    f"/active_{league_prefix}/",
    response_model=list[schemas.League],
    dependencies=[
        Depends(get_current_active_user),
    ],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_active_leagues(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    db: Session = Depends(get_db),
):
    """
    Get leagues that are still valid/active

    Always returns a list, but it may be empty.
    """

    leagues = await CRUD_league.get_active_leagues(db=db)

    return leagues


@router.post(
    "/",
    response_model=schemas.LeagueCreate | list[schemas.LeagueCreate] | None,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_league(
    league: schemas.LeagueCreate | list[schemas.LeagueCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of new leagues.

    Returns the created league or list of leagues.
    """

    return await CRUD_league.create(db=db, obj_in=league, return_nothing=return_nothing)


@router.put(
    "/{leagueId}",
    response_model=schemas.League,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_modifier(
    leagueId: int,
    league_update: schemas.LeagueUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a league by key and value for "leagueId"

    Returns the updated league.
    """

    modifier_map = {"leagueId": leagueId}

    modifier = await CRUD_league.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_league.update(db_obj=modifier, obj_in=league_update, db=db)
