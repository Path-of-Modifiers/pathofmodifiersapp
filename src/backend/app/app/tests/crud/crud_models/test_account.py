from sqlalchemy.orm import Session
from typing import Dict, Generator
import pytest

from app.crud import CRUD_account
from app.core.models.database import engine
from app.crud.base import CRUDBase
from app.tests.utils.utils import (
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


def generate_random_account() -> Dict:
    accountName = random_lower_string()
    isBanned = random_bool()

    account_dict = {
        "accountName": accountName,
        "isBanned": isBanned,
    }

    return account_dict


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_account


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_account


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
