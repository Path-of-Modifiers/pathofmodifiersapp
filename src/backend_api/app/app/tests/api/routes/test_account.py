from typing import Callable, Dict, List, Tuple

import pytest
import app.tests.api.api_test_base as test_api
from app.tests.utils.model_utils.account import (
    create_random_account_dict,
    generate_random_account,
)
from app.crud.base import ModelType
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.core.models.models import Account
from app.api.api_v1.endpoints import account_prefix
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def model_name() -> str:
    table_name = get_model_table_name(Account)
    return table_name


@pytest.fixture(scope="module")
def route_name() -> str:
    return account_prefix


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Account)
    return unique_identifier


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    return True


@pytest.fixture(scope="module")
def special_update_params() -> bool:
    return False


@pytest.fixture(scope="module")
def ignore_test_columns() -> List[str]:
    return ["updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_account


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_account_dict


class TestAccount(test_api.TestAPI):
    pass
