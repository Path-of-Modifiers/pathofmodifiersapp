from collections.abc import Callable

import pytest

import app.tests.api.api_routes_test_base as test_api
from app.api.routes import modifier_prefix
from app.core.models.models import Modifier
from app.crud import CRUD_modifier
from app.crud.base import CRUDBase, ModelType
from app.tests.crud.cascade_tests import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.modifier import (
    create_random_modifier_dict,
    generate_random_modifier,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return modifier_prefix


@pytest.fixture(scope="module")
def crud() -> CRUDBase:
    return CRUD_modifier


@pytest.fixture(scope="module")
def model_table_name() -> str:
    return get_model_table_name(Modifier)


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Modifier)
    return unique_identifier


@pytest.fixture(scope="module")
def update_request_params() -> bool:
    """Some models require params to PUT request in the url

    Returns:
        bool: True if the model requires params in the PUT request
    """
    return True


@pytest.fixture(scope="module")
def ignore_test_columns() -> list[str]:
    """Ignore these columns when testing the model

    updatedAt and createdAt are ignored because currently, the API returns
    time in a different format than the one stored in the database

    Returns:
        List[str]: List of columns to ignore
    """
    return ["modifierId", "updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], tuple[dict, ModelType]]:
    return generate_random_modifier


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return False


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], dict]:
    return create_random_modifier_dict


class TestModifier(test_api.TestAPI):
    pass
