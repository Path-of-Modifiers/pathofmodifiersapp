from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.models.database import Base
from app.core.models.init_db import init_db

TEST_DATABASE_URL: PostgresDsn | None = str(settings.TEST_DATABASE_URI)
ASYNC_TEST_DATABASE_URL: PostgresDsn | None = str(settings.ASYNC_TEST_DATABASE_URI)

if not TEST_DATABASE_URL or not ASYNC_TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set")

test_db_engine = create_engine(TEST_DATABASE_URL)
test_async_db_engine = create_async_engine(ASYNC_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_db_engine
)
AsyncTestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_async_db_engine
)

Base.metadata.create_all(bind=test_db_engine)


# This is a fixture that overrides the get_db dependency of the FastAPI app.
def override_get_db():
    try:
        db = TestingSessionLocal()
        init_db(db)
        yield db
    finally:
        db.close()


async def override_get_async_db():
    try:
        async_db = AsyncTestingSessionLocal()
        yield async_db
    finally:
        await async_db.close()
