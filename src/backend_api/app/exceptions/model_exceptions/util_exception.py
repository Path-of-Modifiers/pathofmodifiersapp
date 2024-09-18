import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class SortingMethodNotSupportedError(PathOfModifiersAPIError):
    """Exception raised for when sorting method is not supported errors."""

    def __init__(
        self,
        *,
        sort: str,
        available_sorting_choices: list[str],
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = f"""Could not sort. Sorting method '{sort}' is not supported,
        instead choose one of available sorting methods: {available_sorting_choices}"""

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class ArgValueNotSupportedError(PathOfModifiersAPIError):
    """Exception raised for when value is not supported errors."""

    def __init__(
        self,
        *,
        value: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = f"Value '{value}' is not supported. Value type: {type(value)}\n"

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
