from dataclasses import dataclass
from pathlib import Path
from typing import Any

import emails  # type: ignore
from jinja2 import Template
from pydantic import EmailStr

from app.core.config import settings
from app.logs.logger import logger


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: EmailStr,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "No provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)

    logger.debug(f"Send email result: {response}")


def generate_test_email(email_to: EmailStr) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(
    email_to: EmailStr, email: str, token: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS // 3600,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_user_registration_email(
    email_to: EmailStr, username: str, token: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Activate account for user {username}"
    link = f"{settings.server_host}/activate-account?token={token}"
    html_content = render_email_template(
        template_name="register_user.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS // 3600,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_user_email_update(email_to: EmailStr, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Update user email information for user {email_to}"
    link = f"{settings.server_host}/update-user-email?token={token}"
    html_content = render_email_template(
        template_name="update_user.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS // 3600,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(email_to: EmailStr, username: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_email_changed_notify_email(
    email_to: EmailStr, new_email: EmailStr, username: str
) -> EmailData:
    """Sent to the old email after a user updates their email"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Email changed for user {username}"
    html_content = render_email_template(
        template_name="email_changed_notify.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "new_email": new_email,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_changed_notify_email(
    email_to: EmailStr, username: str
) -> EmailData:
    """Sent to email after a user updates their password"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password changed for user {username}"
    html_content = render_email_template(
        template_name="password_changed_notify.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)
