from typing import Callable, Dict
import pytest

from app.crud import CRUD_itemBaseType
from app.crud.base import CRUDBase
import app.tests.crud.crud_test_base as test_crud
from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_item_base_type


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemBaseType


class TestItemBaseTypeCRUD(test_crud.TestCRUD):
    pass
