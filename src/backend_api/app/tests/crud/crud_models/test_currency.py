from collections.abc import Callable

import pytest

import app.tests.crud.crud_test_base as test_crud
from app.crud import CRUD_currency
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.currency import generate_random_currency


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
