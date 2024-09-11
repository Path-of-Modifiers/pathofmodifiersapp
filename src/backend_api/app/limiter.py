from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps import get_user_token_by_request
from app.core.config import settings
from app.rate_limit.plot_rate_limit import PlotRateLimit


def default_limit_provider() -> list[str]:
    return [
        settings.DEFAULT_USER_RATE_LIMIT_SECOND,
        settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
        settings.DEFAULT_USER_RATE_LIMIT_HOUR,
        settings.DEFAULT_USER_RATE_LIMIT_DAY,
    ]


# Limiter for user
limiter_user = Limiter(
    key_func=lambda request: get_user_token_by_request,  # Limits based on IP address is default, but can be changed to other functions
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

limiter_user_plot = PlotRateLimit()


def apply_rate_limits(limiter, *limits):
    def decorator(func):
        for limit in limits:
            func = limiter.limit(limit)(func)
        return func

    return decorator


def apply_user_rate_limits(*limits):
    return apply_rate_limits(limiter_user, *limits)


def apply_ip_rate_limits(*limits):
    return apply_rate_limits(limiter_ip, *limits)
