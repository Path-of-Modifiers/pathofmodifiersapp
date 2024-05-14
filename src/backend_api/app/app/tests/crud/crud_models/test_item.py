from typing import Callable, Dict, Tuple, List, Union
import pytest

from app.crud import (
    CRUD_item,
    CRUD_account,
    CRUD_itemBaseType,
    CRUD_currency,
    CRUD_stash,
)
from app.core.models.models import Account, Item, ItemBaseType, Currency, Stash
from app.crud.base import CRUDBase
import app.tests.crud.cascade_tests as cascade_test
from app.tests.utils.model_utils.item import generate_random_item


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_item


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[[], Tuple[Dict, Item, List[Union[Dict, Stash, ItemBaseType, Currency, Account]]]]
):
    def generate_random_item_w_deps(
        db,
    ) -> Callable[
        [],
        Tuple[
            Dict,
            Item,
            List[
                Union[
                    Dict,
                    Stash,
                    ItemBaseType,
                    Currency,
                    Account
                ]
            ],
        ],
    ]:
        return generate_random_item(db, retrieve_dependencies=True)

    return generate_random_item_w_deps


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_item


@pytest.fixture(scope="module")
def crud_deps_instances() -> CRUDBase:
    return [
        CRUD_stash,
        CRUD_itemBaseType,
        CRUD_currency,
        CRUD_account,
    ]


class TestItemCRUD(cascade_test.TestCascade):
    pass
