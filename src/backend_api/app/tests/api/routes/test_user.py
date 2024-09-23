import time
import uuid
from collections.abc import Awaitable
from unittest.mock import patch

import pytest
from fastapi import Response
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_delete_return_msg,
    get_user_psw_change_msg,
    get_user_register_confirmation_sent_msg,
    get_user_successfully_registered_msg,
    get_user_update_me_confirmation_sent_msg,
    get_user_update_me_success_msg,
)
from app.api.deps import get_current_active_superuser, get_current_user
from app.api.routes import user_prefix
from app.api.routes.user import (
    delete_user,
    delete_user_me,
    get_user_by_id,
    register_user_send_confirmation,
)
from app.core.cache.user_cache import UserCache
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import UserCreate
from app.core.security import verify_password
from app.crud import CRUD_user
from app.exceptions import (
    DbObjectAlreadyExistsError,
    DbObjectDoesNotExistError,
    InvalidPasswordError,
    InvalidTokenError,
    NewPasswordIsSameError,
    SuperUserNotAllowedToDeleteSelfError,
    UserIsNotActiveError,
    UserWithNotEnoughPrivilegesError,
)
from app.tests.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.base_test import BaseTest
from app.tests.utils.rate_limit import (
    get_function_decorator_rate_limit_per_time_interval,
)
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
class TestUserAPI(BaseTest):
    @pytest.mark.anyio
    async def _get_current_normal_user(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        db: Session,
    ) -> User:
        get_normal_user_response = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/me",
            headers=normal_user_token_headers,
        )
        normal_user_id = get_normal_user_response.json()["userId"]
        normal_user = db.get(User, normal_user_id)
        return normal_user

    @pytest.mark.anyio
    async def test_get_users_superuser_me(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/me", headers=superuser_token_headers
        )
        current_user = r.json()
        assert current_user
        assert current_user["isActive"]
        assert current_user["isSuperuser"]
        assert current_user["email"] == settings.FIRST_SUPERUSER
        assert current_user["username"] == settings.FIRST_SUPERUSER_USERNAME

    @pytest.mark.anyio
    async def test_get_users_normal_user_me(
        self, client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/me", headers=normal_user_token_headers
        )
        current_user = r.json()
        assert current_user
        assert current_user["isActive"]
        assert current_user["isSuperuser"] is False
        assert current_user["email"] == settings.TEST_USER_EMAIL
        assert current_user["username"] == settings.TEST_USER_USERNAME

    @pytest.mark.anyio
    async def test_create_user_new_email(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        with (
            patch("app.utils.user.send_email", return_value=None),
            patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
            patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
        ):
            email = random_email()
            password = random_lower_string()
            username = random_lower_string()
            data = {"email": email, "password": password, "username": username}
            r = await client.post(
                f"{settings.API_V1_STR}/{user_prefix}/",
                headers=superuser_token_headers,
                json=data,
            )
            assert 200 <= r.status_code < 300
            created_user = r.json()
            user = CRUD_user.get(db=db, filter={"email": email})
            assert user
            assert user.email == created_user["email"]
            assert user.username == created_user["username"]

    @pytest.mark.anyio
    async def test_get_existing_user(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        user_id = user.userId
        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=superuser_token_headers,
        )
        assert 200 <= r.status_code < 300
        api_user = r.json()
        existing_user = CRUD_user.get(db=db, filter={"email": email})
        assert existing_user
        assert existing_user.email == api_user["email"]
        assert existing_user.username == api_user["username"]

    @pytest.mark.anyio
    async def test_get_existing_user_current_user(
        self, client: AsyncClient, db: Session
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        user_id = user.userId

        login_data = {
            "email": email,
            "password": password,
            "username": username,
        }
        r = await client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        a_token = tokens["access_token"]
        headers = {"Authorization": f"Bearer {a_token}"}

        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=headers,
        )
        assert 200 <= r.status_code < 300
        api_user = r.json()
        existing_user = CRUD_user.get(db=db, filter={"email": email})
        assert existing_user
        assert existing_user.email == api_user["email"]
        assert existing_user.username == api_user["username"]

    @pytest.mark.anyio
    async def test_get_existing_user_permissions_error(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        # Create a user
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        user_id = user.userId

        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 403
        assert (
            r.json()["detail"]
            == UserWithNotEnoughPrivilegesError(
                username_or_email=settings.TEST_USER_USERNAME,
                function_name=get_user_by_id.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_create_user_existing_email(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        CRUD_user.create(db=db, user_create=user_in)
        data = {"email": email, "password": password, "username": username}
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/",
            headers=superuser_token_headers,
            json=data,
        )
        created_user = r.json()
        assert r.status_code == 409
        assert "userId" not in created_user

    @pytest.mark.anyio
    async def test_create_user_existing_username(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        CRUD_user.create(db=db, user_create=user_in)
        data = {"email": random_email(), "password": password, "username": username}
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/",
            headers=superuser_token_headers,
            json=data,
        )
        created_user = r.json()
        assert r.status_code == 409
        assert "userId" not in created_user

    @pytest.mark.anyio
    async def test_create_user_by_normal_user(
        self, client: AsyncClient, normal_user_token_headers: dict[str, str]
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/",
            headers=normal_user_token_headers,
            json=data,
        )
        assert r.status_code == 403

    @pytest.mark.anyio
    async def test_retrieve_users(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        CRUD_user.create(db=db, user_create=user_in)

        email2 = random_email()
        password2 = random_lower_string()
        username2 = random_lower_string()
        user_in2 = UserCreate(email=email2, password=password2, username=username2)
        CRUD_user.create(db=db, user_create=user_in2)

        r = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/", headers=superuser_token_headers
        )
        all_users = r.json()

        assert len(all_users["data"]) > 1
        assert "count" in all_users
        for item in all_users["data"]:
            assert "email" in item
            assert "username" in item

    @pytest.mark.anyio
    async def test_update_me_email(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        superuser_token_headers: dict[str, str],
        db: Session,
        user_cache_update_me: UserCache,
    ) -> None:
        normal_user = await self._get_current_normal_user(
            client, normal_user_token_headers, db
        )
        update_email = random_email()
        update_data = {"email": update_email}
        r_pre_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-email-pre-confirmation",
            headers=normal_user_token_headers,
            json=update_data,
        )
        detail_pre_confirm = r_pre_confirm.json()["message"]
        assert r_pre_confirm.status_code == 200
        assert (
            detail_pre_confirm
            == get_user_update_me_confirmation_sent_msg(update_email).message
        )
        assert normal_user.email != update_data["email"]

        user_update_email_token = await user_cache_update_me.create_user_cache_instance(
            user=normal_user,
            expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
            update_params=update_data,
        )
        data_confirm = {"access_token": user_update_email_token}
        r_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-email-confirmation",
            headers=normal_user_token_headers,
            json=data_confirm,
        )
        details_confirm = r_confirm.json()["message"]
        assert r_confirm.status_code == 200
        assert details_confirm == get_user_update_me_success_msg(update_email).message
        db.refresh(normal_user)
        assert settings.TEST_USER_EMAIL != normal_user.email

        # turn email back to settings.TEST_USER_EMAIL with superuser headers
        update_data = {"email": settings.TEST_USER_EMAIL}
        r_pre_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{normal_user.userId}",
            headers=superuser_token_headers,
            json=update_data,
        )
        assert r_pre_confirm.status_code == 200

    @pytest.mark.anyio
    async def test_update_me_username(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        superuser_token_headers: dict[str, str],
        db: Session,
        user_cache_update_me: UserCache,
    ) -> None:
        normal_user = await self._get_current_normal_user(
            client, normal_user_token_headers, db
        )
        update_username = random_lower_string()
        update_data = {"username": update_username}
        r_pre_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-username-pre-confirmation",
            headers=normal_user_token_headers,
            json=update_data,
        )
        detail_pre_confirm = r_pre_confirm.json()["message"]
        assert r_pre_confirm.status_code == 200
        assert (
            detail_pre_confirm
            == get_user_update_me_confirmation_sent_msg(update_username).message
        )
        assert normal_user.username != update_data["username"]

        user_update_username_token = (
            await user_cache_update_me.create_user_cache_instance(
                user=normal_user,
                expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
                update_params=update_data,
            )
        )
        data_confirm = {"access_token": user_update_username_token}
        r_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-username-confirmation",
            headers=normal_user_token_headers,
            json=data_confirm,
        )
        details_confirm = r_confirm.json()["message"]
        assert r_confirm.status_code == 200
        assert (
            details_confirm == get_user_update_me_success_msg(update_username).message
        )
        db.refresh(normal_user)
        assert settings.TEST_USER_USERNAME != normal_user.username

        # turn username back to settings.TEST_USER_USERNAME with superuser headers
        update_data = {"username": settings.TEST_USER_USERNAME}
        r_pre_confirm = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{normal_user.userId}",
            headers=superuser_token_headers,
            json=update_data,
        )
        db.refresh(normal_user)
        assert r_pre_confirm.status_code == 200

    @pytest.mark.anyio
    async def test_update_password_me(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        new_password = random_lower_string()
        data = {
            "current_password": settings.FIRST_SUPERUSER_PASSWORD,
            "new_password": new_password,
        }
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/me/password",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 200
        updated_user = r.json()
        assert (
            updated_user["message"]
            == get_user_psw_change_msg(settings.FIRST_SUPERUSER_USERNAME).message
        )

        user_db = CRUD_user.get(db=db, filter={"email": settings.FIRST_SUPERUSER})
        assert user_db
        assert user_db.email == settings.FIRST_SUPERUSER
        assert user_db.username == settings.FIRST_SUPERUSER_USERNAME
        assert verify_password(new_password, user_db.hashedPassword)

        # Revert to the old password to keep consistency in test
        old_data = {
            "current_password": new_password,
            "new_password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/me/password",
            headers=superuser_token_headers,
            json=old_data,
        )
        db.refresh(user_db)

        assert r.status_code == 200
        assert verify_password(
            settings.FIRST_SUPERUSER_PASSWORD, user_db.hashedPassword
        )

    @pytest.mark.anyio
    async def test_update_password_me_incorrect_password(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        new_password = random_lower_string()
        data = {"current_password": new_password, "new_password": new_password}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/me/password",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 401
        updated_user = r.json()
        assert (
            updated_user["detail"]
            == InvalidPasswordError(
                function_name=CRUD_user.update_password.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_update_user_me_email_exists(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)

        data = {"email": user.email}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-email-pre-confirmation",
            headers=normal_user_token_headers,
            json=data,
        )
        assert r.status_code == 409
        assert (
            r.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=User.__tablename__,
                filter={"email": user.email},
                function_name=CRUD_user.check_exists_raise.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_update_user_me_username_exists(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)

        data = {"username": user.username}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/update-me-username-pre-confirmation",
            headers=normal_user_token_headers,
            json=data,
        )
        assert r.status_code == 409
        assert (
            r.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=User.__tablename__,
                filter={"username": user.username},
                function_name=CRUD_user.check_exists_raise.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_update_password_me_same_password_error(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        data = {
            "current_password": settings.FIRST_SUPERUSER_PASSWORD,
            "new_password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/me/password",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 400
        updated_user = r.json()
        assert (
            updated_user["detail"]
            == NewPasswordIsSameError(
                function_name=CRUD_user.update_password.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_register_user(
        self,
        client: AsyncClient,
        db: Session,
        user_cache_register_user: UserCache,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}
        r_pre_confirm = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
            json=data,
        )
        details_pre_confirm = r_pre_confirm.json()["message"]
        assert r_pre_confirm.status_code == 200
        assert (
            details_pre_confirm
            == get_user_register_confirmation_sent_msg(username, email).message
        )

        user_pre_confirmed_db = CRUD_user.get(db=db, filter={"email": email})
        assert user_pre_confirmed_db.email == email
        assert user_pre_confirmed_db.username == username
        assert user_pre_confirmed_db.isActive is False
        assert verify_password(password, user_pre_confirmed_db.hashedPassword)

        user_register_token = await user_cache_register_user.create_user_cache_instance(
            user=user_pre_confirmed_db,
            expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
        )
        data_confirm = {"access_token": user_register_token}
        r_confirm = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup",
            json=data_confirm,
        )
        assert r_confirm.status_code == 200
        details_confirm = r_confirm.json()["message"]
        assert (
            details_confirm
            == get_user_successfully_registered_msg(username, email).message
        )
        user_after_confirmed_db = CRUD_user.get(db=db, filter={"email": email})
        db.refresh(user_after_confirmed_db)
        assert user_after_confirmed_db.isActive

    @pytest.mark.anyio
    async def test_register_user_email_already_exists_error(
        self, client: AsyncClient
    ) -> None:
        password = random_lower_string()
        username = random_lower_string()
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": password,
            "username": username,
        }
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
            json=data,
        )
        assert r.status_code == 409
        assert (
            r.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=User.__tablename__,
                filter={"email": data["email"]},
                function_name=CRUD_user.check_exists_raise.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_register_user_username_already_exists_error(
        self, client: AsyncClient
    ) -> None:
        email = random_email()
        password = random_lower_string()
        data = {
            "email": email,
            "password": password,
            "username": settings.FIRST_SUPERUSER_USERNAME,
        }
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
            json=data,
        )
        assert r.status_code == 409
        assert (
            r.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=User.__tablename__,
                filter={"username": data["username"]},
                function_name=CRUD_user.check_exists_raise.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_register_wrong_token(
        self,
        client: AsyncClient,
        db: Session,
        user_cache_register_user: UserCache,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}
        r_pre_confirm = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
            json=data,
        )
        details_pre_confirm = r_pre_confirm.json()["message"]
        assert r_pre_confirm.status_code == 200
        assert (
            details_pre_confirm
            == get_user_register_confirmation_sent_msg(username, email).message
        )

        user_pre_confirmed_db = CRUD_user.get(db=db, filter={"email": email})
        assert user_pre_confirmed_db.email == email
        assert user_pre_confirmed_db.username == username
        assert user_pre_confirmed_db.isActive is False
        assert verify_password(password, user_pre_confirmed_db.hashedPassword)

        user_register_token = await user_cache_register_user.create_user_cache_instance(
            user=user_pre_confirmed_db,
            expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
        )

        wrong_token = user_register_token + "wrong"
        data_confirm = {"access_token": wrong_token}
        r_confirm = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup",
            json=data_confirm,
        )
        details_confirm = r_confirm.json()["detail"]
        assert r_confirm.status_code == 401
        assert (
            details_confirm
            == InvalidTokenError(
                token=wrong_token,
                function_name=user_cache_register_user.verify_token.__name__,
                class_name=user_cache_register_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_update_user(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        updated_username = random_lower_string()

        data = {"username": updated_username}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{user.userId}",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 200
        updated_user = r.json()

        assert updated_user["username"] == updated_username

        user_db = CRUD_user.get(db=db, filter={"email": email})
        db.refresh(user_db)
        assert user_db
        assert user_db.username == updated_username

    @pytest.mark.anyio
    async def test_update_user_not_exists(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        data = {"username": "Updated_username"}
        not_found_user_id = uuid.uuid4()
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{not_found_user_id}",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 404
        assert (
            r.json()["detail"]
            == DbObjectDoesNotExistError(
                model_table_name=User.__tablename__,
                filter={"userId": not_found_user_id},
                function_name=CRUD_user.update.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_update_user_email_exists(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)

        email2 = random_email()
        password2 = random_lower_string()
        username2 = random_lower_string()
        user_in2 = UserCreate(email=email2, password=password2, username=username2)
        user2 = CRUD_user.create(db=db, user_create=user_in2)

        data = {"email": user2.email}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{user.userId}",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 409
        assert (
            r.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=User.__tablename__,
                filter=data,
                function_name=CRUD_user.check_exists_raise.__name__,
                class_name=CRUD_user.__class__.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_delete_user_me(self, client: AsyncClient, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        user_id = user.userId

        login_data = {
            "email": email,
            "password": password,
            "username": username,
        }
        r = await client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        a_token = tokens["access_token"]
        headers = {"Authorization": f"Bearer {a_token}"}

        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/me",
            headers=headers,
        )
        assert r.status_code == 200
        deleted_user = r.json()
        assert (
            deleted_user["message"]
            == get_delete_return_msg(User.__tablename__, {"userId": user_id}).message
        )

        result = await client.get(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=headers,
        )
        details = result.json()["detail"]
        assert result.status_code == 404
        assert (
            details
            == DbObjectDoesNotExistError(
                model_table_name=User.__tablename__,
                filter={"userId": user_id},
                function_name=get_current_user.__name__,
            ).detail
        )
        user_db = CRUD_user.get(db=db, filter={"userId": user_id})
        assert user_db is None

    @pytest.mark.anyio
    async def test_delete_user_me_as_superuser(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/me",
            headers=superuser_token_headers,
        )
        assert r.status_code == 403
        response = r.json()
        current_user_email = settings.FIRST_SUPERUSER_USERNAME
        assert (
            response["detail"]
            == SuperUserNotAllowedToDeleteSelfError(
                username_or_email=current_user_email,
                function_name=delete_user_me.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_delete_user_me_not_active(
        self,
        client: AsyncClient,
        db: Session,
        normal_user_token_headers: dict[str, str],
        superuser_token_headers: dict[str, str],
    ) -> None:
        normal_user = await self._get_current_normal_user(
            client, normal_user_token_headers, db
        )
        update_is_active_data = {"isActive": False}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{normal_user.userId}",
            headers=superuser_token_headers,
            json=update_is_active_data,
        )

        assert r.status_code == 200
        updated_user = r.json()
        assert updated_user["isActive"] is False

        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/me",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 403
        response = r.json()

        assert (
            response["detail"]
            == UserIsNotActiveError(
                username_or_email=normal_user.username,
                function_name=get_current_user.__name__,
            ).detail
        )
        # revert to the old active status to keep consistency in test
        update_is_active_data = {"isActive": True}
        r = await client.patch(
            f"{settings.API_V1_STR}/{user_prefix}/{normal_user.userId}",
            headers=superuser_token_headers,
            json=update_is_active_data,
        )
        assert r.status_code == 200
        updated_user = r.json()
        assert updated_user["isActive"]

    @pytest.mark.anyio
    async def test_delete_user_super_user(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in)
        user_id = user.userId
        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=superuser_token_headers,
        )
        assert r.status_code == 200
        deleted_user = r.json()
        assert (
            deleted_user["message"]
            == get_delete_return_msg(User.__tablename__, {"userId": user_id}).message
        )
        result = CRUD_user.get(db=db, filter={"userId": user_id})
        assert result is None

    @pytest.mark.anyio
    async def test_delete_user_not_found(
        self, client: AsyncClient, superuser_token_headers: dict[str, str]
    ) -> None:
        not_found_user_id = uuid.uuid4()
        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/{not_found_user_id}",
            headers=superuser_token_headers,
        )
        assert r.status_code == 404
        assert (
            r.json()["detail"]
            == DbObjectDoesNotExistError(
                model_table_name=User.__tablename__,
                filter={"userId": not_found_user_id},
                function_name=delete_user.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_delete_user_current_super_user_error(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        super_user = CRUD_user.get(db=db, filter={"email": settings.FIRST_SUPERUSER})
        assert super_user
        user_id = super_user.userId

        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/{user_id}",
            headers=superuser_token_headers,
        )
        assert r.status_code == 403
        assert (
            r.json()["detail"]
            == SuperUserNotAllowedToDeleteSelfError(
                username_or_email=super_user.username,
                function_name=delete_user.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_delete_user_without_privileges(
        self,
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
        db: Session,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(
            email=email, password=password, username=username, isActive=True
        )
        user = CRUD_user.create(db=db, user_create=user_in)

        r = await client.delete(
            f"{settings.API_V1_STR}/{user_prefix}/{user.userId}",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 403
        current_user_username = settings.TEST_USER_USERNAME
        assert (
            r.json()["detail"]
            == UserWithNotEnoughPrivilegesError(
                username_or_email=current_user_username,
                function_name=get_current_active_superuser.__name__,
            ).detail
        )

    @pytest.mark.anyio
    async def test_token_expired_user(
        self,
        client: AsyncClient,
        db: Session,
        get_cache: Redis,
        user_cache_register_user: UserCache,
        user_cache_session: UserCache,
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        data = {"email": email, "password": password, "username": username}
        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
            json=data,
        )
        assert r.status_code == 200
        detail = r.json()["message"]
        assert (
            detail == get_user_register_confirmation_sent_msg(username, email).message
        )
        assert (
            detail == get_user_register_confirmation_sent_msg(username, email).message
        )

        user_db = CRUD_user.get(db=db, filter={"email": email})

        token = await user_cache_register_user.create_user_cache_instance(
            user=user_db,
            expire_seconds=settings.EMAIL_RESET_TOKEN_EXPIRE_SECONDS,
        )

        r = await client.post(
            f"{settings.API_V1_STR}/{user_prefix}/signup",
            json={"access_token": token},
        )

        assert r.status_code == 200

        user_db = CRUD_user.get(db=db, filter={"email": email})
        assert user_db
        assert user_db.email == email
        assert user_db.username == username
        assert verify_password(password, user_db.hashedPassword)

        # Test login with expired token
        await get_cache.flushall()
        with (
            patch("app.core.config.settings.ACCESS_SESSION_EXPIRE_SECONDS", 1),
        ):
            login_data = {
                "email": email,
                "password": password,
                "username": username,
            }
            r = await client.post(
                f"{settings.API_V1_STR}/login/access-token", data=login_data
            )
            token = r.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            time.sleep(1.1)  # Wait for token to expire
            r_get_user_me_ok = await client.get(
                f"{settings.API_V1_STR}/{user_prefix}/me",
                headers=headers,
            )
            invalid_token_error = InvalidTokenError(
                token=token,
                function_name=user_cache_session.verify_token.__name__,
                class_name=user_cache_session.__class__.__name__,
            )
            assert r_get_user_me_ok.status_code == invalid_token_error.status_code
            assert r_get_user_me_ok.json()["detail"] == invalid_token_error.detail


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestUserRateLimitAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_pre_register_user_rate_limit(
        self,
        client: AsyncClient,
        ip_rate_limiter,  # noqa: ARG001 # Do not remove, used to enable ip rate limiter
    ) -> None:
        """
        Perform rate limit test for pre register user endpoint.
        """

        # Create API function to test
        def post_plot_query_from_api_normal_user(
            register_data: dict[str, str],
        ) -> Awaitable[Response]:
            return client.post(
                f"{settings.API_V1_STR}/{user_prefix}/signup-send-confirmation",
                json=register_data,
            )

        # Get rate limit per time interval from register_user_send_confirmation API function
        rate_limits_per_interval_format = (
            get_function_decorator_rate_limit_per_time_interval(
                register_user_send_confirmation
            )
        )

        # Create object generator function to generate new users for each rate limit test
        def create_register_user_object() -> dict[str, str]:
            email = random_email()
            password = random_lower_string()
            username = random_lower_string()
            return {
                "email": email,
                "password": password,
                "username": username,
            }

        await self.perform_time_interval_requests_with_api_function(
            api_function=post_plot_query_from_api_normal_user,
            all_rate_limits_per_interval=rate_limits_per_interval_format,
            create_object_dict_func=create_register_user_object,
        )
