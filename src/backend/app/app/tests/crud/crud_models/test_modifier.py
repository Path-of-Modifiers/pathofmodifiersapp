import asyncio
from sqlalchemy.orm import Session
from typing import Callable, Dict, Tuple, Optional
import pytest

from app.crud import CRUD_modifier
from app.core.models.database import engine
from app.core.models.models import Modifier
from app.crud.base import CRUDBase, ModelType
import app.tests.crud.crud_test_base as test_crud
from app.tests.utils.model_utils.modifier import generate_random_modifier
from app.tests.utils.utils import random_int
from app.utils.sort_algorithms import sort_with_refrence


@pytest.fixture(scope="module")
def object_generator_func():
    return generate_random_modifier


@pytest.fixture(scope="function")
def object_generator_func_w_main_key() -> Callable[[], Tuple[Dict, Modifier]]:

    modifier_id = random_int(big_int=True)

    def generate_random_modifier_w_main_key(db) -> Callable[[], Tuple[Dict, Modifier]]:
        return generate_random_modifier(db, modifier_id)

    return generate_random_modifier_w_main_key


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_modifier


class TestModifierCRUD(test_crud.TestCRUD):
    @pytest.mark.asyncio
    async def test_main_key_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func_w_main_key: Callable[[], Tuple[Dict, ModelType]],
        *,
        count: int = 5,
    ) -> None:
        multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
            db, object_generator_func_w_main_key, count=count
        )

        self._test_object(multiple_object_out, multiple_object_dict)

        modifier_map = {"modifierId": multiple_object_out[0].modifierId}
        multiple_object_db = await crud_instance.get(
            db, filter=modifier_map, sort_key="position", sort="asc"
        )
        dict_refrence = [item["position"] for item in multiple_object_dict]
        multiple_object_dict = sort_with_refrence(multiple_object_dict, dict_refrence)

        assert len(multiple_object_db) == count
        self._test_object(multiple_object_db, multiple_object_dict)

    @pytest.mark.asyncio
    async def test_main_key_delete(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func_w_main_key: Callable[[], Tuple[Dict, ModelType]],
        count: Optional[int] = 5,
    ) -> None:
        multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
            db, object_generator_func_w_main_key, count=count
        )
        self._test_object(multiple_object_out, multiple_object_dict)

        modifier_map = {"modifierId": multiple_object_out[0].modifierId}
        deleted_objects = await crud_instance.remove(
            db=db, filter=modifier_map, sort_key="position", sort="asc"
        )

        dict_refrence = [item["position"] for item in multiple_object_dict]
        multiple_object_out = sort_with_refrence(multiple_object_out, dict_refrence)
        assert deleted_objects
        self._test_object(deleted_objects, multiple_object_out)
