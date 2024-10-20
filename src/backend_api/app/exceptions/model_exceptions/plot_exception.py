import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError
from app.logs.logger import logger


class PlotQueryToDBError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        exception: Exception,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
    ):
        detail = f"Failed to perform plot query to the database. Exception: {exception}"
        logger.error(detail)

        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class PlotQueryDataNotFoundError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        query_data: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_404_NOT_FOUND,
    ):
        detail = f"No data matching criteria found. Query data: {query_data}"

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class PlotNoModifiersProvidedError(PathOfModifiersAPIError):
    def __init__(
        self,
        *,
        query_data: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
    ):
        detail = f"Plotting requires you to select at least one modifier. Query data: {query_data}"

        # Call the parent constructor with a specific status code
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
