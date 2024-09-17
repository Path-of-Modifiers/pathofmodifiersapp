# Can be replaced with ./api_message_util.py for better error handling


from fastapi import HTTPException


class PathOfModifiersAPIError(HTTPException):
    """
    Base class for exceptions in the Path of Modifiers API module.

    ``function_name`` makes it easier to debug. It can be provided with `function.__name__`.
    """

    def __init__(
        self,
        *,
        status_code: int | None = 500,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        detail: str | None = "Path of Modifiers service is unavailable",
        headers: dict[str, str] | None = None,
    ):
        if class_name is not None and function_name is not None:
            function_name = f"{class_name}.{function_name}"
        status_code = status_code
        function_name = function_name
        detail = f"POM API : status={status_code} : function={function_name} : {detail}"
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
