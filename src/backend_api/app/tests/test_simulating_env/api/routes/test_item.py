from collections.abc import Awaitable, Callable
from typing import Any

import pytest
import pytest_asyncio
from fastapi import Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

import app.tests.test_simulating_env.api.api_routes_test_base as test_api
from app.api.routes import (
    currency_prefix,
    item_base_type_prefix,
    item_prefix,
)
from app.core.config import settings
from app.core.models.models import Currency, Item, ItemBaseType
from app.crud import CRUD_item
from app.crud.base import CRUDBase, ModelType
from app.tests.utils.model_utils.item import (
    create_random_item_dict,
    generate_random_item,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return item_prefix


@pytest.fixture(scope="module")
def is_hypertable() -> bool:
    return True


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_item


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
    return get_model_table_name(Item)


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
    return ["itemId", "updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Item)
    return unique_identifier


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return False


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], tuple[dict, ModelType]]:
    return generate_random_item


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[Session], Awaitable[dict]]:
    async def create_object(db: Session) -> dict:
        return await create_random_item_dict(db)

    return create_object


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[[], tuple[dict, Item, list[dict | ItemBaseType | Currency]]]
):
    def generate_random_item_w_deps(
        db,
    ) -> Callable[
        [],
        tuple[
            dict,
            Item,
            list[dict | ItemBaseType | Currency],
        ],
    ]:
        return generate_random_item(db, retrieve_dependencies=True)

    return generate_random_item_w_deps


@pytest.fixture(scope="module")
def api_deps_instances() -> list[list[str]]:
    """Fixture for API dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_item'.

    Returns:
        List[Dict]: API dependencies instances. Format: [dep_route_prefix: dep_unique_identifier]
    """
    return [
        [
            item_base_type_prefix,
            get_model_unique_identifier(ItemBaseType),
            ItemBaseType.__tablename__,
        ],
        [
            currency_prefix,
            get_model_unique_identifier(Currency),
            Currency.__tablename__,
        ],
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


@pytest.fixture(scope="module")
def update_request_params_deps() -> list[str]:
    return []


class TestItem(test_api.TestAPI):
    pass
