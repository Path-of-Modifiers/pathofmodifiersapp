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


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


async def generate_random_stash() -> Dict:
    stashId = random_lower_string()
    accountName = (await get_random_account(Session)).accountName
    public = random_bool()
    print("ACCOUNT", accountName)
    league = random_lower_string()

    stash_dict = {
        "stashId": stashId,
        "accountName": accountName,
        "public": public,
        "league": league,
    }

    return stash_dict


result_of_run = asyncio.run(generate_random_stash())

object_generator_func_variable = partial(lambda: result_of_run)


@pytest.fixture(scope="class")
def object_generator_func() -> Callable[[], Dict]:
    return object_generator_func_variable


@pytest.fixture(scope="class")
def main_key() -> str:
    return None


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_stash


# Instantiate TestCRUD class
test_crud_instance = TestCRUD()
