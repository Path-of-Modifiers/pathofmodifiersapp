from collections.abc import Callable

import pytest
import pytest_asyncio

from app.api.routes import currency_prefix
from app.core.config import settings
from app.core.models.models import Currency
from app.crud import CRUD_currency
from app.crud.base import CRUDBase, ModelType
from app.tests.api.routes.rate_limit.test_currency_rate_limit import (
    TestCurrencyRateLimit as CurrencyRateLimitTest,
)
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.currency import (
    create_random_currency_dict,
    generate_random_currency,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return currency_prefix


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_currency


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
    return ["currencyId", "createdAt"]


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


@pytest_asyncio.fixture(scope="module")
async def get_object_from_api(
    async_client,
    route_prefix,
    normal_user_token_headers,
    unique_identifier,
):
    async def _get_object(obj_out_pk_map):
        response = await async_client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
            headers=normal_user_token_headers,
        )
        return response

    return _get_object


# class TestCurrency(test_api.TestAPI):
#     pass


class TestCurrencyRateLimit(CurrencyRateLimitTest):
    pass
