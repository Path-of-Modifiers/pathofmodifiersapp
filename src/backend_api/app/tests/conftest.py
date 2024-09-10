from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.cache.cache import cache
from app.core.config import settings
from app.main import app
from app.tests.setup_test_database import override_get_db, test_db_engine
from app.tests.utils.cache_utils import clear_pom_cache
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


@pytest.fixture(scope="module")
def get_cache() -> Generator[Redis, None, None]:
    yield cache


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(
        app  # For the warning DeprecationWarning: The 'app' ..., check https://github.com/tiangolo/fastapi/discussions/6211.
    ) as c:
        yield c


@pytest.fixture(scope="module")
def clear_db() -> Generator:
    # Remove any data from database (even data not created by this session)
    clear_all_tables()
    yield


@pytest.fixture(scope="module")
def clear_cache() -> Generator:
    clear_pom_cache()
    yield


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client,
        email=settings.TEST_USER_EMAIL,
        username=settings.TEST_USER_USERNAME,
        db=db,
    )
