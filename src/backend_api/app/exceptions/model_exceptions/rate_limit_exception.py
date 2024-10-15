import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class RateLimitExceededError(PathOfModifiersAPIError):
    """Exception for the custom rate limitter"""

    def __init__(
        self,
        *,
        retry_after_seconds: int,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        max_amount_of_tries_per_time_period: int,
        cooldown_seconds: int,
        status_code: int | None = status.HTTP_429_TOO_MANY_REQUESTS,
    ):
        detail = (
            f"Rate limit exceeded. Please try again later. "
            f"max_tries: {max_amount_of_tries_per_time_period} per {cooldown_seconds} seconds"
        )

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            detail=detail,
            function_name=function_name,
            class_name=class_name,
            headers={"Retry-After-Seconds": str(retry_after_seconds)},
        )
