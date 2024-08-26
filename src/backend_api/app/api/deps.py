from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
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

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
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
