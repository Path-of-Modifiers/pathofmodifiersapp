import starlette.status as status

from app.core.config import settings
from app.exceptions.exception_base import PathOfModifiersAPIError


class PlotQueryDataNotFoundError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        query_data: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_404_NOT_FOUND,
    ):
        detail = f"No data matching criteria found. Query data: {query_data}"

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class PlotNoModifiersProvidedError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        query_data: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
    ):
        detail = f"Plotting requires you to select at least one modifier. Query data: {query_data}"

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class PlotRateLimitExceededError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        retry_after_seconds: int,
        max_amount_of_tries_per_time_period: int,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_429_TOO_MANY_REQUESTS,
    ):
        detail = (
            f"Rate limit for plot exceeded. Please try again later. "
            f"max_tries: {max_amount_of_tries_per_time_period} per {settings.PLOT_RATE_LIMIT_COOLDOWN_SECONDS} seconds"
        )

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
            headers={"Retry-After-Seconds": str(retry_after_seconds)},
        )
