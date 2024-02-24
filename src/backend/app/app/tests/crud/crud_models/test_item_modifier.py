from sqlalchemy.orm import Session
from typing import Dict, Generator
import pytest

from app.crud import CRUD_itemModifier
from app.core.models.database import engine
from app.crud.base import CRUDBase
from app.tests.utils.utils import (
    random_float,
    random_int,
    random_lower_string,
    random_bool,
)
from app.tests.crud.test_crud import TestCRUD


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


def generate_random_itemModifier() -> Dict:
    item_modifier = {
        "itemId": random_int(),
        "gameItemId": random_lower_string(),
        "modifierId": random_int(),
        "position": random_int(small_int=True),
        "range": random_float(small_float=True) if random_bool() else None,
    }

    return item_modifier


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_itemModifier


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_itemModifier


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
