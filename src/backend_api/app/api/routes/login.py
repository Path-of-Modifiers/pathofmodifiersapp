# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import (
    UserCacheSession,
    get_db,
)
from app.core.config import settings
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_ip_rate_limits,
)
from app.core.schemas import Token
from app.crud import CRUD_user
from app.exceptions import (
    BadLoginCredentialsError,
)

router = APIRouter()

login_prefix = "login"


@router.post("/access-token")
@apply_ip_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def login_access_session(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_session_cache: UserCacheSession,
    db: Session = Depends(get_db),
) -> Token:
    """
    OAuth2 compatible session login.
    """
    user = CRUD_user.authenticate(
        db=db, email_or_username=form_data.username, password=form_data.password
    )

    if not user:
        raise BadLoginCredentialsError(
            function_name=login_access_session.__name__,
        )

    access_token = await user_session_cache.create_user_cache_instance(
        user=user,
        expire_seconds=settings.ACCESS_SESSION_EXPIRE_SECONDS,
    )

    return Token(
        access_token=access_token,
    )
