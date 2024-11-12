import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.schemas import UserCreate, UserUpdate
from app.core.security import verify_password
from app.crud import CRUD_user as crud
from app.tests.test_simulating_env.base_test import BaseTest
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestUserCRUD(BaseTest):
    def test_create_user(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(email=email, password=password, username=username)
        user = crud.create(db=db, user_create=user_in)
        assert user.email == email
        assert hasattr(user, "hashedPassword")

    def test_authenticate_user(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(email=email, password=password, username=username)
        user = crud.create(db=db, user_create=user_in)
        authenticated_user = crud.authenticate(
            db=db, email_or_username=email, password=password
        )
        assert authenticated_user
        assert user.email == authenticated_user.email

    def test_not_authenticate_user(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        user = crud.authenticate(db=db, email_or_username=email, password=password)
        assert user is None

    def test_check_if_user_is_active(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(email=email, password=password, username=username)
        user = crud.create(db=db, user_create=user_in)
        assert user.isActive

    def test_check_if_user_is_inactive(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(
            email=email, password=password, username=username, isActive=False
        )
        user = crud.create(db=db, user_create=user_in)
        assert user.isActive is False

    def test_check_if_user_is_superuser(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = crud.create(db=db, user_create=user_in)
        assert user.isSuperuser

    def test_check_if_user_is_superuser_normal_user(self, db: Session) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(email=email, password=password, username=username)
        user = crud.create(db=db, user_create=user_in)
        assert user.isSuperuser is False

    def test_get_user(self, db: Session) -> None:
        password = random_lower_string()
        email = random_email()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = crud.create(db=db, user_create=user_in)
        user_2 = crud.get(db=db, filter={"userId": user.userId})
        assert user_2
        assert user.email == user_2.email
        self._test_object(user_2, user)

    def test_update_user(self, db: Session) -> None:
        password = random_lower_string()
        email = random_email()
        username = random_lower_string(small_string=True)
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = crud.create(db=db, user_create=user_in)
        new_password = random_lower_string()
        user_in_update = UserUpdate(password=new_password, isSuperuser=True)
        assert user.email == email
        crud.update(db=db, user_id=user.userId, user_in=user_in_update)
        user_2 = crud.get(db=db, filter={"userId": user.userId})
        assert user_2
        assert user.email == user_2.email
        assert verify_password(new_password, user_2.hashedPassword)
