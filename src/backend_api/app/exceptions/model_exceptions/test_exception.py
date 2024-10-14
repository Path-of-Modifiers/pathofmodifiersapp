import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError
from app.logs.logger import test_logger


class _TestErrorLogBase(PathOfModifiersAPIError):
    """If you want a test error to be logged, inherit from this class."""

    def __init__(
        self,
        *,
        status_code: int | None = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict[str, str] | None = None,
        function_name: str | None = "Unknown function",
        detail: str | None = "Unknown error in the database",
        class_name: str | None = None,
    ):
        test_logger.error(detail)

        super().__init__(
            status_code=status_code,
            headers=headers,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class OnlyAvailableInLocalEnvError(_TestErrorLogBase):
    """Exception raised when an operation is only available in local environment."""

    def __init__(
        self,
        *,
        status_code: int | None = status.HTTP_403_FORBIDDEN,
        headers: dict[str, str] | None = None,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
    ):
        detail = "This operation is only available in a local environment."
        super().__init__(
            status_code=status_code,
            headers=headers,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
