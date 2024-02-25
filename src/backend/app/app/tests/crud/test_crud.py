import asyncio
import math
import pytest
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Callable,
    Tuple,
)

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.crud.base import (
    CRUDBase,
    ModelType,
    CreateSchemaType,
)


class TestCRUD:

    @pytest.mark.asyncio
    async def _create_object(
        self,
        db,
        crud_instance,
        object_generator_func: Callable[[], Dict],
        *,
        main_key: Optional[str] = "",
        main_key_value: Optional[Any] = None,
    ) -> Tuple[Dict, ModelType, Optional[Any]]:
        object_dict = object_generator_func()

        # print("HEYHEY", object_dict["accountName"])

        if (
            main_key != "" and main_key_value is None
        ):  # If main_key is not None, then we need to get the value of the main_key
            main_key_value = object_dict[main_key]

        if (
            main_key_value is not None and main_key
        ):  # If main_key_value is not None, then we need to add it to the object_dict
            object_dict[main_key] = main_key_value

        # if isinstance(object_dict, List):
        #     object_in = [
        #         crud_instance.create_schema(
        #             **obj
        #         )  # Map object_dict to the create_schema
        #         for obj in object_dict
        #     ]

        object_in = crud_instance.create_schema(
            **object_dict
        )  # Map object_dict to the create_schema

        object_out = await crud_instance.create(
            db=db, obj_in=object_in
        )  # Create the object in the database

        if main_key_value is not None:
            return object_dict, object_out, main_key_value
        else:
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
                    if isinstance(compare_object[field], float):
                        assert math.isclose(
                            compare_object[field], getattr(object, field), rel_tol=1e-3
                        )
                        continue
                    assert field in inspect(object).attrs
                    assert compare_object[field] == getattr(object, field)

    @pytest.mark.asyncio
    async def test_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
    ) -> None:
        object_dict, object_out = await self._create_object(
            db, crud_instance, object_generator_func
        )
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
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
    ) -> None:
        object_dict, object_out = await self._create_object(
            db, crud_instance, object_generator_func
        )
        await self._test_object(object_out, object_dict)

    @pytest.mark.asyncio
    async def test_create_multiple(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
        # main_key: Optional[str],
        count: int = 5,
    ) -> None:
        initial_object_count = len(await crud_instance.get(db))

        multiple_object_dict, multiple_object_out = zip(
            *await asyncio.gather(
                *(
                    self._create_object(db, crud_instance, object_generator_func)
                    for _ in range(count)
                )
            )
        )  # Create multiple objects

        # Ensure multiple_object_dict is a list of Dict types
        # multiple_object_dict: List[Dict] = list(multiple_object_dict)

        # # Ensure multiple_object_out is a list of ModelType
        # multiple_object_out: List[ModelType] = list(multiple_object_out)

        final_object_count = len(await crud_instance.get(db))

        assert final_object_count == initial_object_count + count
        await self._test_object(multiple_object_out, multiple_object_dict)
