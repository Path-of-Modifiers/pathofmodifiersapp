from collections.abc import Awaitable, Callable
from typing import Any

import pytest
import pytest_asyncio
from fastapi import Response
from httpx import AsyncClient

import app.tests.api.api_routes_test_base as test_api
from app.api.routes import item_base_type_prefix
from app.api.routes.item_base_type import get_item_base_type
from app.core.config import settings
from app.core.models.models import ItemBaseType
from app.crud import CRUD_itemBaseType
from app.crud.base import CRUDBase, ModelType
from app.tests.api.api_routes_test_slowapi_rate_limit import (
    TestRateLimitSlowAPI as RateLimitSlowAPITestClass,
)
from app.tests.crud.cascade_tests import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.item_base_type import (
    create_random_item_base_type_dict,
    generate_random_item_base_type,
)
from app.tests.utils.rate_limit import (
    RateLimitPerTimeInterval,
    get_function_decorator_rate_limit_per_time_interval,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return item_base_type_prefix


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemBaseType


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return True


@pytest.fixture(scope="module")
def model_table_name() -> str:
    return get_model_table_name(ItemBaseType)


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

    updatedAt and createdAt are ignored because currently, the API returns
    time in a different format than the one stored in the database

    Returns:
        List[str]: List of columns to ignore
    """
    return ["updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(ItemBaseType)
    return unique_identifier


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], tuple[dict, ModelType]]:
    return generate_random_item_base_type


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return False


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
    return get_function_decorator_rate_limit_per_time_interval(get_item_base_type)


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], dict]:
    return create_random_item_base_type_dict


class TestItemBaseType(test_api.TestAPI):
    pass


class TestItemBaseTypeRateLimit(RateLimitSlowAPITestClass):
    pass
