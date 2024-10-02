from pydantic import PostgresDsn

from app.core.config import settings

TEST_DATABASE_URL: PostgresDsn | None = str(settings.TEST_DATABASE_URI)
ASYNC_TEST_DATABASE_URL: PostgresDsn | None = str(settings.ASYNC_TEST_DATABASE_URI)

if not TEST_DATABASE_URL or not ASYNC_TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set")
