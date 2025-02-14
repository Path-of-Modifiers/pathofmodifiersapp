from httpx import AsyncClient
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.schemas import User, UserCreate, UserUpdate
from app.crud import CRUD_user
from app.tests.utils.utils import random_email, random_lower_string


async def user_authentication_headers(
    *, async_client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = await async_client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string(small_string=True)
    user_in = UserCreate(email=email, password=password, username=username)
    user = CRUD_user.create(db=db, user_create=user_in)
    return user


async def authentication_token_from_email(
    *, async_client: AsyncClient, email: EmailStr, username: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = CRUD_user.get(db=db, filter={"email": email})
    if not user:
        user_in_create = UserCreate(email=email, password=password, username=username)
        user = CRUD_user.create(db=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        if not user.userId:
            raise Exception("User id not set")
        user = CRUD_user.update(db=db, user_id=user.userId, user_in=user_in_update)

    return await user_authentication_headers(
        async_client=async_client, email=email, password=password
    )
