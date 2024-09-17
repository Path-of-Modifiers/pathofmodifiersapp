from collections.abc import Awaitable
from unittest.mock import patch

import pytest
from fastapi import Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_password_rec_email_sent_success_msg,
    get_user_psw_change_msg,
)
from app.api.routes.login import (
    login_access_session,
    login_prefix,
    recover_password,
    reset_password,
)
from app.core.cache.user_cache import UserCache
from app.core.config import settings
from app.core.models.models import User
from app.core.security import verify_password
from app.crud import CRUD_user
from app.exceptions import InvalidTokenError, NewPasswordIsSameError
from app.exceptions.model_exceptions.db_exception import DbObjectDoesNotExistError
from app.exceptions.model_exceptions.user_login_exception import (
    BadLoginCredentialsError,
)
from app.tests.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.base_test import BaseTest
from app.tests.utils.rate_limit import (
    get_function_decorator_rate_limit_per_time_interval,
)


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
        bad_login_credentials_error = BadLoginCredentialsError(
            function_name=login_access_session.__name__,
        )
        assert r.status_code == bad_login_credentials_error.status_code
        assert r.json()["detail"] == bad_login_credentials_error.detail

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
        bad_login_credentials_error = BadLoginCredentialsError(
            function_name=login_access_session.__name__,
        )
        assert r.status_code == bad_login_credentials_error.status_code
        assert r.json()["detail"] == bad_login_credentials_error.detail

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
        email_data = {"email": "jVgQr@example.com"}
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
            headers=normal_user_token_headers,
            json=email_data,
        )
        db_obj_not_exist_error = DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=email_data,
            function_name=recover_password.__name__,
        )
        assert r.status_code == db_obj_not_exist_error.status_code
        assert r.json()["detail"] == db_obj_not_exist_error.detail

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
        db_obj_not_exist_error = DbObjectDoesNotExistError(
            model_table_name=User.__tablename__,
            filter=username_data,
            function_name=recover_password.__name__,
        )
        assert r.status_code == db_obj_not_exist_error.status_code
        assert r.json()["detail"] == db_obj_not_exist_error.detail

    @pytest.mark.anyio
    async def test_reset_password(
        self,
        async_client: AsyncClient,
        get_user_cache_password_reset: UserCache,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

        new_password = "the_new_password"
        token = await get_user_cache_password_reset.create_user_cache_instance(
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
        reset_token = await get_user_cache_password_reset.create_user_cache_instance(
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
        get_user_cache_password_reset: UserCache,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        new_password = settings.FIRST_SUPERUSER_PASSWORD
        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        token = await get_user_cache_password_reset.create_user_cache_instance(
            user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
        )
        data = {"new_password": new_password, "token": token}
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
            headers=superuser_token_headers,
            json=data,
        )
        new_password_is_same_error = NewPasswordIsSameError(
            function_name=reset_password.__name__,
        )
        assert r.status_code == new_password_is_same_error.status_code
        assert r.json()["detail"] == new_password_is_same_error.detail

        user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
        db.refresh(user)
        assert user
        assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

    @pytest.mark.anyio
    async def test_reset_password_invalid_token(
        self,
        async_client: AsyncClient,
        get_user_cache_password_reset: UserCache,
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

        invalid_token_error = InvalidTokenError(
            token=invalid_token,
            function_name=get_user_cache_password_reset.verify_token.__name__,
            class_name=get_user_cache_password_reset.__class__.__name__,
        )
        assert "detail" in response
        assert r.status_code == invalid_token_error.status_code
        assert response["detail"] == invalid_token_error.detail


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestLoginRateLimitAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_login_access_token_rate_limit(
        self,
        async_client: AsyncClient,
        ip_rate_limiter,  # noqa: ARG001 # Do not remove, used to enable ip rate limiter
    ) -> None:
        """
        Test login access token rate limit.
        """

        # Create api function to test
        def post_plot_query_from_api_normal_user(
            login_data: dict[str, str],
        ) -> Awaitable[Response]:
            return async_client.post(
                f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
            )

        # Get function decorator rate limit per time interval
        rate_limits_per_interval_format = (
            get_function_decorator_rate_limit_per_time_interval(login_access_session)
        )

        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }

        await self.perform_time_interval_requests_with_api_function(
            api_function=post_plot_query_from_api_normal_user,
            all_rate_limits_per_interval=rate_limits_per_interval_format,
            login_data=login_data,
        )
