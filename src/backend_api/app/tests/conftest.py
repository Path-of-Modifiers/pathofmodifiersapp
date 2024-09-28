import asyncio
import logging
from collections.abc import AsyncGenerator, Generator
from logging import Logger

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from redis.asyncio import Redis
from slowapi import Limiter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.deps import get_async_db, get_db
from app.core.cache.cache import cache
from app.core.cache.user_cache import UserCache, UserCacheTokenType
from app.core.config import settings
from app.limiter import limiter_ip, limiter_user
from app.main import app
from app.tests.setup_test_database import (
    override_get_async_db,
    override_get_db,
    test_async_db_engine,
    test_db_engine,
)
from app.tests.utils.database_utils import (
    clear_all_tables,
    mock_src_database_for_test_db,
)
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    mock_src_database_for_test_db()
    with Session(test_db_engine) as session:
        yield session
        session.rollback()
        session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(test_async_db_engine) as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = override_get_async_db
    with TestClient(
        app  # For the warning DeprecationWarning: The 'app' ..., check https://github.com/tiangolo/fastapi/discussions/6211.
    ) as c:
        yield c


@pytest.fixture
def user_rate_limiter() -> Generator[Limiter, None, None]:
    """
    Fixture that enables user rate limiter for tests.
    Only need to be set as test function param
    """
    limiter_user.enabled = True
    yield limiter_user
    limiter_user.enabled = False


@pytest.fixture
def ip_rate_limiter() -> Generator[Limiter, None, None]:
    """
    Fixture that enables ip rate limiter for tests.
    Only need to be set as test function param
    """
    limiter_ip.enabled = True
    yield limiter_ip
    limiter_ip.enabled = False


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(app=app, base_url="http://testserver-asyncio") as c:
        yield c


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def get_cache() -> AsyncGenerator[Redis, None]:
    yield cache
    await cache.flushall()
    await cache.aclose()


@pytest_asyncio.fixture
async def user_cache_password_reset() -> AsyncGenerator[UserCache, None]:
    async with UserCache(
        UserCacheTokenType.PASSWORD_RESET
    ) as user_cache_password_reset:
        yield user_cache_password_reset


@pytest_asyncio.fixture
async def user_cache_register_user() -> AsyncGenerator[UserCache, None]:
    async with UserCache(UserCacheTokenType.REGISTER_USER) as user_cache_register_user:
        yield user_cache_register_user


@pytest_asyncio.fixture
async def user_cache_session() -> AsyncGenerator[UserCache, None]:
    async with UserCache(UserCacheTokenType.ACCESS_SESSION) as user_cache_session:
        yield user_cache_session


@pytest_asyncio.fixture
async def user_cache_update_me() -> AsyncGenerator[UserCache, None]:
    async with UserCache(UserCacheTokenType.UPDATE_ME) as user_cache_update_me:
        yield user_cache_update_me


@pytest.fixture(scope="module")
def clear_db() -> Generator:
    # Remove any data from database (even data not created by this session)
    clear_all_tables()
    yield


@pytest_asyncio.fixture
async def clear_cache(get_cache: Redis) -> AsyncGenerator:
    # Remove any data from cache
    await get_cache.flushall()
    await get_cache.aclose()
    yield


@pytest_asyncio.fixture
async def superuser_token_headers(
    async_client: AsyncClient,
) -> dict[str, str]:
    return await get_superuser_token_headers(async_client)


@pytest_asyncio.fixture
async def normal_user_token_headers(
    async_client: AsyncClient, db: Session
) -> dict[str, str]:
    return await authentication_token_from_email(
        async_client=async_client,
        email=settings.TEST_USER_EMAIL,
        username=settings.TEST_USER_USERNAME,
        db=db,
    )


@pytest_asyncio.fixture
async def multiple_async_normal_user_token_headers(
    async_client: AsyncClient,
) -> list[dict[str, str]]:
    """Used to perform multiple requests with different users in parallel"""
    number_of_headers = 1  # Currently only works with a few since there's a bug in caching upon multiple requests
    headers = []
    for i in range(number_of_headers):
        with Session(test_db_engine, expire_on_commit=False, autocommit=False) as db:
            try:
                header = await authentication_token_from_email(
                    async_client=async_client,
                    email=str(i) + settings.TEST_USER_EMAIL,
                    username=str(i) + settings.TEST_USER_USERNAME,
                    db=db,
                )
            finally:
                db.close()
            headers.append(header)
    return headers


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_logger() -> Generator[Logger, None, None]:
    yield logging.getLogger(__name__)
