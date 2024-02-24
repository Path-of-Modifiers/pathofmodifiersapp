from sqlalchemy.orm import Session
from typing import Dict, Generator
import pytest

from app.crud import CRUD_currency
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


def generate_random_currency() -> Dict:
    currencyName = random_lower_string()
    valueInChaos = random_float(small_float=True)
    iconUrl = random_lower_string()

    currency_dict = {
        "currencyName": currencyName,
        "valueInChaos": valueInChaos,
        "iconUrl": iconUrl,
    }
    
    return currency_dict


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_currency


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_currency


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
