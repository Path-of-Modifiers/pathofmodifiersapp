# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_bad_login_credentials_msg,
    get_email_or_username_required_msg,
    get_invalid_token_credentials_msg,
    get_new_psw_not_same_msg,
    get_no_obj_matching_query_msg,
    get_not_active_or_auth_user_error_msg,
    get_password_rec_email_sent_success,
    get_user_psw_change_msg,
)
from app.api.deps import CurrentUser, get_current_active_superuser, get_db
from app.core import security
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import Message, NewPassword, Token, UserPublic
from app.core.schemas.token import RecoverPassword
from app.core.security import get_password_hash, verify_password
from app.crud import CRUD_user
from app.limiter import apply_user_rate_limits
from app.utils.user import (
    generate_reset_password_email,
    generate_user_confirmation_token,
    send_email,
    verify_token,
)

router = APIRouter()

login_prefix = "login"


@router.post("/access-token")
@apply_user_rate_limits(
    settings.LOGIN_RATE_LIMIT_SECOND,
    settings.LOGIN_RATE_LIMIT_MINUTE,
    settings.LOGIN_RATE_LIMIT_HOUR,
    settings.LOGIN_RATE_LIMIT_DAY,
)
def login_access_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = CRUD_user.authenticate(
        db=session, email_or_username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail=get_bad_login_credentials_msg().message
        )
    elif not user.isActive:
        raise HTTPException(
            status_code=400,
            detail=get_not_active_or_auth_user_error_msg(user.username).message,
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.userId, expires_delta=access_token_expires
        )
    )


@router.post("/test-token", response_model=UserPublic)
@apply_user_rate_limits(
    settings.LOGIN_RATE_LIMIT_SECOND,
    settings.LOGIN_RATE_LIMIT_MINUTE,
    settings.LOGIN_RATE_LIMIT_HOUR,
    settings.LOGIN_RATE_LIMIT_DAY,
)
def test_token(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    current_user: CurrentUser,
) -> Any:
    """
    Test access token

    """
    return current_user


@router.post("/password-recovery/")
@apply_user_rate_limits(
    settings.RECOVERY_PASSWORD_RATE_LIMIT_SECOND,
    settings.RECOVERY_PASSWORD_RATE_LIMIT_MINUTE,
    settings.RECOVERY_PASSWORD_RATE_LIMIT_HOUR,
    settings.RECOVERY_PASSWORD_RATE_LIMIT_DAY,
)
def recover_password(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    body: RecoverPassword,
    session: Session = Depends(get_db),
) -> Message:
    """
    Password Recovery
    """
    if not body.email and not body.username:
        raise HTTPException(
            status_code=400, detail=get_email_or_username_required_msg().message
        )
    get_user_filter = {}
    if body.email:
        get_user_filter["email"] = body.email
    if body.username:
        get_user_filter["username"] = body.username
    user = CRUD_user.get(db=session, filter=get_user_filter)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(
                get_user_filter, User.__tablename__
            ).message,
        )

    if not body.email:
        email = CRUD_user.get_email_by_username(db=session, username=body.username)
    else:
        email = body.email

    password_reset_token = generate_user_confirmation_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return get_password_rec_email_sent_success()


@router.post("/reset-password/")
@apply_user_rate_limits(
    settings.RESET_PASSWORD_RATE_LIMIT_SECOND,
    settings.RESET_PASSWORD_RATE_LIMIT_MINUTE,
    settings.RESET_PASSWORD_RATE_LIMIT_HOUR,
    settings.RESET_PASSWORD_RATE_LIMIT_DAY,
)
def reset_password(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    body: NewPassword,
    session: Session = Depends(get_db),
) -> Message:
    """
    Reset password
    """
    email = verify_token(token=body.token)
    if not email:
        raise HTTPException(
            status_code=400, detail=get_invalid_token_credentials_msg().message
        )
    get_user_filter = {"email": email}
    user = CRUD_user.get(db=session, filter=get_user_filter)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(
                get_user_filter, User.__tablename__
            ).message,
        )
    elif not user.isActive:
        raise HTTPException(
            status_code=400,
            detail=get_not_active_or_auth_user_error_msg(user.username).message,
        )
    if verify_password(body.new_password, user.hashedPassword):
        raise HTTPException(status_code=400, detail=get_new_psw_not_same_msg().message)
    hashed_password = get_password_hash(password=body.new_password)
    user.hashedPassword = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return get_user_psw_change_msg(user.username)


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(
    email: EmailStr, session: Session = Depends(get_db)
) -> Any:
    """
    HTML Content for Password Recovery
    """
    filter = {"email": email}
    user = CRUD_user.get(db=session, filter=filter)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=get_no_obj_matching_query_msg(filter, User.__tablename__).message,
        )
    password_reset_token = generate_user_confirmation_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
