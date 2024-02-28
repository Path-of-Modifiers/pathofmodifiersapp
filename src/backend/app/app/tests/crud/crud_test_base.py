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

    async def _create_multiple_objects(
        self,
        db,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
        count: int,
    ) -> Tuple[Tuple[Dict], Tuple[ModelType]]:
        multiple_object_dict, multiple_object_out = zip(
            *await asyncio.gather(
                *(self._create_object(db, object_generator_func) for _ in range(count))
            )
        )  # Create multiple objects
        return multiple_object_dict, multiple_object_out

    def _test_object(
        self,
        obj: Union[ModelType, List[ModelType]],
        compare_obj: Optional[
            Union[Dict, List[Dict], ModelType, List[ModelType]]
        ] = None,
        ignore: Optional[List[str]] = [],
    ) -> None:
        assert obj

        if compare_obj is not None:
            if isinstance(obj, (List, Tuple)) and isinstance(
                compare_obj, (List, Tuple)
            ):
                for obj, compare_obj in zip(obj, compare_obj):
                    self._test_object(obj, compare_obj)

            else:
                assert not isinstance(obj, (List, Tuple))
                assert not isinstance(compare_obj, (List, Tuple))
                if isinstance(compare_obj, Dict):
                    extract_value = lambda obj, key: obj[key]
                    extract_fields = lambda obj: obj
                else:
                    extract_value = lambda obj, field: getattr(obj, field)
                    extract_fields = lambda obj: obj.__table__.columns.keys()
                for field in extract_fields(compare_obj):
                    # print(f"\n{field}")
                    assert field in inspect(obj).attrs
                    if field not in ignore:
                        if isinstance(extract_value(compare_obj, field), float):
                            assert math.isclose(
                                extract_value(compare_obj, field),
                                getattr(obj, field),
                                rel_tol=1e-3,
                            )
                        else:
                            # print(
                            #     f"{extract_value(compare_obj, field)} == {getattr(obj, field)}"
                            # )
                            assert extract_value(compare_obj, field) == getattr(
                                obj, field
                            )

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
        self._test_object(object_out, object_dict)

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

        multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
            db, object_generator_func, count=count
        )

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

        object_map = self._create_primary_key_map(object_out)
        deleted_object = await crud_instance.remove(db=db, filter=object_map)
        assert deleted_object
        self._test_object(deleted_object, object_out)

    @pytest.mark.asyncio
    async def test_update(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        object_dict, object_out = await self._create_object(db, object_generator_func)
        self._test_object(object_out, object_dict)

        updated_object_dict, temp_object_out = await self._create_object(
            db, object_generator_func
        )  # Creates a second template
        self._test_object(temp_object_out, updated_object_dict)

        object_map = self._create_primary_key_map(temp_object_out)
        deleted_object = await crud_instance.remove(
            db=db, filter=object_map
        )  # Delete the template from the db
        assert deleted_object
        self._test_object(deleted_object, temp_object_out)

        ignore = [
            key
            for key in object_out.__table__.columns.keys()
            if key not in updated_object_dict
        ]

        updated_object = await crud_instance.update(
            db, db_obj=object_out, obj_in=updated_object_dict
        )
        assert updated_object
        self._test_object(updated_object, object_out, ignore=ignore)
