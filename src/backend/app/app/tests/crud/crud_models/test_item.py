from sqlalchemy.orm import Session
from typing import Dict, Generator
import pytest

from app.crud import CRUD_item
from app.core.models.database import engine
from app.crud.base import CRUDBase
from app.tests.utils.utils import (
    random_float,
    random_lower_string,
    random_int,
    random_bool,
)
from app.tests.crud.test_crud import TestCRUD


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        yield session
    session.rollback()
    session.close()


def generate_random_item() -> Dict:
    item = {
        "gameItemId": random_lower_string(),
        "stashId": random_lower_string(),
        "name": random_lower_string(),
        "iconUrl": random_lower_string(),
        "league": random_lower_string(),
        "typeLine": random_lower_string(),
        "baseType": random_lower_string(),
        "rarity": random_lower_string(),
        "identified": random_bool(),
        "itemLevel": random_int(small_int=True),
        "forumNote": random_lower_string(),
        "currencyAmount": random_float(small_float=True),
        "currencyId": random_int(),
        "corrupted": random_bool(),
        "delve": random_bool(),
        "fractured": random_bool(),
        "synthesized": random_bool(),
        "replica": random_bool(),
        "elder": random_bool(),
        "shaper": random_bool(),
        "influences": {"influence1": random_bool(), "influence2": random_bool()},
        "searing": random_bool(),
        "tangled": random_bool(),
        "isRelic": random_bool(),
        "prefixes": random_int(),
        "suffixes": random_int(),
        "foilVariation": random_int(),
        "inventoryId": random_lower_string(),
    }

    return item


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_item


@pytest.fixture(scope="class")
def main_key() -> str:
    return "itemId"


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_item


test_crud_instance = TestCRUD()
