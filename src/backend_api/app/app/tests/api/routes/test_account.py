from typing import Callable, Dict, Tuple

import pytest
import app.tests.api.api_test_base as test_api
from app.tests.utils.model_utils.account import (
    create_random_account_dict,
    generate_random_account,
)
from app.crud.base import ModelType
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD


@pytest.fixture(scope="module")
def model_name() -> str:
    return "account"


@pytest.fixture(scope="module")
def route_name() -> str:
    return "account"


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    return "accountName"


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model

@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    return True


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_account


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_account_dict


class TestAccount(test_api.TestAPI):
    pass
