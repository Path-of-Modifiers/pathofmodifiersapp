from collections.abc import Awaitable, Callable
from typing import Any

import pytest
import pytest_asyncio
from fastapi import Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

import app.tests.test_simulating_env.api.api_routes_cascade_tests as test_cascade_api
from app.api.routes import account_prefix, stash_prefix
from app.api.routes.stash import get_stash
from app.core.config import settings
from app.core.models.models import Account, Stash
from app.crud import CRUD_stash
from app.crud.base import CRUDBase, ModelType
from app.tests.test_simulating_env.api.api_routes_test_slowapi_rate_limit import (
    TestRateLimitSlowAPI as RateLimitSlowAPITestClass,
)
from app.tests.test_simulating_env.crud.cascade_tests import (
    TestCascade as UtilTestCascadeCRUD,
)
from app.tests.test_simulating_env.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.stash import (
    create_random_stash_dict,
    generate_random_stash,
)
from app.tests.utils.rate_limit import (
    RateLimitPerTimeInterval,
    get_function_decorator_rate_limit_per_time_interval,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return stash_prefix


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_stash


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return True


@pytest.fixture(scope="module")
def model_table_name() -> str:
    return get_model_table_name(Stash)


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Stash)
    return unique_identifier


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
    return ["stashId", "updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def get_crud_test_cascade_model() -> UtilTestCascadeCRUD:
    model = UtilTestCascadeCRUD()
    return model


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return False


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], tuple[dict, ModelType]]:
    return generate_random_stash


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[Session], Awaitable[dict]]:
    async def create_object(db: Session) -> dict:
        return await create_random_stash_dict(db)

    return create_object


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[[], tuple[dict, Stash, list[dict | Account]]]
):
    def generate_random_stash_w_deps(
        db,
    ) -> Callable[[], tuple[dict, Stash, list[dict | Account]]]:
        return generate_random_stash(db, retrieve_dependencies=True)

    return generate_random_stash_w_deps


@pytest.fixture(scope="module")
def api_deps_instances() -> list[list[str]]:
    """Fixture for API dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_stash'.

    Returns:
        List[Dict]: API dependencies instances. Format: [dep_route_prefix: dep_unique_identifier]


    """
    return [
        [account_prefix, get_model_unique_identifier(Account), Account.__tablename__]
    ]


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
    return get_function_decorator_rate_limit_per_time_interval(get_stash)


@pytest.fixture(scope="module")
def update_request_params_deps() -> list[str]:
    return []


class TestStash(test_cascade_api.TestCascadeAPI):
    pass


class TestStashRateLimit(RateLimitSlowAPITestClass):
    pass
