# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from typing import Any

from fastapi import APIRouter, Request, Response

from app.api.deps import (
    CurrentUser,
    UserCachePasswordResetSession,
    UserCacheRegisterSession,
    UserCacheUpdateMeSession,
)
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_user_rate_limits
from app.core.schemas import UserPublic
from app.core.schemas.user import UserInCache

router = APIRouter()


check_token_prefix = "check-token"


@router.post("/check-access-token", response_model=UserPublic)
@apply_user_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_SECOND,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def check_access_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
) -> Any:
    """
    Check access token

    """
    return current_user


@router.post("/check-register-token", response_model=UserInCache)
@apply_user_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_SECOND,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def check_register_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    register_token: str,
    user_cache_register_session: UserCacheRegisterSession,
) -> Any:
    """
    Check register token
    """
    return await user_cache_register_session.verify_token(register_token)


@router.post("/check-password-reset-token", response_model=UserInCache)
@apply_user_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_SECOND,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def check_password_reset_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    password_reset_token: str,
    user_cache_password_reset_session: UserCachePasswordResetSession,
) -> Any:
    """
    Check password reset token
    """
    return await user_cache_password_reset_session.verify_token(password_reset_token)


@router.post("/check-update-me-token", response_model=UserInCache)
@apply_user_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_SECOND,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def check_update_me_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    update_me_token: str,
    user_cache_update_me_session: UserCacheUpdateMeSession,
) -> Any:
    """
    Check register token
    """
    return await user_cache_update_me_session.verify_token(update_me_token)
