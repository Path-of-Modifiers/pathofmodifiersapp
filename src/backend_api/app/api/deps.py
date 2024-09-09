from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.core.models.database as _database
from app.core.cache import user_cache_session
from app.core.config import settings
from app.core.models.models import User
from app.exceptions import (
    DbObjectDoesNotExistError,
    InvalidHeaderProvidedError,
    UserIsNotActiveError,
    UserWithNotEnoughPrivilegesError,
)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    token: TokenDep,
    session: Session = Depends(get_db),
) -> User:
    user_cached = user_cache_session.verify_token(token)

    user = session.get(User, user_cached.userId)
    if not user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter={"userId": user_cached.userId},
            function_name=get_current_user.__name__,
        )
    if not user.isActive:
        raise UserIsNotActiveError(
            username_or_email=user.username,
            function_name=get_current_user.__name__,
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=UserWithNotEnoughPrivilegesError(
                username_or_email=current_user.username,
                function_name=get_current_active_superuser.__name__,
            ).detail,
        )
    return current_user


def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.isActive:
        raise UserIsNotActiveError(
            username_or_email=current_user.username,
            function_name=get_current_active_user.__name__,
        )
    return current_user


def get_user_token_by_request(request: Request) -> str:
    """Get current user id by request.

    Args:
        request (Request): The request

    Raises:
        HTTPException: HTTPException
        InvalidTokenError: InvalidTokenError

    Returns:
        str: _description_
    """
    header = request.headers.get("Authorization")
    if not header:
        raise InvalidHeaderProvidedError(
            function_name=get_user_token_by_request.__name__,
            header=header,
        )
    token = header.split("Bearer ")[1]

    return token


def get_limit_for_current_user_plot(current_user: CurrentUser) -> str:
    # Slow api doesn't support user based or request rate limit values,
    # this is for future use
    """Rate limit for current user when plotting

    Args:
        current_user (CurrentUser): The current user

    Returns:F
        str: Rates for the current user
    """

    if current_user.isSuperuser:
        return "99999999999/minute"

    match current_user.rateLimitTier:
        case 0:
            return settings.DEFAULT_PLOT_RATE_LIMIT
        case 1:
            return settings.TIER_1_PLOT_RATE_LIMIT
        case 2:
            return settings.TIER_2_PLOT_RATE_LIMIT
        case _:
            return settings.TIER_3_PLOT_RATE_LIMIT
