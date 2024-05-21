from typing import Generator
import pytest

from sqlalchemy.orm import Session

from app.tests.mock_database import mock_src_database_for_test_db, test_db_engine

@pytest.fixture(scope="session")
def db() -> Generator:
    mock_src_database_for_test_db()
    with Session(test_db_engine) as session:
        yield session
    session.rollback()
    session.close()
