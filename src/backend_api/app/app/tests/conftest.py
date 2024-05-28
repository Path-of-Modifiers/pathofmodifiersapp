from typing import Generator
from fastapi.testclient import TestClient
import pytest

from sqlalchemy.orm import Session

from app.main import app
from app.tests.mock_database import mock_src_database_for_test_db, test_db_engine



@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    mock_src_database_for_test_db()
    with Session(test_db_engine) as session:
        yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
        