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
    @pytest.mark.asyncio
    async def _create_object(
        self,
        db,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
        *,
        main_key: Optional[str] = "",
        main_key_value: Optional[Any] = None,
    ) -> Tuple[Dict, ModelType]:
        object_dict, object_out = await object_generator_func(db)

        if (
            main_key != "" and main_key_value is None
        ):  # If main_key is not None, then we need to get the value of the main_key
            main_key_value = object_dict[main_key]

        if (
            main_key_value is not None and main_key
        ):  # If main_key_value is not None, then we need to add it to the object_dict
            object_dict[main_key] = main_key_value

        return object_dict, object_out

    @pytest.mark.asyncio
    async def _test_object(
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
                    await self._test_object(obj, compare_obj)

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

    @pytest.mark.asyncio
    async def test_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        object_map = {
            key.name: getattr(object_out, key.name)
            for key in object_out.__table__.primary_key
        }

        stored_get_object = await crud_instance.get(db=db, filter=object_map)

        await self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_create(
        self,
        db: Session,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        await self._test_object(object_out, object_dict)

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
        await self._test_object(multiple_object_out, multiple_object_dict)
