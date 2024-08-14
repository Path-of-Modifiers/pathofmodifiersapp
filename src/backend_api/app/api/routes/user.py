# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
import uuid

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.core.models.models import User
from app.crud import CRUD_user
from app.core.schemas import (
    Message,
    UserPublic,
    UsersPublic,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
    UserRegister,
    UpdatePassword,
    UserInDB,
)
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
def read_users(db: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    count_statement = select(func.count()).select_from(User)
    count = db.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = db.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, db: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = CRUD_user.get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = CRUD_user.create_user(db=db, user_create=user_in)
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


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, db: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = CRUD_user.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.userId != current_user.userId:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    for field in user_data:
        if field in user_data:
            setattr(current_user, field, user_data[field])
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, db: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashedPassword):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashedPassword = hashed_password
    db.add(current_user)
    db.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(db: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    if current_user.isSuperuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    db.delete(current_user)
    db.commit()
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(db: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    print("USER IN ", user_in)
    user = CRUD_user.get_user_by_email(db=db, email=user_in.email)
    print("USER GET EMAIL ", user)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    print("USER GET EMAIL ", user)
    user = CRUD_user.create_user(db=db, user_create=user)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, db: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.isSuperuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesis_supern't have enough privileges",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    db: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = CRUD_user.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.userId != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = CRUD_user.update_user(db=db, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    db: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    db.delete(user)
    db.commit()
    return Message(message="User deleted successfully")
