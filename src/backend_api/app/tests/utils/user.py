from httpx import AsyncClient
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.schemas import User, UserCreate, UserUpdate
from app.crud import CRUD_user
from app.tests.utils.utils import random_email, random_lower_string


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreate(email=email, password=password, username=username)
    async with db.begin():
        user = await CRUD_user.create(db, user_create=user_in)
    return user


async def authentication_token_from_email(
    *,
    client: AsyncClient,
    email: EmailStr,
    username: str,
    db: AsyncSession,
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    async with db.begin():
        user = await CRUD_user.get(db, filter={"email": email})
        if not user:
            user_in_create = UserCreate(
                email=email, password=password, username=username
            )
            user = await CRUD_user.create(db, user_create=user_in_create)
        else:
            user_in_update = UserUpdate(password=password)
            if not user.userId:
                raise Exception("User id not set")
            user = await CRUD_user.update(
                db, user_id=user.userId, user_in=user_in_update
            )

    return await user_authentication_headers(
        client=client, email=email, password=password
    )
