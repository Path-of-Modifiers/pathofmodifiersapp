from typing import Any

import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class InvalidTokenError(PathOfModifiersAPIError):
    """Exception raised for invalid token errors."""

    def __init__(
        self,
        *,
        token: Any,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_401_UNAUTHORIZED,
    ):
        if not token:
            detail = "Invalid token. Token is empty, false or None."
        else:
            detail = "Invalid token. Something went wrong."

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class InvalidHeaderProvidedError(PathOfModifiersAPIError):
    """Exception raised for invalid header errors."""

    def __init__(
        self,
        *,
        header: Any,
        function_name: str | None = "Unknown header function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    ):
        if not header:
            detail = "Invalid header. Header is empty, false or None."
        else:
            detail = "Invalid header. Something went wrong."
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
