from collections.abc import Callable, Generator

import pytest
from sqlalchemy.orm import Session

import app.tests.test_simulating_env.crud.crud_test_base as test_crud
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
def is_hypertable() -> bool:
    return False


@pytest.fixture(scope="module")
def on_duplicate_params() -> tuple[bool, str | None]:
    """
    In tuple:
        First item: `on_duplicate_do_nothing`.
        Second item: `on_duplicate_constraint` (unique constraint to check the duplicate on)
    """
    return (False, None)


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
