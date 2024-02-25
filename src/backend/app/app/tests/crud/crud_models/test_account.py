from sqlalchemy.orm import Session
from typing import Dict, Generator, Callable
import pytest

from app.crud import CRUD_account
from app.core.models.database import engine
from app.crud.base import CRUDBase
import app.tests.crud.test_crud as test_crud
from app.tests.utils.model_utils.account import generate_random_account


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_account


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_account


class TestAccountCRUD(test_crud.TestCRUD):
    pass
