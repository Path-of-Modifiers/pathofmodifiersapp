from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_password_rec_email_sent_success_msg,
    get_user_psw_change_msg,
)
from app.api.routes.login import login_prefix, reset_password
from app.core.cache.user_cache import UserCache
from app.core.config import settings
from app.core.security import verify_password
from app.crud import CRUD_user
from app.exceptions import InvalidTokenError, NewPasswordIsSameError
from app.tests.base_test import BaseTest


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
class TestLoginRoutes(BaseTest):
    @pytest.mark.anyio
    async def test_get_access_token_email(self, async_client: AsyncClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    @pytest.mark.anyio
    async def test_get_access_token_username(self, async_client: AsyncClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    @pytest.mark.anyio
    async def test_get_access_token_incorrect_password_email(
        self, async_client: AsyncClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": "incorrect",
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        assert r.status_code == 401

    @pytest.mark.anyio
    async def test_get_access_token_incorrect_password_user(
        self, async_client: AsyncClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": "incorrect",
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        assert r.status_code == 401

    @pytest.mark.anyio
    async def test_use_access_token(
        self, async_client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/test-token",
            headers=superuser_token_headers,
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    @pytest.mark.anyio
    async def test_recovery_password(
        self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        """No test email yet. Checks internal errors without sending an email"""
        with (
            patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
            patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
        ):
            email_data = {"email": "test@example.com"}
            r = await async_client.post(
                f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
                headers=normal_user_token_headers,
                json=email_data,
            )
            assert r.status_code == 200
            assert r.json() == {
                "message": get_password_rec_email_sent_success_msg().message
            }

    @pytest.mark.anyio
    async def test_recovery_password_user_not_exists_email(
        self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        email = "jVgQr@example.com"
        r = await async_client.post(
            f"{settings.API_V1_STR}/password-recovery/",
            headers=normal_user_token_headers,
            json={"email": email},
        )
        assert r.status_code == 404

    @pytest.mark.anyio
    async def test_recovery_password_user_not_exists_username(
        self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        username_data = {"username": "jVgQr"}
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
            headers=normal_user_token_headers,
            json=username_data,
        )
        assert r.status_code == 404

    @pytest.mark.anyio
    async def test_reset_password(
        self,
        async_client: AsyncClient,
        user_cache_password_reset: UserCache,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

        new_password = "the_new_password"
        token = await user_cache_password_reset.create_user_cache_instance(
            user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
        )
        new_psw_data = {"new_password": new_password, "token": token}
        r = await async_client.post(
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
        reset_token = await user_cache_password_reset.create_user_cache_instance(
            user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
        )
        old_password = settings.FIRST_SUPERUSER_PASSWORD
        old_psw_data = {"new_password": old_password, "token": reset_token}
        r = await async_client.post(
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

    @pytest.mark.anyio
    async def test_reset_same_password(
        self,
        async_client: AsyncClient,
        user_cache_password_reset: UserCache,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        new_password = settings.FIRST_SUPERUSER_PASSWORD
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        token = await user_cache_password_reset.create_user_cache_instance(
            user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
        )
        data = {"new_password": new_password, "token": token}
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 400
        assert (
            r.json()["detail"]
            == NewPasswordIsSameError(
                function_name=reset_password.__name__,
            ).detail
        )

        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        db.refresh(user)
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

    @pytest.mark.anyio
    async def test_reset_password_invalid_token(
        self,
        async_client: AsyncClient,
        user_cache_password_reset: UserCache,
        superuser_token_headers: dict[str, str],
    ) -> None:
        invalid_token = "invalid"
        data = {"new_password": "the_new_password", "token": invalid_token}
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=data,
        )
        response = r.json()
        assert "detail" in response
        assert r.status_code == 401
        assert (
            response["detail"]
            == InvalidTokenError(
                token=invalid_token,
                function_name=user_cache_password_reset.verify_token.__name__,
                class_name=user_cache_password_reset.__class__.__name__,
            ).detail
        )
