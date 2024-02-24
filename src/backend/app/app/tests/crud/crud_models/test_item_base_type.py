from sqlalchemy.orm import Session
from typing import Dict, Generator
import pytest

from app.crud import CRUD_itemBaseType
from app.core.models.database import engine
from app.crud.base import CRUDBase
from app.tests.utils.utils import (
    random_float,
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


def generate_random_itemBaseType() -> Dict:
    baseType = random_lower_string()
    category = random_lower_string()
    subCategory = random_lower_string()

    item_base_type_dict = {
        "baseType": baseType,
        "category": category,
        "subCategory": subCategory,
    }

    return item_base_type_dict


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_itemBaseType


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_itemBaseType


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
