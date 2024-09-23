from collections.abc import Callable

import pytest
import pytest_asyncio

import app.tests.crud.crud_test_base as test_crud
from app.crud import CRUD_account
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.account import generate_random_account


@pytest_asyncio.fixture
async def object_generator_func() -> Callable[[], dict]:
    return generate_random_account


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return True


@pytest_asyncio.fixture
async def crud_instance() -> CRUDBase:
    return CRUD_account


class TestAccountCRUD(test_crud.TestCRUD):
    pass
