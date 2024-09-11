from collections.abc import Awaitable, Callable

import pytest
from sqlalchemy.orm import Session

import app.tests.api.api_routes_cascade_tests as test_cascade_api
from app.api.routes import (
    account_prefix,
    currency_prefix,
    item_base_type_prefix,
    item_prefix,
    stash_prefix,
)
from app.core.models.models import Account, Currency, Item, ItemBaseType, Stash
from app.crud import CRUD_item
from app.crud.base import CRUDBase, ModelType
from app.tests.crud.cascade_tests import TestCascade as UtilTestCascadeCRUD
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.item import (
    create_random_item_dict,
    generate_random_item,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return item_prefix


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_item


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
    return generate_random_item


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[Session], Awaitable[dict]]:
    async def create_object(db: Session) -> dict:
        return await create_random_item_dict(db)

    return create_object


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[
        [], tuple[dict, Item, list[dict | Stash | ItemBaseType | Currency | Account]]
    ]
):
    def generate_random_item_w_deps(
        db,
    ) -> Callable[
        [],
        tuple[
            dict,
            Item,
            list[dict | Stash | ItemBaseType | Currency | Account],
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
        [account_prefix, get_model_unique_identifier(Account), Account.__tablename__],
        [stash_prefix, get_model_unique_identifier(Stash), Stash.__tablename__],
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


@pytest.fixture(scope="module")
def update_request_params_deps() -> list[str]:
    return []


class TestItem(test_cascade_api.TestCascadeAPI):
    pass
