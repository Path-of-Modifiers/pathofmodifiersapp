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


async def get_current_user(
    token: TokenDep,
    session: Session = Depends(get_db),
) -> User:
    user_cached = await user_cache_session.verify_token(token)

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


async def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=UserWithNotEnoughPrivilegesError(
                username_or_email=current_user.username,
                function_name=get_current_active_superuser.__name__,
            ).detail,
        )
    return current_user


async def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.isActive:
        raise UserIsNotActiveError(
            username_or_email=current_user.username,
            function_name=get_current_active_user.__name__,
        )
    return current_user


def get_user_id_by_request(request: Request) -> str:
    """Get current user id by request.

    Args:
        request (Request): The request

    Raises:
        HTTPException: HTTPException
        InvalidTokenError: InvalidTokenError

    Returns:
        str: The user id extracted from the token.
    """
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        raise InvalidHeaderProvidedError(
            status_code=403,
            function_name=get_user_id_by_request.__name__,
            header=header,
        )

    user_id = header[7:]  # Strip "Bearer " prefix (7 characters)

    return user_id


def get_rate_limit_amount_by_tier(tier: int) -> int:
    if tier == 0:
        return settings.TIER_0_PLOT_RATE_LIMIT
    if tier == 1:
        return settings.TIER_1_PLOT_RATE_LIMIT


async def get_rate_limit_tier_by_request(request: Request) -> int:
    """Get current user rate limit tier by request."""
    token = get_user_id_by_request(request)

    user = await user_cache_session.verify_token(token)

    if user.isSuperuser:
        return 30  #

    return get_rate_limit_amount_by_tier(user.rateLimitTier)
