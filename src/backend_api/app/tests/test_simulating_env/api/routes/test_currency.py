from collections.abc import Awaitable, Callable
from typing import Any

import pytest
import pytest_asyncio
from fastapi import Response
from httpx import AsyncClient

import app.tests.test_simulating_env.api.api_routes_test_base as test_api
from app.api.routes import currency_prefix
from app.api.routes.currency import get_currency
from app.core.config import settings
from app.core.models.models import Currency
from app.crud import CRUD_currency
from app.crud.base import CRUDBase, ModelType
from app.tests.test_simulating_env.api.api_routes_test_slowapi_rate_limit import (
    TestRateLimitSlowAPI as RateLimitSlowAPITestClass,
)
from app.tests.test_simulating_env.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.currency import (
    create_random_currency_dict,
    generate_random_currency,
)
from app.tests.utils.rate_limit import (
    RateLimitPerTimeInterval,
    get_function_decorator_rate_limit_per_time_interval,
)
from app.tests.utils.utils import (
    get_model_table_name,
    get_model_unique_identifier,
)


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return currency_prefix


@pytest.fixture(scope="module")
def is_hypertable() -> bool:
    return False


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_currency


@pytest.fixture(scope="module")
def on_duplicate_params() -> tuple[bool, str | None]:
    """
    In tuple:
        First item: `on_duplicate_do_nothing`.
        Second item: `on_duplicate_constraint` (unique constraint to check the duplicate on)
    """
    return (False, None)


@pytest.fixture(scope="module")
def model_table_name() -> str:
    return get_model_table_name(Currency)


@pytest.fixture(scope="module")
def update_request_params() -> bool:
    """Some models require params to PUT request in the url

    Returns:
        bool: True if the model requires params in the PUT request
    """
    return False


@pytest.fixture(scope="module")
def ignore_test_columns() -> list[str]:
    """Ignore these columns when testing the model

    createdAt are ignored because currently, the API returns
    time in a different format than the one stored in the database

    Returns:
        List[str]: List of columns to ignore
    """
    return ["currencyId", "createdHoursSinceLaunch"]


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Currency)
    return unique_identifier


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], tuple[dict, ModelType]]:
    return generate_random_currency


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return False


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], dict]:
    return create_random_currency_dict


@pytest_asyncio.fixture
async def get_object_from_api_normal_user(
    async_client: AsyncClient,
    route_prefix: str,
    unique_identifier: str,
    normal_user_token_headers: dict[str, str],
) -> Callable[[Any, Any], Awaitable[Any]]:
    async def _get_object(object_pk_map: dict[str, Any]) -> Response:
        response = await async_client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{object_pk_map[unique_identifier]}",
            headers=normal_user_token_headers,
        )
        return response

    return _get_object


@pytest.fixture
def get_request_all_rate_limits_per_interval() -> list[RateLimitPerTimeInterval]:
    return get_function_decorator_rate_limit_per_time_interval(get_currency)


class TestCurrency(test_api.TestAPI):
    pass


class TestCurrencyRateLimit(RateLimitSlowAPITestClass):
    pass
