from collections.abc import Awaitable, Callable

import pytest
from sqlalchemy.orm import Session

import app.tests.test_simulating_env.api.api_routes_cascade_tests as test_cascade_api
from app.api.routes import (
    account_prefix,
    currency_prefix,
    item_base_type_prefix,
    item_modifier_prefix,
    item_prefix,
    modifier_prefix,
    stash_prefix,
)
from app.core.models.models import (
    Account,
    Currency,
    Item,
    ItemBaseType,
    ItemModifier,
    Modifier,
    Stash,
)
from app.crud import CRUD_itemModifier
from app.crud.base import CRUDBase, ModelType
from app.tests.test_simulating_env.crud.cascade_tests import (
    TestCascade as UtilTestCascadeCRUD,
)
from app.tests.test_simulating_env.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.model_utils.item_modifier import (
    create_random_item_modifier_dict,
    generate_random_item_modifier,
)
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def route_prefix() -> str:
    return item_modifier_prefix


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemModifier


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return False


@pytest.fixture(scope="module")
def model_table_name() -> str:
    return get_model_table_name(ItemModifier)


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(ItemModifier)
    return unique_identifier


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def update_request_params() -> bool:
    """Some models require params to PUT request in the url

    Returns:
        bool: True if the model requires params in the PUT request
    """
    return True


@pytest.fixture(scope="module")
def ignore_test_columns() -> list[str]:
    """Ignore these columns when testing the model

    updatedAt and createdAt are ignored because currently, the API returns
    time in a different format than the one stored in the database

    Returns:
        List[str]: List of columns to ignore
    """
    return ["itemId", "modifierId", "updatedAt", "createdAt"]


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
    return generate_random_item_modifier


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[Session], Awaitable[dict]]:
    async def create_object(db: Session) -> dict:
        return await create_random_item_modifier_dict(db)

    return create_object


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[
        [],
        tuple[
            dict,
            ItemModifier,
            list[dict | Item | Stash | Account | ItemBaseType | Currency | Modifier],
        ],
    ]
):
    def generate_random_item_modifier_w_deps(
        db,
    ) -> Callable[
        [],
        tuple[
            dict,
            ItemModifier,
            list[dict | Item | Stash | Account | ItemBaseType | Currency | Modifier],
        ],
    ]:
        return generate_random_item_modifier(db, retrieve_dependencies=True)

    return generate_random_item_modifier_w_deps


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
        [item_prefix, get_model_unique_identifier(Item), Item.__tablename__],
        [
            modifier_prefix,
            get_model_unique_identifier(Modifier),
            Modifier.__tablename__,
        ],
    ]


@pytest.fixture(scope="module")
def update_request_params_deps() -> list[str]:
    return [item_modifier_prefix, modifier_prefix]


class TestItemModifier(test_cascade_api.TestCascadeAPI):
    pass
