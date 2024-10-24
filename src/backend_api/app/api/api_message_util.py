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
        message=f"{model_table_name} with filter {filter} was deleted successfully"
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
        message=f"User '{username}' active status changed successfully to {active}"
    )


def get_user_psw_change_msg(username: str) -> Message:
    """Returns a message indicating the user's password was changed successfully.

    Args:
        username (str): Username of the user.

    Returns:
        Message: Message indicating the user's password was changed successfully.
    """

    return Message(message=f"User '{username}' password changed successfully")


def get_password_rec_email_sent_success_msg() -> Message:
    """Returns a message indicating the password recovery email was sent successfully.

    Returns:
        Message: Message indicating the password recovery email was sent successfully.
    """

    return Message(message="Password recovery email sent successfully")


def get_user_register_confirmation_sent_msg(
    username: UsernameStr, email: EmailStr
) -> Message:
    return Message(
        message=f"User registration with username '{username}' and email '{email}' requested. Please check your email for confirmation."
    )


def get_user_successfully_registered_msg(
    username: UsernameStr, email: EmailStr
) -> Message:
    return Message(
        message=f"User '{username}' successfully registered with email '{email}'"
    )


def get_user_update_me_confirmation_sent_msg(
    email_or_username: EmailStr | UsernameStr,
) -> Message:
    return Message(
        message=f"User update with email '{email_or_username}' requested. Please check your email for confirmation."
    )


def get_user_update_me_success_msg(
    email_or_username: EmailStr | UsernameStr,
) -> Message:
    return Message(message=f"User updated successfully field to '{email_or_username}'")


def get_failed_send_challenge_request_error_msg(e: Exception | list[str]) -> Message:
    """Returns a message indicating the challenge request failed to send.

    Args:
        e (Exception): Exception raised when sending the challenge request.

    Returns:
        Message: Message indicating the challenge request failed to send.
    """

    return Message(
        message=(
            f"Failed to send challenge request to cloudflare "
            f"turnstile endpoint with error: {e}"
        )
    )


def get_set_rate_limit_tier_success_msg(username: str, rate_limit_tier: int) -> Message:
    """Returns a message indicating the rate limit tier was set successfully.

    Returns:
        Message: Message indicating the rate limit tier was set successfully.
    """

    return Message(
        message=f"User '{username}' rate limit tier set to {rate_limit_tier}"
    )


def get_activation_token_confirmation_sent_msg(
    username: UsernameStr, email: EmailStr
) -> Message:
    return Message(
        message=(
            f"Successfully sent user activation token with "
            f"username '{username}' and email '{email}'. Please check your email for confirmation."
        )
    )
