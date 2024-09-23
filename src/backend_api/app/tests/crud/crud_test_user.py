from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import UserCreate, UserUpdate
from app.core.security import verify_password
from app.crud import CRUD_user as crud
from app.tests.base_test import BaseTest
from app.tests.utils.utils import random_email, random_lower_string


# @pytest.mark.usefixtures("clear_db", autouse=True)
class TestUserCRUD(BaseTest):
    async def test_create_user(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = await crud.create(db, user_create=user_in)
        assert user.email == email
        assert hasattr(user, "hashedPassword")

    async def test_authenticate_user(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = await crud.create(db, user_create=user_in)
        authenticated_user = await crud.authenticate(
            db, email_or_username=email, password=password
        )
        assert authenticated_user
        assert user.email == authenticated_user.email

    async def test_not_authenticate_user(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        user = await crud.authenticate(db, email_or_username=email, password=password)
        assert user is None

    async def test_check_if_user_is_active(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = await crud.create(db, user_create=user_in)
        assert user.isActive

    async def test_check_if_user_is_inactive(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(
            email=email, password=password, username=username, isActive=False
        )
        user = await crud.create(db, user_create=user_in)
        assert user.isActive is False

    async def test_check_if_user_is_superuser(self, db: AsyncSession) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = await crud.create(db, user_create=user_in)
        assert user.isSuperuser

    async def test_check_if_user_is_superuser_normal_user(
        self, db: AsyncSession
    ) -> None:
        email = random_email()
        password = random_lower_string()
        username = random_lower_string()
        user_in = UserCreate(email=email, password=password, username=username)
        user = await crud.create(db=db, user_create=user_in)
        assert user.isSuperuser is False

    async def test_get_user(self, db: AsyncSession) -> None:
        password = random_lower_string()
        email = random_email()
        username = random_lower_string()
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = await crud.create(db, user_create=user_in)
        user_2 = await crud.get(db, filter={"userId": user.userId})
        assert user_2
        assert user.email == user_2.email
        assert jsonable_encoder(user) == jsonable_encoder(user_2)

    async def test_update_user(self, db: AsyncSession) -> None:
        password = random_lower_string()
        email = random_email()
        username = random_lower_string()
        user_in = UserCreate(
            email=email, password=password, username=username, isSuperuser=True
        )
        user = await crud.create(db, user_create=user_in)
        new_password = random_lower_string()
        user_in_update = UserUpdate(password=new_password, isSuperuser=True)
        assert user.email == email
        await crud.update(db, user_id=user.userId, user_in=user_in_update)
        user_2 = await crud.get(db, filter={"userId": user.userId})
        assert user_2
        assert user.email == user_2.email
        assert verify_password(new_password, user_2.hashedPassword)
