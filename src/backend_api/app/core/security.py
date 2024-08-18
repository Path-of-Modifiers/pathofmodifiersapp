import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

from app.core.config import settings

PRIVATIZE_API = os.getenv("PRIVATIZE_API")
FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

security = HTTPBasic()


def verification(
    credentials: HTTPBasicCredentials = Depends(security),
) -> None:
    """Verify the username and password for the API.

    Needs to raise HTTPException if return False.

    Args:
        credentials (HTTPBasicCredentials, optional): HTTP Credentials. Defaults to Depends(security).

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        None
    """
    if PRIVATIZE_API:
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = FIRST_SUPERUSER.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = FIRST_SUPERUSER_PASSWORD.encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if is_correct_password and is_correct_username:
            return True
        else:
            return False
    else:
        return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
