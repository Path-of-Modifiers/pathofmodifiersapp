from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, field_validator


class RateLimitPerTimeInterval(BaseModel):
    rate_per_interval: str

    @field_validator("rate_per_interval")
    def check_rate_pattern(cls, value):
        import re

        if not re.match(r"^\d+/(second|minute|hour|day)$", value):
            raise ValueError(
                "Rate per interval must be in the format {number}/second, {number}/minute, {number}/hour, or {number}/day"
            )
        return value


# Function to retrieve decorator parameters
def get_function_decorator_rate_limit_per_time_interval(
    func: Callable[[Any, Any], Awaitable[Any]],
) -> list[RateLimitPerTimeInterval]:
    """
    Gets rate limit per time interval from function decorator.

    Should only be used on API route functions.
    """
    all_rate_per_interval = getattr(func, "_rate_limits", None)
    if not all_rate_per_interval:
        raise ValueError("Rate limit decorator values not found on function")

    rate_limit_per_time_interval_list = [
        RateLimitPerTimeInterval(rate_per_interval=rate_per_interval)
        for rate_per_interval in all_rate_per_interval
    ]
    return rate_limit_per_time_interval_list
