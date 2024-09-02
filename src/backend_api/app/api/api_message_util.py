from pydantic import EmailStr

from app.core.schemas.message import Message
from app.core.schemas.user import (
    UsernameStr,
)


def get_delete_return_msg(
    model_table_name: str,
    filter: dict[str, str],
) -> Message:
    """Returns a message indicating the object was deleted successfully.

    Args:
        model_table_name (str): Table name for the object.
        unique_identifier (str): Unique identifier for the object (main primary key name).
        unique_identifier_value (str): Value of the unique identifier.

    Returns:
        str: Message indicating the object was deleted successfully.
    """

    return Message(
        message=f"""{model_table_name} with filter
        {filter} was
        deleted successfully"""
    )


def get_db_obj_already_exists_msg(
    model_table_name: str,
    filter: dict[str, str],
) -> Message:
    """Returns a message indicating the object already exists.

    Args:
        model_table_name (str): Model table name for the object.
        filter (dict[str, str]): filter of the object.

    Returns:
        Message: Message indicating the object already exists.
    """

    return Message(
        message=f"""{model_table_name} with filter
        ({', '.join([key + ': ' + str(item) for key, item in filter.items()])})
        already exists"""
    )


def get_not_superuser_auth_msg(username: str) -> Message:
    """Returns a message indicating the user is not a superuser.

    Args:
        username (str): Username of the user.

    Returns:
        Message: Message indicating the user is not a superuser.
    """

    return Message(message=f"OAuth user {username} is not a superuser")


def get_not_active_or_auth_user_error_msg(username: str) -> Message:
    """Returns a message indicating the user is not active or authenticated.

    Args:
        username (str): Username of the user.

    Returns:
        Message: Message indicating the user is not active or authenticated.
    """

    return Message(
        message=f"OAuth user {username} is not authenticated or is not active"
    )


def get_superuser_not_allowed_delete_self_msg(username: str) -> Message:
    """Returns a message indicating a superuser is not allowed to delete themselves.

    Returns:
        Message: Message indicating a superuser is not allowed to delete themselves.
    """

    return Message(message=f"Superuser {username} is not allowed to delete themselves")


def get_superuser_not_allowed_change_active_self_msg(username: str) -> Message:
    """Returns a message indicating a superuser is not allowed to change their active status.

    Returns:
        Message: Message indicating a superuser is not allowed to change their active status.
    """

    return Message(
        message=f"Superuser {username} is not allowed to change their active status"
    )


def get_user_active_change_msg(username: str, active: bool) -> Message:
    """Returns a message indicating the user's active status was changed successfully.

    Args:
        username (str): Username of the user.
        active (bool): Active status of the user.

    Returns:
        Message: Message indicating the user's active status was changed successfully.
    """

    return Message(
        message=f"User {username} active status changed successfully to {active}"
    )


def get_user_psw_change_msg(username: str) -> Message:
    """Returns a message indicating the user's password was changed successfully.

    Args:
        username (str): Username of the user.

    Returns:
        Message: Message indicating the user's password was changed successfully.
    """

    return Message(message=f"User {username} password changed successfully")


def get_bad_login_credentials_msg() -> Message:
    """Returns a message indicating the login credentials are invalid.

    Returns:
        Message: Message indicating the login credentials are invalid.
    """

    return Message(message="Could not authenticate. Invalid login credentials")


def get_incorrect_psw_msg() -> Message:
    """Returns a message indicating the password is incorrect.

    Returns:
        Message: Message indicating the password is incorrect.
    """

    return Message(message="Incorrect password")


def get_new_psw_not_same_msg() -> Message:
    """Returns a message indicating the new password is the same as the old password.

    Returns:
        Message: Message indicating the new password is the same as the old password.
    """

    return Message(message="The new password cannot be the same as the old password")


def get_email_or_username_required_msg() -> Message:
    """Returns a message indicating an email or username is required for password recovery.

    Returns:
        Message: Message indicating an email or username is required for password recovery.
    """

    return Message(message="Email or username required for password recovery")


def get_sorting_method_not_supported_msg(
    sort: str, available_sorting_choices: list[str]
) -> Message:
    """Returns a message indicating the sorting method is not supported.

    Args:
        sort (str): Sorting method.
        available_sorting_choices (list[str]): List of available sorting methods.

    Returns:
        Message: Message indicating the sorting method is not supported.
    """

    return Message(
        message=f"The sorting method {sort} is not supported, instead choose one of {available_sorting_choices}"
    )


def get_no_obj_matching_query_msg(
    filter: dict[str, str] | None, model_table_name: str
) -> Message:
    """Returns a message indicating no object matching the query was found.

    Args:
        filter (dict[str, str]): Filter used to query the object.
        model (Base): Model of the object.

    Returns:
        Message: Message indicating no object matching the query was found.
    """
    if not filter:
        return Message(
            message=f"No object matching the query in the route {model_table_name} was found."
        )

    return Message(
        message=f"No object matching the query ({', '.join([key + ': ' + str(item) for key, item in filter.items()])}) in the route {model_table_name} was found."
    )


def get_too_many_items_delete_msg(
    filter: dict[str, str], max_deletion_number: int
) -> Message:
    """Returns a message indicating too many objects matching the query were found and cannot guarantee safety.

    Args:
        filter (dict[str, str]): Filter used to query the object.
        max_deletion_number (int): Maximum number of deletions allowed.

    Returns:
        Message: Message indicating too many objects matching the query were found.
    """

    return Message(
        message=f"""Too many objects matching the query
        ({','.join([key + ': ' + str(item) for key, item in filter.items()])}),
        cannot delete and guarantee safety. Maximum of {max_deletion_number} deletions allowed."""
    )


def get_invalid_token_credentials_msg() -> Message:
    """Returns a message indicating the token credentials are invalid.

    Returns:
        Message: Message indicating the token credentials are invalid.
    """

    return Message(message="Could not validate credentials. Invalid token")


def get_password_rec_email_sent_success() -> Message:
    """Returns a message indicating the password recovery email was sent successfully.

    Returns:
        Message: Message indicating the password recovery email was sent successfully.
    """

    return Message(message="Password recovery email sent successfully")


def get_failed_send_challenge_request_error_msg(e: Exception | list[str]) -> Message:
    """Returns a message indicating the challenge request failed to send.

    Args:
        e (Exception): Exception raised when sending the challenge request.

    Returns:
        Message: Message indicating the challenge request failed to send.
    """

    return Message(
        message=f"""Failed to send challenge request to cloudflare turnstile endpoint with error: {e}"""
    )


def get_user_email_confirmation_sent(username: UsernameStr, email: EmailStr) -> Message:
    return Message(
        message=f"User creation for {username} and {email} requested. Please check your email for confirmation."
    )


def get_user_successfully_registered_msg(
    username: UsernameStr, email: EmailStr
) -> Message:
    return Message(
        message=f"User {username} successfully registered with email {email}"
    )
