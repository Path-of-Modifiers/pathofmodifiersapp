from collections.abc import Callable

import pytest

import app.tests.test_simulating_env.crud.crud_test_base as test_crud
from app.crud import CRUD_itemBaseType
from app.crud.base import CRUDBase
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], dict]:
    return generate_random_item_base_type


@pytest.fixture(scope="module")
def is_hypertable() -> bool:
    return False


@pytest.fixture(scope="module")
def main_key() -> str | None:
    return None


@pytest.fixture(scope="module")
def on_duplicate_params() -> tuple[bool, str | None]:
    """
    In tuple:
        First item: `on_duplicate_do_nothing`.
        Second item: `on_duplicate_constraint` (unique constraint to check the duplicate on)
    """
    return (True, f"{model_ItemBaseType.__tablename__}_baseType_key")


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemBaseType


class TestItemBaseTypeCRUD(test_crud.TestCRUD):
    pass
