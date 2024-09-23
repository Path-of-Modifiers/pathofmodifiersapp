from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.datastructures import Headers

from app.core.cache.user_cache import UserCache, UserCacheTokenType
from app.core.config import settings
from app.core.models.database import engine
from app.core.models.models import User
from app.exceptions import (
    DbObjectDoesNotExistError,
    InvalidHeaderProvidedError,
    UserIsNotActiveError,
    UserWithNotEnoughPrivilegesError,
)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_db():
    AsyncSessionLocal = async_sessionmaker(
        autocommit=False, bind=engine, expire_on_commit=False
    )

    db = AsyncSessionLocal()
    yield db


async def get_user_cache_session() -> AsyncGenerator[UserCache, None]:
    """Get user cache session."""
    async with UserCache(UserCacheTokenType.ACCESS_SESSION) as user_cache_session:
        yield user_cache_session


UserCacheSession = Annotated[UserCache, Depends(get_user_cache_session)]


async def get_user_cache_register_session() -> AsyncGenerator[UserCache, None]:
    """Get user cache register session."""
    async with UserCache(
        UserCacheTokenType.REGISTER_USER
    ) as user_cache_register_session:
        yield user_cache_register_session


UserCacheRegisterSession = Annotated[
    UserCache, Depends(get_user_cache_register_session)
]


async def get_user_cache_password_reset_session() -> AsyncGenerator[UserCache, None]:
    """Get user cache password reset session."""
    async with UserCache(
        UserCacheTokenType.PASSWORD_RESET
    ) as user_cache_password_reset_session:
        yield user_cache_password_reset_session


UserCachePasswordResetSession = Annotated[
    UserCache, Depends(get_user_cache_password_reset_session)
]


async def get_user_cache_update_me_session() -> AsyncGenerator[UserCache, None]:
    """Get user cache update me session."""
    async with UserCache(UserCacheTokenType.UPDATE_ME) as user_cache_update_me_session:
        yield user_cache_update_me_session


UserCacheUpdateMeSession = Annotated[
    UserCache, Depends(get_user_cache_update_me_session)
]


async def get_current_user(
    token: TokenDep,
    user_cache_session: UserCacheSession,
    db: AsyncSession = Depends(get_db),
) -> User:
    user_cached = await user_cache_session.verify_token(token)

    user = await db.get(User, user_cached.userId)
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
        raise UserWithNotEnoughPrivilegesError(
            username_or_email=current_user.username,
            function_name=get_current_active_superuser.__name__,
        )
    return current_user


async def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.isActive:
        raise UserIsNotActiveError(
            username_or_email=current_user.username,
            function_name=get_current_active_user.__name__,
        )
    return current_user


def get_token_from_headers(headers: Headers) -> str:
    """Get access token from header.

    Args:
        headers (Headers): The headers

    Raises:
        InvalidTokenError: InvalidHeaderProvidedError

    Returns:
        str: The access token extracted from the header.
    """
    header = headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        raise InvalidHeaderProvidedError(
            status_code=403,
            function_name=get_token_from_headers.__name__,
            header=header,
        )

    token = header[7:]  # Strip "Bearer " prefix (7 characters)

    return token


def get_user_token_by_request(request: Request) -> str:
    """Get user access token by request."""
    return get_token_from_headers(request.headers)


def get_username_by_request(request: Request) -> str:
    """Get username by request."""
    token = get_token_from_headers(request.headers)

    return UserCache.extract_username_from_token(token=token)


def get_rate_limit_amount_by_tier(tier: int) -> int:
    if tier == 0:
        return settings.TIER_0_PLOT_RATE_LIMIT
    if tier == 1:
        return settings.TIER_1_PLOT_RATE_LIMIT


async def get_rate_limit_tier_by_request(
    request: Request, user_cache_session: UserCacheSession
) -> int:
    """Get current user rate limit tier by request."""
    token = get_user_token_by_request(request)

    user = await user_cache_session.verify_token(token)

    if user.isSuperuser:
        return settings.TIER_SUPERUSER_PLOT_RATE_LIMIT

    return get_rate_limit_amount_by_tier(user.rateLimitTier)
