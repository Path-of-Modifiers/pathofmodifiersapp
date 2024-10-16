# From FastAPI Fullstack Template https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/login.py
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_password_rec_email_sent_success_msg,
    get_user_psw_change_msg,
)
from app.api.deps import (
    UserCachePasswordResetSession,
    UserCacheSession,
    get_current_active_superuser,
    get_db,
)
from app.core.config import settings
from app.core.models.models import User
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import (
    apply_ip_rate_limits,
)
from app.core.schemas import Message, NewPassword, Token
from app.core.schemas.token import RecoverPassword
from app.core.security import (
    get_password_hash,
    verify_password,
)
from app.crud import CRUD_user
from app.exceptions import (
    BadLoginCredentialsError,
    DbObjectDoesNotExistError,
    EmailOrUsernameRequiredError,
    InvalidTokenError,
    NewPasswordIsSameError,
)
from app.utils.user import (
    generate_reset_password_email,
    send_email,
)

router = APIRouter()

login_prefix = "login"


@router.post("/access-token")
@apply_ip_rate_limits(
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_MINUTE,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_HOUR,
    rate_limit_settings.IP_LOGIN_RATE_LIMIT_DAY,
)
async def login_access_session(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_session_cache: UserCacheSession,
    db: Session = Depends(get_db),
) -> Token:
    """
    OAuth2 compatible session login.
    """
    user = CRUD_user.authenticate(
        db=db, email_or_username=form_data.username, password=form_data.password
    )

    if not user:
        raise BadLoginCredentialsError(
            function_name=login_access_session.__name__,
        )

    access_token = await user_session_cache.create_user_cache_instance(
        user=user,
        expire_seconds=settings.ACCESS_SESSION_EXPIRE_SECONDS,
    )

    return Token(
        access_token=access_token,
    )


@router.post("/password-recovery/")
@apply_ip_rate_limits(
    rate_limit_settings.RECOVERY_PASSWORD_RATE_LIMIT_SECOND,
    rate_limit_settings.RECOVERY_PASSWORD_RATE_LIMIT_MINUTE,
    rate_limit_settings.RECOVERY_PASSWORD_RATE_LIMIT_HOUR,
    rate_limit_settings.RECOVERY_PASSWORD_RATE_LIMIT_DAY,
)
async def recover_password(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    body: RecoverPassword,
    user_cache_password_reset: UserCachePasswordResetSession,
    db: Session = Depends(get_db),
) -> Message:
    """
    Password Recovery
    """
    if not body.email and not body.username:
        raise EmailOrUsernameRequiredError(
            function_name=recover_password.__name__,
        )
    get_user_filter = {}
    if body.email:
        get_user_filter["email"] = body.email
    if body.username:
        get_user_filter["username"] = body.username
    user = CRUD_user.get(db=db, filter=get_user_filter)
    if not user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=get_user_filter,
            function_name=recover_password.__name__,
        )

    password_reset_token = await user_cache_password_reset.create_user_cache_instance(
        user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    )

    if not body.email:
        email = CRUD_user.get_email_by_username(db=db, username=body.username)
    else:
        email = body.email

    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return get_password_rec_email_sent_success_msg()


@router.post("/reset-password/")
@apply_ip_rate_limits(
    rate_limit_settings.RESET_PASSWORD_RATE_LIMIT_SECOND,
    rate_limit_settings.RESET_PASSWORD_RATE_LIMIT_MINUTE,
    rate_limit_settings.RESET_PASSWORD_RATE_LIMIT_HOUR,
    rate_limit_settings.RESET_PASSWORD_RATE_LIMIT_DAY,
)
async def reset_password(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    body: NewPassword,
    user_cache_password_reset: UserCachePasswordResetSession,
    db: Session = Depends(get_db),
) -> Message:
    """
    Reset password
    """
    cached_user = await user_cache_password_reset.verify_token(token=body.token)

    email = cached_user.email
    if not email:
        raise InvalidTokenError(
            token=body.token,
            function_name=reset_password.__name__,
        )
    get_user_filter = {"email": email}
    user = CRUD_user.get(db=db, filter=get_user_filter)
    if not user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=get_user_filter,
            function_name=reset_password.__name__,
        )
    if verify_password(body.new_password, user.hashedPassword):
        raise NewPasswordIsSameError(
            function_name=reset_password.__name__,
        )
    hashed_password = get_password_hash(password=body.new_password)
    user.hashedPassword = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return get_user_psw_change_msg(user.username)


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
async def recover_password_html_content(
    email: EmailStr,
    user_cache_password_reset: UserCachePasswordResetSession,
    db: Session = Depends(get_db),
) -> Any:
    """
    HTML Content for Password Recovery
    """
    filter = {"email": email}
    user = CRUD_user.get(db=db, filter=filter)

    if not user:
        raise DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=filter,
            function_name=recover_password_html_content.__name__,
        )
    password_reset_token = await user_cache_password_reset.create_user_cache_instance(
        user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    )

    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
