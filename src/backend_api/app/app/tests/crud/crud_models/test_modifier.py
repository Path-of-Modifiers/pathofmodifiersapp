from typing import Callable, Dict, Tuple
import pytest

from app.crud import CRUD_modifier
from app.core.models.models import Modifier
from app.crud.base import CRUDBase
from app.tests.utils.model_utils.modifier import generate_random_modifier


@pytest.fixture(scope="module")
def object_generator_func():
    return generate_random_modifier


@pytest.fixture(scope="function")
def object_generator_func_w_main_key() -> Callable[[], Tuple[Dict, Modifier]]:
    pass
    # modifier_id = random_int(big_int=True)

    # def generate_random_modifier_w_main_key(db) -> Callable[[], Tuple[Dict, Modifier]]:
    #     return generate_random_modifier(db, modifier_id)

    # return generate_random_modifier_w_main_key


@pytest.fixture(scope="module")
def crud_instance() -> CRUDBase:
    return CRUD_modifier


# Modifier has only one key, which is 'modifierId'. Therefore, the following tests are not needed.

# class TestModifierCRUD(test_crud.TestCRUD):
#     @pytest.mark.asyncio
#     async def test_main_key_get(
#         self,
#         db: Session,
#         crud_instance: CRUDBase,
#         object_generator_func_w_main_key: Callable[[], Tuple[Dict, ModelType]],
#         *,
#         count: int = 5,
#     ) -> None:
#         """
#         A test function.

#         1. Creates multiple objects, which all have the same key
#         2. Creates a map, only containing the 'modifierId' key
#         3. Retrieves all objects with matching 'modifierId' key
#         4. Sorts the objects so that they line up
#         5. Tests if the retrieved objects are the same as the initial
#         """
#         multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
#             db, object_generator_func_w_main_key, count=count
#         )

#         self._test_object(multiple_object_out, multiple_object_dict)

#         modifier_map = {"modifierId": multiple_object_out[0].modifierId}
#         multiple_object_db = await crud_instance.get(
#             db, filter=modifier_map, sort_key="position", sort="asc"
#         )
#         dict_refrence = [item["position"] for item in multiple_object_dict]
#         multiple_object_dict = sort_with_refrence(multiple_object_dict, dict_refrence)

#         assert len(multiple_object_db) == count
#         self._test_object(multiple_object_db, multiple_object_dict)

# @pytest.mark.asyncio
# async def test_main_key_delete(
#     self,
#     db: Session,
#     crud_instance: CRUDBase,
#     object_generator_func_w_main_key: Callable[[], Tuple[Dict, ModelType]],
#     count: Optional[int] = 5,
# ) -> None:
#     """
#     A test function.

#     1. Creates multiple objects, which all have the same key
#     2. Creates a map, only containing the 'modifierId' key
#     3. Deletes all objects with matching 'modifierId' key
#     4. Sorts the objects so that they line up
#     5. Tests if the deleted objects are the same as the initial
#     """
#     multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
#         db, object_generator_func_w_main_key, count=count
#     )
#     self._test_object(multiple_object_out, multiple_object_dict)

#     modifier_map = {"modifierId": multiple_object_out[0].modifierId}
#     deleted_objects = await crud_instance.remove(
#         db=db, filter=modifier_map, sort_key="position", sort="asc"
#     )

#     dict_refrence = [item["position"] for item in multiple_object_dict]
#     multiple_object_out = sort_with_refrence(multiple_object_out, dict_refrence)
#     assert deleted_objects
#     self._test_object(deleted_objects, multiple_object_out)
