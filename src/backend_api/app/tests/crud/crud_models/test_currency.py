from collections.abc import Callable, Generator

import pytest
from sqlalchemy.orm import Session

import app.tests.crud.crud_test_base as test_crud
from app.core.models.database import engine
from app.crud import CRUD_currency
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.currency import generate_random_currency


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return False


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], dict]:
    return generate_random_currency


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_currency


class TestCurrencyCRUD(test_crud.TestCRUD):
    pass
