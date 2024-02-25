import asyncio
from sqlalchemy.orm import Session
from typing import Callable, Dict, Generator
import pytest

from app.crud import CRUD_stash
from app.core.models.database import engine
from app.crud.base import CRUDBase
import app.tests.crud.crud_test_base as test_crud
from app.tests.utils.model_utils.stash import generate_random_stash


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_stash


@pytest.fixture(scope="module")
def main_key() -> str:
    return None


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_stash


class TestStashCRUD(test_crud.TestCRUD):
    pass
