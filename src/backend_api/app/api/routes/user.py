import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_activation_token_confirmation_sent_msg,
    get_delete_return_msg,
    get_set_rate_limit_tier_success_msg,
    get_user_active_change_msg,
    get_user_psw_change_msg,
    get_user_register_confirmation_sent_msg,
    get_user_successfully_registered_msg,
    get_user_update_me_confirmation_sent_msg,
    get_user_update_me_success_msg,
)
from app.api.deps import (
    CurrentUser,
    CurrentUserNotActive,
    UserCacheRegisterSession,
    UserCacheUpdateMeSession,
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.core.config import settings
from app.core.models.models import User
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_ip_rate_limits,
    apply_user_rate_limits,
)
from app.core.schemas import (
    Message,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegisterPreEmailConfirmation,
    UsersPublic,
    UserUpdate,
)
from app.core.schemas.token import Token
from app.core.schemas.user import UserUpdateMe
from app.crud import CRUD_user
from app.exceptions import (
    DbObjectDoesNotExistError,
    InvalidTokenError,
    SuperUserNotAllowedToChangeActiveSelfError,
    SuperUserNotAllowedToDeleteSelfError,
    UserWithNotEnoughPrivilegesError,
)
from app.exceptions.model_exceptions.user_login_exception import (
    UpdateExisitingMeValuesError,
    UserEmailRequiredError,
    UserIsAlreadyActiveError,
    UserUsernameRequiredError,
)
from app.utils.user import (
    generate_email_changed_notify_email,
    generate_new_account_email,
    generate_password_changed_notify_email,
    generate_user_email_update,
    generate_user_registration_email,
    send_email,
)

router = APIRouter()

