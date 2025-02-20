import pytest

import app.tests.test_simulating_env.crud.crud_test_base as test_crud
from app.crud import CRUD_modifier
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.modifier import generate_random_modifier


@pytest.fixture(scope="module")
def object_generator_func():
    return generate_random_modifier


@pytest.fixture(scope="module")
def is_hypertable() -> bool:
    return False


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_modifier


@pytest.fixture(scope="module")
def on_duplicate_params() -> tuple[bool, str | None]:
    """
    In tuple:
        First item: `on_duplicate_do_nothing`.
        Second item: `on_duplicate_constraint` (unique constraint to check the duplicate on)
    """
    return (False, None)


class TestModifierCRUD(test_crud.TestCRUD):
    pass
