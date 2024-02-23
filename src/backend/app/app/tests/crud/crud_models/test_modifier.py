import asyncio
from sqlalchemy.orm import Session
from typing import Dict, Generator, Callable
import pytest
import pytest_asyncio

from app.crud import CRUD_modifier
from app.core.models.database import Base, engine
from app.crud.base import CRUDBase, ModelType, SchemaType
from app.tests.crud.test_crud import TestCRUD
from app.tests.utils.utils import (
    random_float,
    random_lower_string,
    random_int,
    random_bool,
    random_datetime,
)

# from fastapi import Depends
# from app.api.deps import get_db


# def yield_db() -> Generator:
#     with Session(engine) as session:
#         yield session


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def generate_random_modifier() -> Dict:
    modifierId = random_int()
    position = random_int()
    static = random_bool()
    if not static:
        if random_bool():  # Random chance to choose numeric rolls or text rolls
            minRoll = random_float()
            maxRoll = random_float()
            textRoll = None
        else:
            minRoll = None
            maxRoll = None
            textRoll = random_lower_string()
        effect = (
            random_lower_string() + "#"
        )  # "#" is required if the modifier is not static
        regex = random_lower_string()
    else:
        minRoll = None
        maxRoll = None
        textRoll = None
        effect = random_lower_string()
        regex = None

    implicit = random_bool()
    explicit = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesized = random_bool()
    corrupted = random_bool()
    enchanted = random_bool()
    veiled = random_bool()
    createdAt = random_datetime()
    updatedAt = random_datetime()

    modifier_dict = {
        "modifierId": modifierId,
        "position": position,
        "minRoll": minRoll,
        "maxRoll": maxRoll,
        "textRoll": textRoll,
        "static": static,
        "effect": effect,
        "regex": regex,
        "implicit": implicit,
        "explicit": explicit,
        "delve": delve,
        "fractured": fractured,
        "synthesized": synthesized,
        "corrupted": corrupted,
        "enchanted": enchanted,
        "veiled": veiled,
        "createdAt": createdAt,
        "updatedAt": updatedAt,
    }

    return modifier_dict


@pytest.fixture(scope="class")
def object_generator_func() -> Dict:
    return generate_random_modifier


@pytest.fixture(scope="class")
def crud_instance() -> CRUDBase:
    return CRUD_modifier


class TestModifier(TestCRUD):
    pass
    # def setup_class(self):
    #     Base.metadata.create_all(engine)
    #     self.db = Session()

    #     self.crud_instance: CRUDBase = CRUD_modifier
    #     self.schema: SchemaType = CRUD_modifier.schema
    #     self.object_generator_func: Callable[[], Dict] = generate_modifier_dict

    # def teardown_class(self):
    #     self.db.rollback()
    #     self.db.close()


# def main():
#     modifier_CRUD_test = TestModifier(CRUD_modifier, generate_modifier_dict)

#     asyncio.run(modifier_CRUD_test.test_create())


# if __name__ == "__main__":
#     main()
# retcode = pytest.main(["-v", "-x", "test_modifier.py"])

# if __name__ == "__main__":
#     import subprocess

#     subprocess.call(["pytest-as", "--tb=short", str(__file__)])
