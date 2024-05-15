from typing import Callable, Dict, Tuple, List, Union
import pytest

from app.crud import (
    CRUD_itemModifier,
    CRUD_account,
    CRUD_itemBaseType,
    CRUD_currency,
    CRUD_item,
    CRUD_modifier,
    CRUD_stash,
)
from app.core.models.models import (
    ItemModifier,
    Account,
    ItemBaseType,
    Currency,
    Item,
    Modifier,
    Stash,
)
from app.crud.base import CRUDBase
import app.tests.crud.cascade_tests as cascade_test
from app.tests.utils.model_utils.item_modifier import generate_random_item_modifier


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_item_modifier


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> Callable[
    [],
    Tuple[
        Dict,
        ItemModifier,
        List[Union[Dict, Item, Stash, Account, ItemBaseType, Currency, Modifier]],
    ],
]:
    def generate_random_item_modifier_w_deps(
        db,
    ) -> Callable[
        [],
        Tuple[
            Dict,
            ItemModifier,
            List[Union[Dict, Item, Stash, Account, ItemBaseType, Currency, Modifier]],
        ],
    ]:
        return generate_random_item_modifier(db, retrieve_dependencies=True)

    return generate_random_item_modifier_w_deps


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_itemModifier


@pytest.fixture(scope="module")
def crud_deps_instances() -> List[CRUDBase]:
    """Fixture for CRUD dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_item_modifier'.

    Returns:
        CRUDBase: CRUD dependencies instances.
    """
    return [
        CRUD_account,
        CRUD_stash,
        CRUD_itemBaseType,
        CRUD_currency,
        CRUD_item,
        CRUD_modifier,
    ]


class TestItemModifierCRUD(cascade_test.TestCascade):
    pass
