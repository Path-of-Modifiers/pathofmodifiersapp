import asyncio
import logging
from collections.abc import AsyncGenerator, Generator
from contextlib import ExitStack
from logging import Logger

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from redis.asyncio import Redis
from slowapi import Limiter
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import Session

from app.api.deps import get_async_db, get_db
from app.core.cache.cache import cache
from app.core.cache.user_cache import UserCache, UserCacheTokenType
from app.core.config import settings
from app.core.models.init_db import init_db
from app.core.rate_limit.rate_limiters import limiter_ip, limiter_user
from app.main import app as actual_app
from app.tests.test_simulating_env.setup_test_database import (
    ASYNC_TEST_DATABASE_URL,
    TEST_DATABASE_URL,
)
from app.tests.utils.database_utils import (
    clear_all_tables,
    mock_src_database_for_test_db,
)
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, None, None]:
    with ExitStack():
        yield actual_app


@pytest.fixture(scope="session")
def engine() -> Generator[AsyncEngine, None, None]:
    test_db_engine = create_engine(TEST_DATABASE_URL)
    mock_src_database_for_test_db(test_db_engine)
    yield test_db_engine


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None, None]:
    engine = create_async_engine(ASYNC_TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def setup_db(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def db(setup_db: Session) -> Generator[Session, None, None]:
    yield setup_db


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_async_db(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def async_db(
    setup_async_db: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    yield setup_async_db


@pytest_asyncio.fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app=app) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver-asyncio") as c:
        yield c


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_override(
    app: FastAPI, engine: Engine, async_engine: AsyncEngine
) -> None:
    def override_get_db():
        with Session(engine) as db:
            init_db(db)
            yield db

    async def override_get_async_db():
        async with AsyncSession(async_engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = override_get_async_db


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


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def get_cache() -> AsyncGenerator[Redis, None]:
    yield cache
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


@pytest.fixture
def clear_db(engine: Engine) -> Generator:
    # Remove any data from database (even data not created by this session)
    clear_all_tables(engine)
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
    engine: Engine,
) -> list[dict[str, str]]:
    """Used to perform multiple requests with different users in parallel"""
    number_of_headers = 2  # Currently only works with a few since there's a bug in caching upon multiple requests
    headers = []
    for i in range(number_of_headers):
        with Session(engine, expire_on_commit=False, autocommit=False) as db:
            header = await authentication_token_from_email(
                async_client=async_client,
                email=str(i) + settings.TEST_USER_EMAIL,
                username=str(i) + settings.TEST_USER_USERNAME,
                db=db,
            )
            headers.append(header)
    return headers


@pytest.fixture(scope="session")
def event_loop(request):  # noqa: ARG001
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_logger() -> Generator[Logger, None, None]:
    yield logging.getLogger(__name__)
