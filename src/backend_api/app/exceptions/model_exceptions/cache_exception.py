import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class InvalidCacheUpdateParamsError(PathOfModifiersAPIError):
    """Exception raised for when cache update params are invalid errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
    ):
        detail = "Invalid cache update params for object."
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