user_prefix = "user"


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def get_all_users(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve all users.
    """

    users_public = CRUD_user.get_all(db, skip=skip, limit=limit)

    return users_public


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def create(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create new user.
    """
    user = CRUD_user.create(db=db, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.username
        )
        background_tasks.add_task(
            send_email,
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch(
    "/update-me-email-pre-confirmation",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_SECOND,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_MINUTE,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_HOUR,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_DAY,
)
async def update_me_email_send_confirmation(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    *,
    db: Session = Depends(get_db),
    user_cache_update_me: UserCacheUpdateMeSession,
    user_update_me_email: UserUpdateMe,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
) -> Message:
    """
    Send confirmation to update own user.
    """
    if not user_update_me_email.email:
        raise UserEmailRequiredError(
            function_name=update_me_email_send_confirmation.__name__,
        )
    if user_update_me_email.email == current_user.email:
        raise UpdateExisitingMeValuesError(
            value=user_update_me_email.email,
            function_name=update_me_email_send_confirmation.__name__,
        )
    CRUD_user.check_exists_raise(
        db,
        filter={"email": user_update_me_email.email},
    )

    update_user_params = {"email": user_update_me_email.email}
    user_update_token = await user_cache_update_me.create_user_cache_instance(
        expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
        user=current_user,
        update_params=update_user_params,
    )
    if settings.emails_enabled:
        email_data = generate_user_email_update(
            email_to=user_update_me_email.email,
            token=user_update_token,
        )
        background_tasks.add_task(
            send_email,
            email_to=user_update_me_email.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return get_user_update_me_confirmation_sent_msg(
        email_or_username=user_update_me_email.email,
    )


@router.patch(
    "/update-me-email-confirmation",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_SECOND,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_MINUTE,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_HOUR,
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_DAY,
)
async def update_me_email_confirmation(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    token: Token,
    current_user: CurrentUser,
    user_cache_update_me: UserCacheUpdateMeSession,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Message:
    """
    Confirm update email.
    """
    cached_user_update = await user_cache_update_me.verify_token(token.access_token)
    update_email = cached_user_update.email
    if not update_email:
        raise InvalidTokenError(
            token=token.access_token,
            function_name=update_me_email_confirmation.__name__,
        )
    if update_email == current_user.email:
        raise UpdateExisitingMeValuesError(
            value=update_email,
            function_name=update_me_email_confirmation.__name__,
        )
    CRUD_user.check_exists_raise(
        db,
        filter={"email": update_email},
    )
    if settings.emails_enabled:
        email_data = generate_email_changed_notify_email(
            email_to=current_user.email,
            new_email=update_email,
            username=current_user.username,
        )
        background_tasks.add_task(
            send_email,
            email_to=current_user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    CRUD_user.update(
        db,
        user_id=current_user.userId,
        user_in=UserUpdateMe(
            email=update_email,
        ),
    )

    return get_user_update_me_success_msg(email_or_username=update_email)


@router.patch(
    "/update-me-username",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.UPDATE_ME_RATE_LIMIT_MONTH,
)
async def update_me_username(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_update_me_username: UserUpdateMe,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Message:
    """
    Update username. Can only be used by users once a month.

    TODO: Fix rate limit if route throws an error, it doesn't rate limit.
    """
    if not user_update_me_username.username:
        raise UserUsernameRequiredError(
            function_name=update_me_email_send_confirmation.__name__,
        )
    if user_update_me_username.username == current_user.username:
        raise UpdateExisitingMeValuesError(
            value=user_update_me_username.username,
            function_name=update_me_username.__name__,
        )
    CRUD_user.check_exists_raise(
        db,
        filter={"username": user_update_me_username.username},
    )
    CRUD_user.update(
        db,
        user_id=current_user.userId,
        user_in=UserUpdateMe(
            username=user_update_me_username.username,
        ),
    )

    return get_user_update_me_success_msg(
        email_or_username=user_update_me_username.username
    )


@router.patch(
    "/me/password",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.UPDATE_PASSWORD_ME_RATE_LIMIT_SECOND,
    rate_limit_settings.UPDATE_PASSWORD_ME_RATE_LIMIT_MINUTE,
    rate_limit_settings.UPDATE_PASSWORD_ME_RATE_LIMIT_HOUR,
    rate_limit_settings.UPDATE_PASSWORD_ME_RATE_LIMIT_DAY,
)
async def update_password_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    *,
    db: Session = Depends(get_db),
    body: UpdatePassword,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Update own password.
    """
    CRUD_user.update_password(
        db=db,
        db_user=current_user,
        body=body,
    )

    if settings.emails_enabled:
        email_data = generate_password_changed_notify_email(
            email_to=current_user.email,
            username=current_user.username,
        )
        background_tasks.add_task(
            send_email,
            email_to=current_user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return get_user_psw_change_msg(current_user.username)


@router.get(
    "/me",
    response_model=UserPublic,
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_user_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUserNotActive,
) -> Any:
    """
    Get current user. User doesn't have to be active (confirmed email).
    """
    return current_user


@router.delete(
    "/me",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
async def delete_user_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Message:
    """
    Delete own user.
    """
    if current_user.isSuperuser:
        raise SuperUserNotAllowedToDeleteSelfError(
            username_or_email=current_user.username,
            function_name=delete_user_me.__name__,
        )
    db.delete(current_user)
    db.commit()
    return get_delete_return_msg(
        model_table_name=User.__tablename__, filter={"userId": current_user.userId}
    )


@router.post("/signup-send-confirmation", response_model=Message)
@apply_ip_rate_limits(
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
async def register_user_send_confirmation(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_register_pre_confirmed: UserRegisterPreEmailConfirmation,
    user_cache_register_user: UserCacheRegisterSession,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Any:
    """
    Send email confirmation on user register. Account doesn't get created yet.
    """
    CRUD_user.check_exists_raise(
        db, filter={"email": user_register_pre_confirmed.email}
    )
    CRUD_user.check_exists_raise(
        db, filter={"username": user_register_pre_confirmed.username}
    )

    user_create = UserCreate(
        username=user_register_pre_confirmed.username,
        email=user_register_pre_confirmed.email,
        password=user_register_pre_confirmed.password,
        isActive=False,
    )

    user = CRUD_user.create(db=db, user_create=user_create)

    user_register_token = await user_cache_register_user.create_user_cache_instance(
        user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    )
    if settings.emails_enabled:
        email_data = generate_user_registration_email(
            email_to=user_register_pre_confirmed.email,
            username=user_register_pre_confirmed.username,
            token=user_register_token,
        )
        background_task.add_task(
            send_email,
            email_to=user_register_pre_confirmed.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return get_user_register_confirmation_sent_msg(
        email=user_register_pre_confirmed.email,
        username=user_register_pre_confirmed.username,
    )


@router.post("/signup", response_model=Message)
@apply_ip_rate_limits(
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
async def register_user_confirm(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    token: Token,
    user_cache_register_user: UserCacheRegisterSession,
    db: Session = Depends(get_db),
) -> Any:
    """
    Confirm new user without the need to be logged in. Requires email confirmation.
    """
    cached_user = await user_cache_register_user.verify_token(token.access_token)
    email = cached_user.email
    if not email:
        raise InvalidTokenError(
            token=token.access_token,
            function_name=register_user_confirm.__name__,
        )

    user_db = CRUD_user.get(db, filter={"email": email})

    user = CRUD_user.set_active(db=db, user_id=user_db.userId, active=True)

    return get_user_successfully_registered_msg(
        username=user.username, email=user.email
    )


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_user_by_id(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_id: uuid.UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    get_user_filter = {"userId": user_id}
    db_user = CRUD_user.get(db, filter=get_user_filter)
    if not db_user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=get_user_filter,
            function_name=get_user_by_id.__name__,
        )
    if db_user == current_user:
        return db_user
    if not current_user.isSuperuser:
        raise UserWithNotEnoughPrivilegesError(
            username_or_email=current_user.username,
            function_name=get_user_by_id.__name__,
        )
    return db_user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = CRUD_user.update(db=db, user_id=user_id, user_in=user_in)
    return db_user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
async def delete_user(
    current_user: CurrentUser,
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Message:
    """
    Delete a user.
    """
    delete_user_fiter = {"userId": user_id}
    db_user = CRUD_user.get(db, filter=delete_user_fiter)
    if not db_user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=delete_user_fiter,
            function_name=delete_user.__name__,
        )
    if db_user == current_user:
        raise SuperUserNotAllowedToDeleteSelfError(
            username_or_email=current_user.username,
            function_name=delete_user.__name__,
        )
    db.delete(db_user)
    db.commit()
    return get_delete_return_msg(
        model_table_name=User.__tablename__, filter=delete_user_fiter
    )


@router.patch(
    "/is_active/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
async def change_is_active_user(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
    user_id: uuid.UUID,
    is_active: bool,
    db: Session = Depends(get_db),
) -> Message:
    """
    Change activity to current user.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if not db_user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter={"userId": user_id},
            function_name=change_is_active_user.__name__,
        )
    if db_user == current_user:
        raise SuperUserNotAllowedToChangeActiveSelfError(
            username_or_email=current_user.username,
            function_name=change_is_active_user.__name__,
        )
    CRUD_user.set_active(db, user_id=user_id, active=is_active)
    return get_user_active_change_msg(db_user.username, is_active)


@router.patch(
    "/rate_limit_tier/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
async def set_rate_limit_tier_user(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_id: uuid.UUID,
    rate_limit_tier: int,
    db: Session = Depends(get_db),
) -> Message:
    """
    Set rate limit tier to current user.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if not db_user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter={"userId": user_id},
            function_name=set_rate_limit_tier_user.__name__,
        )
    user_update = UserUpdate(rateLimitTier=rate_limit_tier)
    CRUD_user.update(db=db, user_id=user_id, user_in=user_update)
    return get_set_rate_limit_tier_success_msg(db_user.username, rate_limit_tier)


@router.post("/check-current-user-active", response_model=bool)
@apply_user_rate_limits(
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
async def check_current_user_active(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUserNotActive,
) -> bool:
    """
    Checks if the current user is active. Returns True if the user is active, otherwise False.
    """
    return current_user.isActive


@router.post("/activation-token-send-confirmation", response_model=Message)
@apply_user_rate_limits(
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
async def set_active_user_send_confirmation(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_cache_register_user: UserCacheRegisterSession,
    current_user: CurrentUserNotActive,
    background_task: BackgroundTasks,
) -> Message:
    """
    Send email confirmation to set active user during registration process.
    Rute `/signup` is used to confirm the user.
    """
    if current_user.isActive:
        raise UserIsAlreadyActiveError(
            username_or_email=current_user.username,
            function_name=set_active_user_send_confirmation.__name__,
        )
    user_register_token = await user_cache_register_user.create_user_cache_instance(
        user=current_user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    )
    if settings.emails_enabled:
        email_data = generate_user_registration_email(
            email_to=current_user.email,
            username=current_user.username,
            token=user_register_token,
        )
        background_task.add_task(
            send_email,
            email_to=current_user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return get_activation_token_confirmation_sent_msg(
        email=current_user.email,
        username=current_user.username,
    )
