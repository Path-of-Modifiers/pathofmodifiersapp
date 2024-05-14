import secrets
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import os


PRIVATIZE_API = os.getenv("PRIVATIZE_API")
FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

security = HTTPBasic()


def verification(
    credentials: HTTPBasicCredentials = Depends(security),
) -> None:
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    else:
        return True
