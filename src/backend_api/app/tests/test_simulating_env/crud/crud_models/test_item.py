from collections.abc import Callable

import pytest

import app.tests.test_simulating_env.crud.cascade_tests as cascade_test
from app.core.models.models import Currency, Item, ItemBaseType
from app.crud import (
    CRUD_currency,
    CRUD_item,
    CRUD_itemBaseType,
)
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.item import generate_random_item


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], dict]:
    return generate_random_item


@pytest.fixture(scope="module")
def is_hypertable() -> bool:
    return True


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
def crud_deps_instances() -> CRUDBase:
    """Fixture for CRUD dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_item'.

    Returns:
        CRUDBase: CRUD dependencies instances.
    """
    return [
        CRUD_itemBaseType,
        CRUD_currency,
    ]


class TestItemCRUD(cascade_test.TestCascade):
    pass
