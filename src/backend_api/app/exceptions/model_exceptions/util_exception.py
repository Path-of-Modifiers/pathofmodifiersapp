import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError
from app.logger import logger


class _UtilBaseError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        status_code: int | None = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict[str, str] | None = None,
        detail: str | None = "Unknown error in the utility",
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
    ):
        logger.error(detail)

        super().__init__(
            status_code=status_code,
            headers=headers,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class SortingMethodNotSupportedError(_UtilBaseError):
    """Exception raised for when sorting method is not supported errors."""

    def __init__(
        self,
        *,
        sort: str,
        available_sorting_choices: list[str],
        function_name: str | None = None,
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = (
            f"Could not sort. Sorting method '{sort}' is not supported, "
            f"instead choose one of available sorting methods: {available_sorting_choices}"
        )

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class ArgValueNotSupportedError(_UtilBaseError):
    """Exception raised for when value is not supported errors."""

    def __init__(
        self,
        *,
        value: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = f"Value '{value}' is not supported. Value type: '{type(value)}'"

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
