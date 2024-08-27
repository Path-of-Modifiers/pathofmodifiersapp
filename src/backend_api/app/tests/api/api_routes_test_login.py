from unittest.mock import patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_invalid_token_credentials_msg,
    get_new_psw_not_same_msg,
    get_password_rec_email_sent_success,
    get_user_psw_change_msg,
)
from app.api.routes.login import login_prefix
from app.core.config import settings
from app.core.security import verify_password
from app.crud import CRUD_user
from app.tests.base_test import BaseTest
from app.utils.user import generate_password_reset_token


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestLoginRoutes(BaseTest):
    def _reset_password_client(
        self,
        reset_psw_client: TestClient,
        *,
        headers: dict[str, str],
        token: str,
        new_password: str,
    ) -> Response:
        pass

    def test_get_access_token_email(self, client: TestClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    def test_get_access_token_username(self, client: TestClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    def test_get_access_token_incorrect_password_email(
        self, client: TestClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": "incorrect",
        }
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        assert r.status_code == 400

    def test_get_access_token_incorrect_password_user(self, client: TestClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": "incorrect",
        }
        r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
        assert r.status_code == 400

    def test_use_access_token(
        self, client: TestClient, superuser_token_headers: dict[str, str]
    ) -> None:
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/test-token",
            headers=superuser_token_headers,
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    def test_recovery_password(
        self, client: TestClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        with (
            patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
            patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
        ):
            email_data = {"email": "test@example.com"}
            r = client.post(
                f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
                headers=normal_user_token_headers,
                json=email_data,
            )
            assert r.status_code == 200
            assert r.json() == {
                "message": get_password_rec_email_sent_success().message
            }

    def test_recovery_password_user_not_exists_email(
        self, client: TestClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        email = "jVgQr@example.com"
        r = client.post(
            f"{settings.API_V1_STR}/password-recovery/",
            headers=normal_user_token_headers,
            json={"email": email},
        )
        assert r.status_code == 404

    def test_recovery_password_user_not_exists_username(
        self, client: TestClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        username_data = {"username": "jVgQr"}
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
            headers=normal_user_token_headers,
            json=username_data,
        )
        assert r.status_code == 404

    def test_reset_password(
        self, client: TestClient, superuser_token_headers: dict[str, str], db: Session
    ) -> None:
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

        new_password = "the_new_password"
        token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
        new_psw_data = {"new_password": new_password, "token": token}
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=new_psw_data,
        )
        assert r.status_code == 200
        assert r.json() == {
            "message": get_user_psw_change_msg(
                settings.FIRST_SUPERUSER_USERNAME
            ).message
        }
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        db.refresh(user)
        assert user
        assert verify_password(new_password, user.hashedPassword)

        # Reset password back to original
        reset_token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
        old_password = settings.FIRST_SUPERUSER_PASSWORD
        old_psw_data = {"new_password": old_password, "token": reset_token}
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=old_psw_data,
        )
        assert r.status_code == 200
        assert r.json() == {
            "message": get_user_psw_change_msg(
                settings.FIRST_SUPERUSER_USERNAME
            ).message
        }

        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        db.refresh(user)
        assert user
        assert verify_password(old_password, user.hashedPassword)

    def test_reset_same_password(
        self, client: TestClient, superuser_token_headers: dict[str, str], db: Session
    ) -> None:
        new_password = settings.FIRST_SUPERUSER_PASSWORD
        token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
        data = {"new_password": new_password, "token": token}
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 400
        assert r.json() == {"detail": get_new_psw_not_same_msg().message}

        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        db.refresh(user)
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

    def test_reset_password_invalid_token(
        self, client: TestClient, superuser_token_headers: dict[str, str], db: Session
    ) -> None:
        data = {"new_password": "the_new_password", "token": "invalid"}
        r = client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=data,
        )
        response = r.json()
        assert "detail" in response
        assert r.status_code == 400
        assert response["detail"] == get_invalid_token_credentials_msg().message