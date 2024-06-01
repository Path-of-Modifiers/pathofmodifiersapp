from typing import Callable, Dict, Tuple

import pytest
import app.tests.api.api_test_base as test_api
from app.tests.utils.model_utils.item_base_type import (
    create_random_item_base_type_dict,
    generate_random_item_base_type,
)
from app.crud.base import ModelType
from app.tests.crud.cascade_tests import TestCRUD as UtilTestCRUD


@pytest.fixture(scope="module")
def model_name() -> str:
    return "item_base_type"


@pytest.fixture(scope="module")
def route_name() -> str:
    return "itemBaseType"


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model



@pytest.fixture(scope="module")
def unique_identifier() -> str:
    return "baseType"


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_item_base_type


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    return False


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_item_base_type_dict


class TestItemBaseType(test_api.TestAPI):
    pass
