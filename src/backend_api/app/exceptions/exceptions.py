# Can be replaced with ./api_message_util.py for better error handling


from typing import Any


class PathOfModifiersAPIError(Exception):
    """Base class for exceptions in the Path of Modifiers API module."""

    def __init__(
        self,
        status_code: int = 500,
        function_name: str = "Unknown function",
        message: str = "Path of Modifiers service is unavailable",
    ):
        self.status_code = status_code
        self.function_name = function_name
        self.message = f"POM API : {status_code} : {function_name} : {message}"
        super().__init__(
            self.message,
        )


class InvalidTokenError(PathOfModifiersAPIError):
    """Exception raised for invalid token errors."""

    def __init__(
        self,
        function_name: str,
        token: Any,
    ):
        if not isinstance(token, str):
            message = f"Invalid token: '{str(token)}'. Token should be a string, not type {type(token)}."
        elif token == "":
            message = "Invalid token: Token is an empty string."
        elif " " in token:
            message = f"Invalid token: '{token}' contains whitespace."
        else:
            message = f"Invalid token: '{token}'. Something went wrong."

        # Call the parent constructor with a specific status code
        super().__init__(
            403,
            function_name,
            message,
        )
