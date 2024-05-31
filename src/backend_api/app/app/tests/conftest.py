from typing import Generator
from fastapi.testclient import TestClient
import pytest
from requests.auth import HTTPBasicAuth

from sqlalchemy.orm import Session

from app.main import app
from app.tests.test_database import override_get_db, test_db_engine
from app.tests.utils.database_utils import (
    clear_all_tables,
    mock_src_database_for_test_db,
)
from app.core.models.database import Base
from app.api.deps import get_db
from app.tests.utils.utils import get_super_authentication


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    mock_src_database_for_test_db()
    with Session(test_db_engine) as session:
        yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def superuser_headers() -> HTTPBasicAuth:
    return get_super_authentication()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def clear_db() -> Generator:
    yield
    # Remove any data from database (even data not created by this session)
    clear_all_tables()
