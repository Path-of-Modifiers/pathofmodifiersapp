import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

import app.core.models.database as _database
from app.api.api_message_util import (
    get_invalid_token_credentials_msg,
    get_no_obj_matching_query_msg,
    get_not_active_or_auth_user_error_msg,
    get_not_superuser_auth_msg,
)
from app.core import security
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas.token import TokenPayload
from app.exceptions.exceptions import InvalidHeaderProvidedError, InvalidTokenError

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
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=get_invalid_token_credentials_msg().message,
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(None, User.__tablename__).message,
        )
    if not user.isActive:
        raise HTTPException(
            status_code=400,
            detail=get_not_active_or_auth_user_error_msg(user.username).message,
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=get_not_superuser_auth_msg(current_user.username).message,
        )
    return current_user


def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.isActive:
        raise HTTPException(
            status_code=403,
            detail=get_not_active_or_auth_user_error_msg(current_user.username).message,
        )
    return current_user


def get_current_user_id_by_request(request: Request) -> str:
    # Currently too slow to use in production.
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
            status_code=403,
            function_name=get_current_user_id_by_request.__name__,
            message=f"No Authorization header provided. Authorization header: {header}",
        )
    token = header.split("Bearer ")[1]

    if isinstance(token, str):
        current_user = get_current_user(token=token, session=next(get_db()))
    else:
        raise InvalidTokenError(
            function_name=get_current_user_id_by_request.__name__,
            token=token,
        )

    if current_user.isSuperuser is True:
        # Return random string to avoid rate limiting
        random_identifier = uuid.uuid4().hex
        return random_identifier
    return current_user.userId


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
