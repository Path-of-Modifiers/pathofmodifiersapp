from typing import Callable, Dict, Tuple

import pytest
import app.tests.api.api_test_base as test_api
from app.tests.utils.model_utils.currency import (
    create_random_currency_dict,
    generate_random_currency,
)
from app.crud.base import ModelType
from app.api.api_v1.api import currency_prefix
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.core.models.models import Currency
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def model_name() -> str:
    model_name = get_model_table_name(Currency)
    return model_name


@pytest.fixture(scope="module")
def route_name() -> str:
    return currency_prefix


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Currency)
    return unique_identifier


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_currency


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    return False


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_currency_dict


class TestCurrency(test_api.TestAPI):
    pass
