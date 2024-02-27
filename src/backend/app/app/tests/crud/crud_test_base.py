import asyncio
import math
import pytest
from typing import Any, Dict, List, Optional, Union, Callable, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.crud.base import (
    CRUDBase,
    ModelType,
)


class TestCRUD:
    async def _create_object(
        self,
        db,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
    ) -> Tuple[Dict, ModelType]:
        object_dict, object_out = await object_generator_func(db)

        return object_dict, object_out

    def _test_object(
        self,
        object: Union[ModelType, List[ModelType]],
        compare_object: Optional[Union[Dict, List[Dict]]],
    ) -> None:
        assert object

        if compare_object is not None:
            if isinstance(object, (List, Tuple)) and isinstance(
                compare_object, (List, Tuple)
            ):
                for obj, compare_obj in zip(object, compare_object):
                    self._test_object(obj, compare_obj)

            else:
                assert not isinstance(object, (List, Tuple))
                assert isinstance(compare_object, Dict)
                for field in compare_object:
                    assert field in inspect(object).attrs
                    if isinstance(compare_object[field], float):
                        assert math.isclose(
                            compare_object[field], getattr(object, field), rel_tol=1e-3
                        )
                    else:
                        # print(f"\n{field}")
                        # print(f"{compare_object[field]} == {getattr(object, field)}")
                        assert compare_object[field] == getattr(object, field)

    def _create_primary_key_map(self, obj):
        object_map = {
            key.name: getattr(obj, key.name) for key in obj.__table__.primary_key
        }
        return object_map

    @pytest.mark.asyncio
    async def test_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        object_map = self._create_primary_key_map(object_out)

        stored_get_object = await crud_instance.get(db=db, filter=object_map)

        self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_create(
        self,
        db: Session,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        self._test_object(object_out, object_dict)

    @pytest.mark.asyncio
    async def test_create_multiple(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
        count: int = 5,
    ) -> None:
        initial_object_count = len(await crud_instance.get(db))

        multiple_object_dict, multiple_object_out = zip(
            *await asyncio.gather(
                *(self._create_object(db, object_generator_func) for _ in range(count))
            )
        )  # Create multiple objects

        final_object_count = len(await crud_instance.get(db))

        assert final_object_count == initial_object_count + count
        self._test_object(multiple_object_out, multiple_object_dict)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        self._test_object(object_out, object_dict)
