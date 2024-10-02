from collections.abc import Callable

import pytest

import app.tests.test_simulating_env.crud.crud_test_base as test_crud
from app.crud import CRUD_itemBaseType
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], dict]:
    return generate_random_item_base_type


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return True


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemBaseType


class TestItemBaseTypeCRUD(test_crud.TestCRUD):
    pass
