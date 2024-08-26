# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.api_message_util import (
    get_delete_return_msg,
    get_no_obj_matching_query_msg,
    get_not_superuser_auth_msg,
    get_superuser_not_allowed_change_active_self_msg,
    get_superuser_not_allowed_delete_self_msg,
    get_user_active_change_msg,
    get_user_psw_change_msg,
)
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
    get_current_active_user,
)
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import (
    Message,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.crud import CRUD_user
from app.utils.user import (
    generate_new_account_email,
    send_email,
)

router = APIRouter()

user_prefix = "user"


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def get_all(db: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all users.
    """

    users_public = CRUD_user.get_all(db, skip=skip, limit=limit)

    return users_public


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create(*, db: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = CRUD_user.create(db=db, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
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
def update_me(
    *, db: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
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
def update_password_me(
    *, db: SessionDep, body: UpdatePassword, current_user: CurrentUser
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
def get_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete(
    "/me",
    response_model=Message,
    dependencies=[Depends(get_current_active_user)],
)
def delete_user_me(db: SessionDep, current_user: CurrentUser) -> Message:
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


@router.post("/signup", response_model=UserPublic)
def register_user(db: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user_create = UserCreate(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
    )

    user = CRUD_user.create(db=db, user_create=user_create)
    return user


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
def get_user_by_id(
    user_id: uuid.UUID, db: SessionDep, current_user: CurrentUser
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
    db: SessionDep,
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
    db: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
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
def change_activate_user(
    db: SessionDep,
    current_user: CurrentUser,
    user_id: uuid.UUID,
    activate: bool,
) -> Message:
    """
    Change activity to current user.
    """
    db_user = CRUD_user.get(db, filter={"userId": user_id})
    if db_user == current_user:
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
