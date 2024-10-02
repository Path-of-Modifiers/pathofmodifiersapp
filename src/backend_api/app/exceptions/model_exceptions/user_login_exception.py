import starlette.status as status

from app.exceptions.exception_base import PathOfModifiersAPIError


class UserWithNotEnoughPrivilegesError(PathOfModifiersAPIError):
    """Exception raised when user doesn't have enough privileges to perform an action."""

    def __init__(
        self,
        *,
        username_or_email: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_403_FORBIDDEN,
    ):
        detail = f"Cannot perform action with user '{username_or_email}'. User doesn't have enough privileges to perform this action"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserIsNotActiveError(PathOfModifiersAPIError):
    """Exception raised when user tries to perform actions and is not active."""

    def __init__(
        self,
        *,
        username_or_email: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_403_FORBIDDEN,
    ):
        detail = (
            f"Cannot perform action with user '{username_or_email}'. User is not active"
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class SuperUserNotAllowedToDeleteSelfError(PathOfModifiersAPIError):
    """Exception raised when superuser tries to delete themselves."""

    def __init__(
        self,
        *,
        username_or_email: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_403_FORBIDDEN,
    ):
        detail = (
            f"Cannot delete user '{username_or_email}'. "
            f"Superuser is not allowed to delete themselves"
        )

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class SuperUserNotAllowedToChangeActiveSelfError(PathOfModifiersAPIError):
    """Exception raised when superuser tries to change their active status."""

    def __init__(
        self,
        *,
        username_or_email: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_403_FORBIDDEN,
    ):
        detail = (
            f"Cannot change user '{username_or_email}' active status. "
            f"Superuser is not allowed to change their active status"
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class BadLoginCredentialsError(PathOfModifiersAPIError):
    """Exception raised for bad login credentials errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_401_UNAUTHORIZED,
    ):
        detail = "Could not authorize. Invalid login credentials"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class InvalidPasswordError(PathOfModifiersAPIError):
    """Exception raised for invalid password errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_401_UNAUTHORIZED,
    ):
        detail = "Could not authorize. Invalid password"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class EmailOrUsernameRequiredError(PathOfModifiersAPIError):
    """Exception raised for email or username is required for the operation errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = "Email or username is required for this operation"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class NewPasswordIsSameError(PathOfModifiersAPIError):
    """Exception raised if the new password is the same as the old one."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
        detail: str | None = None,
    ):
        detail = "Could not authorize. New password is the same as the old one"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class NotAuthenticatedError(PathOfModifiersAPIError):
    """Exception raised for not authenticated errors."""

    def __init__(
        self,
        *,
        detail: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UpdateExisitingMeValuesError(PathOfModifiersAPIError):
    """
    Exception raised when user tries to update their own values to
    be the same as their own existing values.
    """

    def __init__(
        self,
        *,
        value: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_400_BAD_REQUEST,
    ):
        detail = (
            f"Cannot update user with value '{value}' to be "
            f"the same as their own existing values."
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserEmailRequiredError(PathOfModifiersAPIError):
    """Exception raised for email is required for the operation errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = "Email is required for this operation"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserUsernameRequiredError(PathOfModifiersAPIError):
    """Exception raised for username is required for the operation errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int | None = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = "Username is required for this operation"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
