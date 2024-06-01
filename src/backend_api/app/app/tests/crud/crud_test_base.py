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
from app.tests.utils.utils import get_ignore_keys


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCRUD:
    async def _create_object(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
    ) -> Tuple[Dict, ModelType]:
        """
        A private method used to create objects
        """
        object_dict, object_out = await object_generator_func(db)

        return object_dict, object_out

    async def _create_multiple_objects(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
        count: int,
    ) -> Tuple[Tuple[Dict], Tuple[ModelType]]:
        """
        A private method used to create multiple objects
        """
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
        """
        A method for comparing if to objects are the same

        Uses recursion

        `obj` is the object being evaluated
        `compare_obj` is the object that `obj` is being evaluated agains

        Goes through all the fields in `compare_obj`, which can
        be a dict or another model. Checks if `obj` contains the field,
        and then checks if the field contains the same value. In cases
        where the value of the field is a float, a relative tolerance of 1e-3
        is used.

        We also test that the objects are of the correct type. However,
        currently we only check if they are not lists or tuples. I could
        not find a way to test if an object is of the type ModelType.

        Some fields can be ignored.
        """
        assert obj

        if compare_obj is not None:
            if isinstance(obj, (List, Tuple)) and isinstance(
                compare_obj, (List, Tuple)
            ):
                for obj, compare_obj in zip(obj, compare_obj):
                    self._test_object(obj, compare_obj)

            else:
                # Checks type of objects
                assert not isinstance(obj, (List, Tuple))
                assert not isinstance(compare_obj, (List, Tuple))
                # Different ways to extract fields depending on input type
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

    def _create_primary_key_map(self, obj: ModelType) -> Dict[str, Any]:
        """
        The CRUD get method uses filters. We can send in a map of primary keys to
        get the object we are looking for
        """
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
        """
        A test function.

        1. Tests if the initially created objects are valid.
        2. Creates a filter map using primary keys
        3. Uses the get method to retrieve whats in the db
        4. Checks the retrieved object agains the initial
        """
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
        """
        A test function.

        1. Uses the create method to create the objects.
        2. Tests if the initially created objects are valid.
        """
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
        """
        A test function.

        1. Counts how many objects are currently in the db.
        2. Uses the create method to create multiple objects.
        3. Tests if the initially created objects are valid.
        4. Counts how many objects are in the db after new objects are created.
        5. Checks that the specified amount of objects have been created.
        """
        initial_object_count = len(await crud_instance.get(db))

        multiple_object_dict, multiple_object_out = await self._create_multiple_objects(
            db, object_generator_func, count=count
        )
        self._test_object(multiple_object_out, multiple_object_dict)

        final_object_count = len(await crud_instance.get(db))

        assert final_object_count == initial_object_count + count

    @pytest.mark.asyncio
    async def test_delete(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], Tuple[Dict, ModelType]],
    ) -> None:
        """
        A test function.

        1. Uses the create method to create the objects.
        2. Tests if the initially created objects are valid.
        3. Creates a filter map using primary keys
        4. Deletes the object that matches the filter
        5. Tests that the deleted object is the same as the initial.
        """
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
        """
        A test function.

        1. Uses the create method to create the objects.
        2. Tests if the initially created objects are valid.
        3. Uses the create method to create an example of a new valid object.
        4. Removes the bi-product of creating an example of a valid object.
        5. Checks that the deleted object matches the temporary object.
        6. Creates an ignore list, which contains the fields which are created
        by the db on creation.
        7. Updates the values of the initial object.
        8. Tests if the returned updated object has been updated.
        """
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

        ignore = get_ignore_keys(object_dict, updated_object_dict)

        updated_object = await crud_instance.update(
            db, db_obj=object_out, obj_in=updated_object_dict
        )
        assert updated_object
        self._test_object(updated_object, updated_object_dict, ignore=ignore)
