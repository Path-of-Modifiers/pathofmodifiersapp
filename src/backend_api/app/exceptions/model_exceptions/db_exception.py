from typing import Any

import starlette.status as status

from app.core.models.models import User as model_User
from app.exceptions.exception_base import PathOfModifiersAPIError
from app.logs.logger import logger

HIDDEN_TABLE_LIST = [model_User.__tablename__]


class _DBErrorLogBase(PathOfModifiersAPIError):
    """If you want DB error to be logged, inherit from this class."""

    def __init__(
        self,
        *,
        status_code: int | None = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict[str, str] | None = None,
        function_name: str | None = "Unknown function",
        detail: str | None = "Unknown error in the database",
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


class GeneralDBError(_DBErrorLogBase):
    """Exception raised for general db errors."""

    def __init__(
        self,
        *,
        model_table_name: str,
        headers: dict[str, str] | None = None,
        function_name: str | None = None,
        class_name: str | None = None,
        detail: str | None = None,
        exception: Exception | None = None,
    ):
        if model_table_name in HIDDEN_TABLE_LIST:
            detail = f"A general error occured in {model_table_name} table"
        elif exception is not None and detail is None:
            detail = f"Details: {detail}. The DB exception occured: {exception}"
        elif detail is None:
            detail = "An error occured during operations to the database"

        super().__init__(
            function_name=function_name,
            class_name=class_name,
            detail=detail,
            headers=headers,
        )


class DbObjectAlreadyExistsError(_DBErrorLogBase):
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
            if model_table_name in HIDDEN_TABLE_LIST:
                detail = (
                    f"Query in {model_table_name} table with filter "
                    f"({', '.join([key + ': hidden_value' for key in filter.keys()])}) "
                    f"already exists"
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
        filter: dict[str, Any] | None = None,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_404_NOT_FOUND,
    ):
        if filter is None:
            detail = f"No object matching the query in the table {model_table_name} was found."
        else:
            if model_table_name in HIDDEN_TABLE_LIST:
                detail = (
                    f"No {model_table_name} object matching the query with filter "
                    f"({', '.join([key + ': hidden_value' for key in filter.keys()])}) "
                    f"in the table '{model_table_name}' was found."
                )
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


class DbTooManyItemsDeleteError(_DBErrorLogBase):
    """
    Exception raised for db when too many items are trying to get deleted on one query errors.

    ``class_name`` is only valid if ``function_name`` is provided.
    """

    def __init__(
        self,
        model_table_name: str,
        max_deletion_number: int,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_409_CONFLICT,
    ):
        detail = (
            f"Too many objects matching the query "
            f"cannot delete and guarantee safety in the table '{model_table_name}'. "
            f"Maximum of {max_deletion_number} deletions allowed in one query."
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
