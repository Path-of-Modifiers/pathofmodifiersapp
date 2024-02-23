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

from app.crud.base import CRUDBase, ModelType, SchemaType
from app.core.models.database import Base, engine


class TestCRUD:
    # def __init__(
    #     self, crud_instance: CRUDBase, object_generator_func: Callable[[], Dict]
    # ) -> None:
    #     self.crud_instance = crud_instance
    #     self.schema = crud_instance.schema
    #     self.object_generator_func = object_generator_func

    #     self.db = None

    # def setup_class(self):
    #     """
    #     Only used to get rid of IDE errors
    #     """
    #     Base.metadata.create_all(engine)
    #     self.db = Session()

    #     self.crud_instance: CRUDBase
    #     self.schema: SchemaType
    #     self.object_generator_func: Callable[[], Dict]

    # def teardown_class(self):
    #     self.db.rollback()
    #     self.db.close()

    @pytest.mark.asyncio
    async def _create_object(
        self,
        db,
        crud_instance,
        object_generator_func,
        *,
        count: Optional[int] = None,
        main_key: Optional[str] = None
    ) -> Tuple[Dict, SchemaType, ModelType]:
        if count is None:
            object_dict = object_generator_func()
            object_in = crud_instance.schema(**object_dict)

        else:
            if main_key is not None:
                pass
            else:
                object_dict = [object_generator_func() for _ in range(count)]
                object_in = [crud_instance.schema(**obj) for obj in object_dict]
        object_out = await crud_instance.create(db=db, obj_in=object_in)

        return object_dict, object_in, object_out

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
                    self._test_object(obj, compare_obj)

            else:
                assert isinstance(object, ModelType)
                assert isinstance(compare_object, Dict)
                for field in compare_object:
                    assert field in inspect(compare_object).attrs
                    assert compare_object[field] == getattr(object, field)

    # async def test_get_main_key(self, db: Session, main_key: str) -> None:
    #     object_dict, object_in, object_out = await self._create_object(self.db)

    #     object_map = {main_key: getattr(object_out, main_key)}
    #     stored_get_object = await self.crud_instance.get(db=self.db, filter=object_map)
    #     self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_get(self, db: Session, crud_instance: CRUDBase) -> None:
        object_dict, object_in, object_out = await self._create_object(db)
        # object_dict = self.object_generator_func()
        # object_in = self.schema(**object_dict)
        # object_out = await crud_instance.create(db=db, obj_in=object_in)

        object_map = {
            key.name: getattr(object_out, key.name)
            for key in inspect(object_out).primary_key
        }

        stored_get_object = await crud_instance.get(db=db, obj_in=object_map)

        self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_create(self, db: Session, crud_instance: CRUDBase) -> None:
        object_dict, object_in, object_out = await self._create_object(
            db, crud_instance
        )
        self._test_object(object_out, object_dict)

    # async def test_create_multiple(
    #     self,
    #     db: Session,
    #     count: int = 5,
    # ) -> None:
    #     initial_object_count = len(await self.crud_instance.get(self.db))
    #     object_dicts, object_ins, object_outs = await self._create_object(
    #         self.db, count
    #     )
    #     final_object_count = len(await self.crud_instance.get(self.db))

    #     assert final_object_count == initial_object_count + count
    #     self._test_object(object_outs, object_dicts)
