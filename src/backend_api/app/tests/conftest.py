from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from asyncpg import Connection
from httpx import AsyncClient
from redis.asyncio import Redis
from slowapi import Limiter
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.core.cache.cache import cache
from app.core.cache.user_cache import UserCache, UserCacheTokenType
from app.core.config import settings
from app.core.models.database import Base
from app.limiter import limiter_ip, limiter_user
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

TEST_DATABASE_URL: str | None = str(settings.TEST_DATABASE_URI)

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set")


def run_migrations(connection: Connection):
    config = Config("app/alembic.ini")
    config.set_main_option("script_location", "app/alembic")
    config.set_main_option("sqlalchemy.url", str(settings.TEST_DATABASE_URI))
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):  # noqa: ARG001
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": Base.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(
        str(settings.TEST_DATABASE_URI), pool_size=300, max_overflow=0
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
def async_session_maker(engine):
    AsyncSessionLocal = async_sessionmaker(
        autocommit=False, bind=engine, expire_on_commit=False
    )

    return AsyncSessionLocal


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture()
async def setup_database(engine):
    # Run alembic migrations on test DB
    async with engine.begin() as connection:
        await connection.run_sync(run_migrations)

    yield

    # Teardown
    await engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db(async_session_maker, setup_database):  # noqa: ARG001
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def get_db_session_override():
        yield db

    app.dependency_overrides[get_db] = get_db_session_override
    async with AsyncClient(app=app, base_url="http://testserver-asyncio") as c:
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


@pytest.fixture
def anyio_backend():
    return "asyncio"


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


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


# @pytest_asyncio.fixture
# async def clear_db() -> AsyncGenerator:
# """Fixture to clear the test database before running tests."""
# Remove any data from the database (even data not created by this session)
# await clear_all_tables()
# yield


@pytest_asyncio.fixture
async def clear_cache(get_cache: Redis) -> AsyncGenerator:
    # Remove any data from cache
    await get_cache.flushall()
    await get_cache.aclose()
    yield


@pytest_asyncio.fixture
async def superuser_token_headers(
    client: AsyncClient,
) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture
async def normal_user_token_headers(
    client: AsyncClient, db: AsyncSession
) -> dict[str, str]:
    return await authentication_token_from_email(
        client=client,
        email=settings.TEST_USER_EMAIL,
        username=settings.TEST_USER_USERNAME,
        db=db,
    )
