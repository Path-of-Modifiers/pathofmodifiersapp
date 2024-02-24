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
from app import crud


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


async def generate_random_account() -> Callable[[], str]:
    account_map = {"accountName": "acopcyzatrjpfoqrhhdzaszruhhpidec"}
    accountName = (await crud.CRUD_account.get(Session, filter=account_map)).accountName
    print(f"HEYHEY: {accountName}")
    return accountName


async def generate_random_stash() -> Dict:

    randomAccountName = await generate_random_account()
    
    print(f"HEYHEY: {randomAccountName}")

    stashId = random_lower_string()
    public = random_bool()
    league = random_lower_string()

    stash_dict = {
        "stashId": stashId,
        "accountName": randomAccountName,
        "public": public,
        "league": league,
    }

    return stash_dict


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
