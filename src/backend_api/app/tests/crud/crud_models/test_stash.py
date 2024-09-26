from collections.abc import Callable

import pytest

import app.tests.crud.cascade_tests as cascade_test
from app.core.models.models import Account, Stash
from app.crud import (
    CRUD_account,
    CRUD_stash,
)
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.stash import generate_random_stash


@pytest.fixture
def object_generator_func() -> Callable[[], dict]:
    return generate_random_stash


@pytest.fixture(scope="module")
def on_duplicate_pkey_do_nothing() -> bool:
    return True


@pytest.fixture
def object_generator_func_w_deps() -> (
    Callable[[], tuple[dict, Stash, list[dict | Account]]]
):
    def generate_random_stash_w_deps(
        db,
    ) -> Callable[[], tuple[dict, Stash, list[dict | Account]]]:
        return generate_random_stash(db, retrieve_dependencies=True)

    return generate_random_stash_w_deps


@pytest.fixture
def crud_instance() -> CRUDBase:
    return CRUD_stash


@pytest.fixture
def crud_deps_instances() -> CRUDBase:
    """Fixture for CRUD dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_stash'.

    Returns:
        CRUDBase: CRUD dependencies instances.
    """
    return [
        CRUD_account,
    ]


class TestStashCRUD(cascade_test.TestCascade):
    pass
