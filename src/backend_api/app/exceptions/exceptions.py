# Can be replaced with ./api_message_util.py for better error handling

from typing import Any

from fastapi import HTTPException


class PathOfModifiersAPIError(HTTPException):
    """Base class for exceptions in the Path of Modifiers API module."""

    def __init__(
        self,
        status_code: int = 500,
        function_name: str = "Unknown function",
        detail: str = "Path of Modifiers service is unavailable",
    ):
        self.status_code = status_code
        self.function_name = function_name
        self.detail = f"POM API : {status_code} : {function_name} : {detail}"
        super().__init__(
            self.status_code,
            self.detail,
        )


class InvalidTokenError(PathOfModifiersAPIError):
    """Exception raised for invalid token errors."""

    def __init__(
        self,
        function_name: str,
        token: Any,
    ):
        if not isinstance(token, str):
            detail = f"Invalid token: '{str(token)}'. Token should be a string, not type {type(token)}."
        elif token == "":
            detail = "Invalid token: Token is an empty string."
        elif " " in token:
            detail = f"Invalid token: '{token}' contains whitespace."
        else:
            detail = f"Invalid token: '{token}'. Something went wrong."

        # Call the parent constructor with a specific status code
        super().__init__(
            403,
            function_name,
            detail,
        )


class InvalidHeaderProvidedError(PathOfModifiersAPIError):
    """Exception raised for invalid header errors."""

    def __init__(self, status_code: int, function_name: str, detail: str):
        super().__init__(
            status_code,
            function_name,
            detail,
        )


class NotAuthenticatedError(PathOfModifiersAPIError):
    """Exception raised for not authenticated errors."""

    def __init__(self, status_code: int, function_name: str, detail: str):
        detail = "Could not authenticate user."
        super().__init__(
            status_code,
            function_name,
            detail,
        )
