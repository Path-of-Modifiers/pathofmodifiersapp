# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from datetime import timedelta
from typing import Annotated, Any, Optional

from app.core.schemas.user import UserInDB
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import CRUD_user
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.schemas import Message, NewPassword, Token, UserPublic
from app.utils.user import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
from pydantic import EmailStr

router = APIRouter()

login_prefix = "login"


@router.post("/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = CRUD_user.authenticate(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.isActive:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.userId, expires_delta=access_token_expires
        )
    )


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/")
def recover_password(
    session: SessionDep,
    username: Optional[str] = None,
    email: Optional[EmailStr] = None,
) -> Message:
    """
    Password Recovery
    """
    if not email and not username:
        raise HTTPException(
            status_code=400, detail="Email or username required for recovery"
        )
    get_user_filter = {}
    if email:
        get_user_filter["email"] = email
    if username:
        get_user_filter["username"] = username
    user = CRUD_user.get(db=session, filter_map=get_user_filter)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email or username does not exist in the system.",
        )

    if not email:
        email = CRUD_user.get_email_by_username(db=session, username=username)

    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    get_user_filter = {"email": email}
    user = CRUD_user.get(db=session, filter_map=get_user_filter)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.isActive:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    setattr(user, "hashedPassword", hashed_password)
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: EmailStr, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    filter_map = {"email": email}
    user = CRUD_user.get(db=session, filter_map=filter_map)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
