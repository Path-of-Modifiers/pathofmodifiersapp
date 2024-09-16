from typing import Any

import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class GeneralDBError(PathOfModifiersAPIError):
    """Exception raised for general db errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_500_INTERNAL_SERVER_ERROR,
        exception: Exception | None = None,
        headers: dict[str, str] | None = None,
    ):
        if exception is None:
            detail = "Unknown error"
        else:
            detail = str(exception)

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
            headers=headers,
        )


class DbObjectAlreadyExistsError(PathOfModifiersAPIError):
    """Exception raised for db object already exists errors."""

    def __init__(
        self,
        *,
        model_table_name: str,
        filter: dict[str, Any] | list[dict[str, Any]],
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_409_CONFLICT,
    ):
        if isinstance(filter, list):
            detail = (
                f"Object(s) try to be created in '{model_table_name}' already exists"
            )
        else:
            detail = (
                f"Query in table '{model_table_name}' with filter "
                f"({', '.join([key + ': ' + str(item) for key, item in filter.items()])}) "
                f"already exists"
            )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class DbObjectDoesNotExistError(PathOfModifiersAPIError):
    """Exception raised for db object does not exist errors.

    ``class_name`` is only valid if ``function_name`` is provided.
    """

    def __init__(
        self,
        *,
        model_table_name: str,
        filter: dict[str, str] | None = None,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_404_NOT_FOUND,
    ):
        if filter is None:
            detail = f"No object matching the query in the table {model_table_name} was found."
        else:
            detail = (
                f"No object matching the query with filter "
                f"({', '.join([key + ': ' + str(item) for key, item in filter.items()])}) "
                f"in the table '{model_table_name}' was found."
            )

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class DbTooManyItemsDeleteError(PathOfModifiersAPIError):
    """
    Exception raised for db when too many items are trying to get deleted on one query errors.

    ``class_name`` is only valid if ``function_name`` is provided.
    """

    def __init__(
        self,
        model_table_name: str,
        filter: dict[str, str],
        max_deletion_number: int,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_409_CONFLICT,
    ):
        detail = (
            f"Too many objects matching the query "
            f"({', '.join([key + ': ' + str(item) for key, item in filter.items()])}), "
            f"cannot delete and guarantee safety in the table '{model_table_name}'. "
            f"Maximum of {max_deletion_number} deletions allowed in one query."
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
