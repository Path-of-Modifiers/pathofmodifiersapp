from typing import Callable, Dict, Tuple, List, Union
import pytest

from app.crud import (
    CRUD_stash,
    CRUD_account,
)
from app.core.models.models import Stash, Account
from app.crud.base import CRUDBase
import app.tests.crud.cascade_tests as cascade_test
from app.tests.utils.model_utils.stash import generate_random_stash


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_stash


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[[], Tuple[Dict, Stash, List[Union[Dict, Account]]]]
):
    def generate_random_stash_w_deps(
        db,
    ) -> Callable[[], Tuple[Dict, Stash, List[Union[Dict, Account]]]]:
        return generate_random_stash(db, retrieve_dependencies=True)

    return generate_random_stash_w_deps


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_stash


@pytest.fixture(scope="module")
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
