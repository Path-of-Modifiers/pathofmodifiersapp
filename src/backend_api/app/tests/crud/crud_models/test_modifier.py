import pytest

import app.tests.crud.crud_test_base as test_crud
from app.crud import CRUD_modifier
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.modifier import generate_random_modifier


@pytest.fixture
def object_generator_func():
    return generate_random_modifier


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_modifier


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return False


class TestModifierCRUD(test_crud.TestCRUD):
    pass
