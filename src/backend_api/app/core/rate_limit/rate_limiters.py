from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps import get_username_by_request
from app.core.cache.cache import cache
from app.core.config import settings
from app.core.rate_limit.custom_rate_limiter import RateLimiter, RateSpec
from app.core.rate_limit.rate_limit_config import rate_limit_settings


def default_limit_provider() -> list[str]:
    return [
        rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
        rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
        rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
        rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
    ]


# Limiter for user
limiter_user = Limiter(
    key_func=get_username_by_request,
    default_limits=default_limit_provider(),
    storage_uri=str(settings.CACHE_URI),
    headers_enabled=True,
    enabled=settings.RATE_LIMIT,
)

# Limiter for IP
limiter_ip = Limiter(
    key_func=get_remote_address,
    default_limits=default_limit_provider(),
    storage_uri=str(settings.CACHE_URI),
    headers_enabled=True,
    enabled=settings.RATE_LIMIT,
)


def apply_rate_limits(
    limiter: Limiter, *limits: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Dynamically add the _rate_limits attribute using setattr
        func._rate_limits = limits

        # Apply each limit individually
        for limit in limits:
            func = limiter.limit(limit)(func)
        return func

    return decorator


def apply_user_rate_limits(
    *limits: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return apply_rate_limits(limiter_user, *limits)


def apply_ip_rate_limits(
    *limits: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    return apply_rate_limits(limiter_ip, *limits)


@asynccontextmanager
async def apply_custom_rate_limit(
    unique_key: str, rate_spec: RateSpec, prefix: str
) -> AsyncGenerator[None, RateLimiter]:
    """
    Helper function to apply custom rate limit based on a unique key.
    """
    async with RateLimiter(
        unique_key=unique_key,
        backend=cache,
        rate_spec=rate_spec,
        cache_prefix=prefix,
        enabled=settings.RATE_LIMIT,
    ):
        yield
