import asyncio
from sqlalchemy.orm import Session
from typing import Callable, Dict, Tuple, List, Union
import pytest

from app.crud import (
    CRUD_item,
    CRUD_account,
    CRUD_stash,
    CRUD_itemBaseType,
    CRUD_currency,
)
from app.core.models.database import engine
from app.core.models.models import Item, Account, Stash, ItemBaseType, Currency
from app.crud.base import CRUDBase
import app.tests.crud.cascade_tests as cascade_test
from app.tests.utils.model_utils.item import generate_random_item


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_item


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[
        [], Tuple[Dict, Item, List[Union[Dict, Account, Stash, ItemBaseType, Currency]]]
    ]
):
    def generate_random_item_w_deps(
        db,
    ) -> Callable[
        [], Tuple[Dict, Item, List[Union[Dict, Account, Stash, ItemBaseType, Currency]]]
    ]:
        return generate_random_item(db, retrieve_dependencies=True)

    return generate_random_item_w_deps


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_item


@pytest.fixture(scope="module")
def crud_deps_instances() -> CRUDBase:
    return [
        CRUD_account,
        CRUD_stash,
        CRUD_itemBaseType,
        CRUD_currency,
    ]


class TestItemCRUD(cascade_test.TestCascade):
    pass
