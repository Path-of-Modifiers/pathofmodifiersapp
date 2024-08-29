# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_delete_return_msg,
    get_invalid_token_credentials_msg,
    get_no_obj_matching_query_msg,
    get_not_superuser_auth_msg,
    get_superuser_not_allowed_change_active_self_msg,
    get_superuser_not_allowed_delete_self_msg,
    get_user_active_change_msg,
    get_user_email_confirmation_sent,
    get_user_psw_change_msg,
    get_user_successfully_registered_msg,
)
from app.api.deps import (
    CurrentUser,
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import (
    Message,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.core.schemas.user import (
    UserRegisterPostEmailConfirmation,
    UserRegisterPreEmailConfirmation,
)
from app.crud import CRUD_user
from app.limiter import (
    apply_ip_rate_limits,
    apply_user_rate_limits,
)
from app.utils.user import (
    generate_new_account_email,
    generate_user_confirmation_token,
    generate_user_registration_email,
    send_email,
    verify_token,
)

router = APIRouter()

user_prefix = "user"


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def get_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all users.
    """

    users_public = CRUD_user.get_all(db, skip=skip, limit=limit)

    return users_public


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = CRUD_user.create(db=db, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.username
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch(
    "/me",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.UPDATE_ME_RATE_LIMIT_SECOND,
    settings.UPDATE_ME_RATE_LIMIT_MINUTE,
    settings.UPDATE_ME_RATE_LIMIT_HOUR,
    settings.UPDATE_ME_RATE_LIMIT_DAY,
)
def update_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdateMe,
    current_user: CurrentUser,
) -> Any:
    """
    Update own user.
    """

    CRUD_user.update(db=db, user_id=current_user.userId, user_in=user_in)

    return current_user


@router.patch(
    "/me/password",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.UPDATE_PASSWORD_ME_RATE_LIMIT_SECOND,
    settings.UPDATE_PASSWORD_ME_RATE_LIMIT_MINUTE,
    settings.UPDATE_PASSWORD_ME_RATE_LIMIT_HOUR,
    settings.UPDATE_PASSWORD_ME_RATE_LIMIT_DAY,
)
def update_password_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    *,
    db: Session = Depends(get_db),
    body: UpdatePassword,
    current_user: CurrentUser,
) -> Any:
    """
    Update own password.
    """
    CRUD_user.update_password(
        db=db,
        db_user=current_user,
        body=body,
    )

    return get_user_psw_change_msg(current_user.username)


@router.get(
    "/me",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
def get_user_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete(
    "/me",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
def delete_user_me(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Message:
    """
    Delete own user.
    """
    if current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=get_superuser_not_allowed_delete_self_msg(
                current_user.username
            ).message,
        )
    db.delete(current_user)
    db.commit()
    return get_delete_return_msg(
        model_table_name=User.__tablename__, filter={"userId": current_user.userId}
    )


@router.post("/signup-send-confirmation", response_model=Message)
@apply_ip_rate_limits(
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
def register_user_send_confirmation(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_pre_confirmed: UserRegisterPreEmailConfirmation,
    db: Session = Depends(get_db),
) -> Any:
    """
    Send email confirmation on user register. Account doesn't get created yet.
    """
    CRUD_user.check_exists_raise(
        db, filter={"email": user_pre_confirmed.email}, user_in=user_pre_confirmed
    )
    CRUD_user.check_exists_raise(
        db, filter={"username": user_pre_confirmed.username}, user_in=user_pre_confirmed
    )

    user_create = UserCreate(
        username=user_pre_confirmed.username,
        email=user_pre_confirmed.email,
        password=user_pre_confirmed.password,
        isActive=False,
    )

    CRUD_user.create(db=db, user_create=user_create)

    user_register_token = generate_user_confirmation_token(
        email=user_pre_confirmed.email
    )
    email_data = generate_user_registration_email(
        email_to=user_pre_confirmed.email,
        username=user_pre_confirmed.username,
        token=user_register_token,
    )
    send_email(
        email_to=user_pre_confirmed.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

    return get_user_email_confirmation_sent(user=user_pre_confirmed)


@router.post("/signup", response_model=Message)
@apply_ip_rate_limits(
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
def register_user(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_register_confirmation: UserRegisterPostEmailConfirmation,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new user without the need to be logged in. Requires email confirmation.
    """
    email = verify_token(token=user_register_confirmation.token)
    if not email:
        raise HTTPException(
            status_code=400, detail=get_invalid_token_credentials_msg().message
        )

    user_db = CRUD_user.get(db, filter={"email": email})

    user = CRUD_user.set_active(db=db, db_user=user_db, active=True)

    return get_user_successfully_registered_msg(
        username=user.username, email=user.email
    )


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
def get_user_by_id(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    user_id: uuid.UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(
                {"userId": user_id}, User.__tablename__
            ).message,
        )
    if db_user == current_user:
        return db_user
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=get_not_superuser_auth_msg(current_user.username).message,
        )
    return db_user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update(
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


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    current_user: CurrentUser,
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Message:
    """
    Delete a user.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(
                {"userId": user_id}, User.__tablename__
            ).message,
        )
    if db_user == current_user:
        raise HTTPException(
            status_code=403,
            detail=get_superuser_not_allowed_delete_self_msg(
                current_user.username
            ).message,
        )
    db.delete(db_user)
    db.commit()
    return get_delete_return_msg(
        model_table_name=User.__tablename__, filter={"userId": user_id}
    )


@router.patch(
    "/activate/{user_id}",
    dependencies=[Depends(get_current_active_user)],
)
@apply_user_rate_limits(
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_SECOND,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_HOUR,
    settings.STRICT_DEFAULT_USER_RATE_LIMIT_DAY,
)
def change_activate_user(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
    user_id: uuid.UUID,
    activate: bool,
    db: Session = Depends(get_db),
) -> Message:
    """
    Change activity to current user.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if db_user == current_user and not current_user.isSuperuser:
        CRUD_user.set_active(db=db, db_user=db_user, active=activate)
        return Message(
            message=get_user_active_change_msg(db_user.username, activate),
        )
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail=get_not_superuser_auth_msg(current_user.username).message,
        )
    if db_user == current_user:
        raise HTTPException(
            status_code=403,
            detail=get_superuser_not_allowed_change_active_self_msg(
                current_user.username
            ).message,
        )
    CRUD_user.set_active(db=db, db_user=db_user, active=activate)
    return Message(
        message=get_user_active_change_msg(db_user.username, activate),
    )
