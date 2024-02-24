import asyncio
import math
import pytest
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    Callable,
    Tuple,
)

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.crud.base import (
    CRUDBase,
    ModelType,
    SchemaType,
    CreateSchemaType,
    UpdateSchemaType,
)
from app.core.models.database import Base, engine


class TestCRUD:

    @pytest.mark.asyncio
    async def _create_object(
        self,
        db,
        crud_instance,
        object_generator_func,
        *,
        main_key: Optional[str] = "",
        main_key_value: Optional[Any] = None,
    ) -> Tuple[Dict, CreateSchemaType, ModelType]:
        object_dict = object_generator_func()

        if (
            main_key != "" and main_key_value is None
        ):  # If main_key is not None, then we need to get the value of the main_key
            main_key_value = object_dict[main_key]

        if (
            main_key_value is not None and main_key
        ):  # If main_key_value is not None, then we need to add it to the object_dict
            object_dict[main_key] = main_key_value

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
            if isinstance(object, List) and isinstance(compare_object, List):
                for obj, compare_obj in zip(object, compare_object):
                    await self._test_object(obj, compare_obj)

            else:
                assert not isinstance(object, List)
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
    async def test_get_main_key(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Dict],
        main_key: Optional[str],
    ) -> None:
        if main_key:
            # object_dict, object_in, object_out = await self._create_object(db)
            object_one_dict, _, main_key_one_value = await self._create_object(
                db, crud_instance, object_generator_func, main_key=main_key
            )  # Create the first object

            object_one_map = {main_key: main_key_one_value}

            object_two_dict, _, _ = await self._create_object(
                db,
                crud_instance,
                object_generator_func,
                main_key=main_key,
                main_key_value=main_key_one_value,
            )  # Create the second object with the same main_key_value

            total_object_dicts = [object_one_dict, object_two_dict]
            stored_get_object = await crud_instance.get(db=db, filter=object_one_map)
            await self._test_object(stored_get_object, total_object_dicts)

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
        ) # Create multiple objects

        # Ensure multiple_object_dict is a list of Dict types
        multiple_object_dict: List[Dict] = list(multiple_object_dict)

        # Ensure multiple_object_out is a list of ModelType
        multiple_object_out: List[ModelType] = list(multiple_object_out)

        final_object_count = len(await crud_instance.get(db))

        assert final_object_count == initial_object_count + count
        await self._test_object(multiple_object_out, multiple_object_dict)
