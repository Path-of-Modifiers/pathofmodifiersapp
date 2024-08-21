import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.api.api_message_util import (
    get_db_obj_already_exists_msg,
    get_delete_return_msg,
    get_incorrect_psw_msg,
    get_new_psw_not_same_msg,
    get_no_obj_matching_query_msg,
    get_superuser_not_allowed_delete_self_msg,
    get_user_psw_change_msg,
)
from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import UserCreate
from app.core.security import verify_password
from app.crud import CRUD_user as crud
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    with (
        patch("app.utils.send_email", return_value=None),
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        email = random_email()
        password = random_lower_string()
        data = {"email": email, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.get(session=db, filter={"email": email})
        assert user
        assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)
    user_id = user.userId
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get(session=db, filter={"email": email})
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)
    user_id = user.userId

    login_data = {
        "email": email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get(session=db, filter=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_permissions_error(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The user doesn't have enough privileges"}


def test_create_user_existing_email(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    # email = email
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.create(session=db, user_create=user_in)
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.create(session=db, user_create=user_in)

    email2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=email2, password=password2)
    crud.create(session=db, user_create=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users["data"]) > 1
    assert "count" in all_users
    for item in all_users["data"]:
        assert "email" in item


def test_update_user_me(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    username = "Updated Name"
    email = random_email()
    data = {"username": username, "email": email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["email"] == email
    assert updated_user["username"] == username

    user_db = crud.get(session=db, filter={"email": email})
    assert user_db
    assert user_db.email == email
    assert user_db.username == username


def test_update_password_me(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": new_password,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert (
        updated_user["message"]
        == get_user_psw_change_msg(settings.FIRST_SUPERUSER).message
    )

    email_map = {"email": settings.FIRST_SUPERUSER}
    user_db = crud.get(session=db, filter=email_map)
    assert user_db
    assert user_db.email == settings.FIRST_SUPERUSER
    assert verify_password(new_password, user_db.hashedPassword)

    # Revert to the old password to keep consistency in test
    old_data = {
        "current_password": new_password,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=old_data,
    )
    db.refresh(user_db)

    assert r.status_code == 200
    assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user_db.hashedPassword)


def test_update_password_me_incorrect_password(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert updated_user["detail"] == get_incorrect_psw_msg().message


def test_update_user_me_email_exists(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)

    data = {"email": user.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert (
        r.json()["detail"]
        == get_db_obj_already_exists_msg(
            User.__tablename__, {"email", user_in.email}
        ).message
    )


def test_update_password_me_same_password_error(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert updated_user["detail"] == get_new_psw_not_same_msg().message


def test_register_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    data = {"email": email, "password": password, "username": username}
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == email
    assert created_user["username"] == username

    user_db = crud.get(session=db, filter={"email": email})
    assert user_db
    assert user_db.email == email
    assert user_db.username == username
    assert verify_password(password, user_db.hashedPassword)


def test_register_user_already_exists_error(client: TestClient) -> None:
    password = random_lower_string()
    username = random_lower_string()
    data = {
        "email": settings.FIRST_SUPERUSER,
        "password": password,
        "username": username,
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 400
    assert (
        r.json()["detail"]
        == get_db_obj_already_exists_msg(
            User.__tablename__, {"email": data["email"]}
        ).message
    )


def test_update_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)

    data = {"username": "Updated_username"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.userId}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()

    assert updated_user["username"] == "Updated_username"

    user_db = crud.get(db=db, filter={"email": email})
    db.refresh(user_db)
    assert user_db
    assert user_db.username == "Updated_username"


def test_update_user_not_exists(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"username": "Updated_username"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert (
        r.json()["detail"]
        == get_no_obj_matching_query_msg(
            filter={"username": data["username"]}, model_table_name=User.__tablename__
        ).message
    )


def test_update_user_email_exists(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)

    email2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=email2, password=password2)
    user2 = crud.create(session=db, user_create=user_in2)

    data = {"email": user2.email}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.userId}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert (
        r.json()["detail"]
        == get_db_obj_already_exists_msg(
            User.__tablename__, mapping={"email": user2.email}
        ).message
    )


def test_delete_user_me(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)
    user_id = user.userId

    login_data = {
        "email": email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert (
        deleted_user["message"]
        == get_delete_return_msg(User.__tablename__, {"userId": user_id}).message
    )
    result = crud.get(db=db, filter={"userId": user_id})
    assert result is None

    user_query = select(User).where(user.userId == user_id)
    user_db = db.execute(user_query).first()
    assert user_db is None


def test_delete_user_me_as_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    response = r.json()
    current_user_email = settings.FIRST_SUPERUSER_USERNAME
    assert (
        response["detail"]
        == get_superuser_not_allowed_delete_self_msg(
            username=current_user_email
        ).message
    )


def test_delete_user_super_user(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)
    user_id = user.userId
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert (
        deleted_user["message"]
        == get_delete_return_msg(User.__tablename__, {"userId": user_id}).message
    )
    result = db.exec(select(User).where(user.userId == user_id)).first()
    assert result is None


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    not_found_user_id = uuid.uuid4()
    r = client.delete(
        f"{settings.API_V1_STR}/users/{not_found_user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == get_no_obj_matching_query_msg(
        {"user:": not_found_user_id}, User.__tablename__
    )


def test_delete_user_current_super_user_error(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    super_user = crud.get(session=db, filter={"email": settings.FIRST_SUPERUSER})
    assert super_user
    user_id = super_user.userId

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert (
        r.json()["detail"]
        == get_superuser_not_allowed_delete_self_msg(super_user.email).message
    )


def test_delete_user_without_privileges(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create(session=db, user_create=user_in)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.userId}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"
