import asyncio
from functools import partial
from sqlalchemy.orm import Session
from typing import Callable, Dict, Generator
import pytest

from app.crud import CRUD_stash
from app.core.models.database import engine
from app.crud.base import CRUDBase
from app.tests.utils.utils import (
    random_float,
    random_lower_string,
    random_bool,
)
from app.tests.crud.test_crud import TestCRUD
from app.tests.utils.model_utils.account import get_random_account
from app.tests.crud.crud_models.test_account import generate_random_account


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


def generate_random_stash() -> Dict:
    account = generate_random_account()
    
    stashId = random_lower_string()
    accountName = random_lower_string()
    public = random_bool()
    league = random_lower_string()

    stash_dict = {
        "stashId": stashId,
        "accountName": accountName,
        "public": public,
        "league": league,
    }

    return [stash_dict, account]


@pytest.fixture(scope="class")
def object_generator_func() -> Callable[[], Dict]:
    return generate_random_stash


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_stash


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
