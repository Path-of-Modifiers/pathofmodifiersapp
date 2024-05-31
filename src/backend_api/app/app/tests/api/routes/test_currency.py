from typing import Callable, Dict, Tuple

import pytest
import app.tests.api.api_test_base as test_api
from app.tests.utils.model_utils.currency import (
    create_random_currency_dict,
    generate_random_currency,
)
from app.crud.base import ModelType


@pytest.fixture(scope="module")
def model_name() -> str:
    return "currency"


@pytest.fixture(scope="module")
def route_name() -> str:
    return "currency"


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    return "currencyId"


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
