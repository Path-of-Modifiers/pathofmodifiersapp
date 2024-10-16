import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.api.routes.check_token import check_token_prefix
from app.core.cache.user_cache import UserCache, UserCacheTokenType
from app.core.config import settings
from app.crud import CRUD_user
from app.exceptions.model_exceptions.request_exception import InvalidTokenError
from app.tests.test_simulating_env.base_test import BaseTest


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
class TestCheckTokenRoutes(BaseTest):
    @pytest.mark.anyio
    async def test_use_access_token(
        self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-access-token",
            headers=normal_user_token_headers,
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    @pytest.mark.anyio
    async def test_use_wrong_access_token(
        self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        wrong_normal_user_token_headers = {
            **normal_user_token_headers,
            "Authorization": "Bearer wrong_token",
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-access-token",
            headers=wrong_normal_user_token_headers,
        )
        result = r.json()
        user_cache_access_session = UserCache(UserCacheTokenType.ACCESS_SESSION)
        invalid_token_error = InvalidTokenError(
            token="wrong_token",
            function_name=user_cache_access_session.verify_token.__name__,
            class_name=user_cache_access_session.__class__.__name__,
        )
        assert r.status_code == invalid_token_error.status_code
        assert result["detail"] == invalid_token_error.detail

    @pytest.mark.anyio
    async def test_check_register_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_register_user: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        register_token = await user_cache_register_user.create_user_cache_instance(
            expire_seconds=5, user=normal_user
        )
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-register-token",
            headers=normal_user_token_headers,
            params={"register_token": register_token},
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    @pytest.mark.anyio
    async def test_use_wrong_check_register_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_register_user: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        wrong_register_token = (
            await user_cache_register_user.create_user_cache_instance(
                expire_seconds=5, user=normal_user
            )
            + "wrong"
        )
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-register-token",
            headers=normal_user_token_headers,
            params={"register_token": wrong_register_token},
        )
        user_cache_register_session = UserCache(UserCacheTokenType.REGISTER_USER)
        invalid_token_error = InvalidTokenError(
            token=wrong_register_token,
            function_name=user_cache_register_session.verify_token.__name__,
            class_name=user_cache_register_session.__class__.__name__,
        )
        result = r.json()
        assert r.status_code == invalid_token_error.status_code
        assert result["detail"] == invalid_token_error.detail

    @pytest.mark.anyio
    async def test_check_password_reset_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_password_reset: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        password_reset_token = (
            await user_cache_password_reset.create_user_cache_instance(
                expire_seconds=5, user=normal_user
            )
        )
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-password-reset-token",
            headers=normal_user_token_headers,
            params={"password_reset_token": password_reset_token},
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    @pytest.mark.anyio
    async def test_use_wrong_check_password_reset_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_password_reset: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        wrong_password_reset_token = (
            await user_cache_password_reset.create_user_cache_instance(
                expire_seconds=5, user=normal_user
            )
        ) + "wrong"
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-password-reset-token",
            headers=normal_user_token_headers,
            params={"password_reset_token": wrong_password_reset_token},
        )
        result = r.json()
        user_cache_password_reset_session = UserCache(UserCacheTokenType.PASSWORD_RESET)
        invalid_token_error = InvalidTokenError(
            token=wrong_password_reset_token,
            function_name=user_cache_password_reset_session.verify_token.__name__,
            class_name=user_cache_password_reset_session.__class__.__name__,
        )
        assert r.status_code == invalid_token_error.status_code
        assert result["detail"] == invalid_token_error.detail

    @pytest.mark.anyio
    async def test_check_update_me_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_update_me: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        update_me_token = await user_cache_update_me.create_user_cache_instance(
            expire_seconds=5, user=normal_user
        )
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-update-me-token",
            headers=normal_user_token_headers,
            params={"update_me_token": update_me_token},
        )
        result = r.json()
        assert r.status_code == 200
        assert "email" in result
        assert "username" in result

    @pytest.mark.anyio
    async def test_use_wrong_check_update_me_token(
        self,
        db: Session,
        async_client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        user_cache_update_me: UserCache,
    ) -> None:
        normal_user = CRUD_user.get(
            db=db,
            filter={"email": settings.TEST_USER_EMAIL},
        )
        wrong_update_me_token = (
            await user_cache_update_me.create_user_cache_instance(
                expire_seconds=5, user=normal_user
            )
            + "wrong"
        )
        r = await async_client.post(
            f"{settings.API_V1_STR}/{check_token_prefix}/check-update-me-token",
            headers=normal_user_token_headers,
            params={"update_me_token": wrong_update_me_token},
        )
        result = r.json()
        user_cache_password_reset_session = UserCache(UserCacheTokenType.UPDATE_ME)
        invalid_token_error = InvalidTokenError(
            token=wrong_update_me_token,
            function_name=user_cache_password_reset_session.verify_token.__name__,
            class_name=user_cache_password_reset_session.__class__.__name__,
        )
        assert r.status_code == invalid_token_error.status_code
        assert result["detail"] == invalid_token_error.detail

    # @pytest.mark.anyio
    # async def test_get_access_token_email(self, async_client: AsyncClient) -> None:
    #     login_data = {
    #         "username": settings.FIRST_SUPERUSER,
    #         "password": settings.FIRST_SUPERUSER_PASSWORD,
    #     }
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
    #     )
    #     tokens = r.json()
    #     assert r.status_code == 200
    #     assert "access_token" in tokens
    #     assert tokens["access_token"]

    # @pytest.mark.anyio
    # async def test_get_access_token_username(self, async_client: AsyncClient) -> None:
    #     login_data = {
    #         "username": settings.FIRST_SUPERUSER_USERNAME,
    #         "password": settings.FIRST_SUPERUSER_PASSWORD,
    #     }
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/login/access-token", data=login_data
    #     )
    #     tokens = r.json()
    #     assert r.status_code == 200
    #     assert "access_token" in tokens
    #     assert tokens["access_token"]

    # @pytest.mark.anyio
    # async def test_get_access_token_incorrect_password_email(
    #     self, async_client: AsyncClient
    # ) -> None:
    #     login_data = {
    #         "username": settings.FIRST_SUPERUSER,
    #         "password": "incorrect",
    #     }
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
    #     )
    #     assert r.status_code == 401

    # @pytest.mark.anyio
    # async def test_get_access_token_incorrect_password_user(
    #     self, async_client: AsyncClient
    # ) -> None:
    #     login_data = {
    #         "username": settings.FIRST_SUPERUSER_USERNAME,
    #         "password": "incorrect",
    #     }
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/login/access-token", data=login_data
    #     )
    #     assert r.status_code == 401

    # @pytest.mark.anyio
    # async def test_use_access_token(
    #     self, async_client: AsyncClient, superuser_token_headers: dict[str, str]
    # ) -> None:
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/test-access-token",
    #         headers=superuser_token_headers,
    #     )
    #     result = r.json()
    #     assert r.status_code == 200
    #     assert "email" in result
    #     assert "username" in result

    # @pytest.mark.anyio
    # async def test_recovery_password(
    #     self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    # ) -> None:
    #     """No test email yet. Checks internal errors without sending an email"""
    #     with (
    #         patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
    #         patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    #     ):
    #         email_data = {"email": "test@example.com"}
    #         r = await async_client.post(
    #             f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
    #             headers=normal_user_token_headers,
    #             json=email_data,
    #         )
    #         assert r.status_code == 200
    #         assert r.json() == {
    #             "message": get_password_rec_email_sent_success_msg().message
    #         }

    # @pytest.mark.anyio
    # async def test_recovery_password_user_not_exists_email(
    #     self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    # ) -> None:
    #     email = "jVgQr@example.com"
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/password-recovery/",
    #         headers=normal_user_token_headers,
    #         json={"email": email},
    #     )
    #     assert r.status_code == 404

    # @pytest.mark.anyio
    # async def test_recovery_password_user_not_exists_username(
    #     self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    # ) -> None:
    #     username_data = {"username": "jVgQr"}
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/password-recovery/",
    #         headers=normal_user_token_headers,
    #         json=username_data,
    #     )
    #     assert r.status_code == 404

    # @pytest.mark.anyio
    # async def test_reset_password(
    #     self,
    #     async_client: AsyncClient,
    #     user_cache_password_reset: UserCache,
    #     superuser_token_headers: dict[str, str],
    #     db: Session,
    # ) -> None:
    #     user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
    #     assert user
    #     assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

    #     new_password = "the_new_password"
    #     token = await user_cache_password_reset.create_user_cache_instance(
    #         user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    #     )
    #     new_psw_data = {"new_password": new_password, "token": token}
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
    #         headers=superuser_token_headers,
    #         json=new_psw_data,
    #     )
    #     assert r.status_code == 200
    #     assert r.json() == {
    #         "message": get_user_psw_change_msg(
    #             settings.FIRST_SUPERUSER_USERNAME
    #         ).message
    #     }
    #     user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
    #     db.refresh(user)
    #     assert user
    #     assert verify_password(new_password, user.hashedPassword)

    #     # Reset password back to original
    #     reset_token = await user_cache_password_reset.create_user_cache_instance(
    #         user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    #     )
    #     old_password = settings.FIRST_SUPERUSER_PASSWORD
    #     old_psw_data = {"new_password": old_password, "token": reset_token}
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
    #         headers=superuser_token_headers,
    #         json=old_psw_data,
    #     )
    #     assert r.status_code == 200
    #     assert r.json() == {
    #         "message": get_user_psw_change_msg(
    #             settings.FIRST_SUPERUSER_USERNAME
    #         ).message
    #     }

    #     user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
    #     db.refresh(user)
    #     assert user
    #     assert verify_password(old_password, user.hashedPassword)

    # @pytest.mark.anyio
    # async def test_reset_same_password(
    #     self,
    #     async_client: AsyncClient,
    #     user_cache_password_reset: UserCache,
    #     superuser_token_headers: dict[str, str],
    #     db: Session,
    # ) -> None:
    #     new_password = settings.FIRST_SUPERUSER_PASSWORD
    #     user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
    #     token = await user_cache_password_reset.create_user_cache_instance(
    #         user=user, expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS
    #     )
    #     data = {"new_password": new_password, "token": token}
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
    #         headers=superuser_token_headers,
    #         json=data,
    #     )
    #     assert r.status_code == 400
    #     assert (
    #         r.json()["detail"]
    #         == NewPasswordIsSameError(
    #             function_name=reset_password.__name__,
    #         ).detail
    #     )

    #     user = CRUD_user.get(db, filter={"email": settings.FIRST_SUPERUSER})
    #     db.refresh(user)
    #     assert user
    #     assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.hashedPassword)

    # @pytest.mark.anyio
    # async def test_reset_password_invalid_token(
    #     self,
    #     async_client: AsyncClient,
    #     user_cache_password_reset: UserCache,
    #     superuser_token_headers: dict[str, str],
    # ) -> None:
    #     invalid_token = "invalid"
    #     data = {"new_password": "the_new_password", "token": invalid_token}
    #     r = await async_client.post(
    #         f"{settings.API_V1_STR}/{login_prefix}/reset-password/",
    #         headers=superuser_token_headers,
    #         json=data,
    #     )
    #     response = r.json()
    #     assert "detail" in response
    #     assert r.status_code == 401
    #     assert (
    #         response["detail"]
    #         == InvalidTokenError(
    #             token=invalid_token,
    #             function_name=user_cache_password_reset.verify_token.__name__,
    #             class_name=user_cache_password_reset.__class__.__name__,
    #         ).detail
    #     )
