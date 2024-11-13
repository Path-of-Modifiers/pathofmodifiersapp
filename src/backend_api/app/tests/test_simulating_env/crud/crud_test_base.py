from collections.abc import Callable

import pytest
from sqlalchemy.orm import Session

from app.crud.base import (
    CRUDBase,
    ModelType,
)
from app.exceptions.model_exceptions.db_exception import (
    DbObjectAlreadyExistsError,
    DbObjectDoesNotExistError,
)
from app.tests.test_simulating_env.base_test import BaseTest
from app.tests.utils.utils import get_ignore_keys


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCRUD(BaseTest):
    @pytest.mark.asyncio
    async def test_get(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        is_hypertable: bool,
    ) -> None:
        """
        A test function.

        1. Tests if the initially created objects are valid.
        2. Creates a filter map using primary keys
        3. Uses the get method to retrieve whats in the db
        4. Checks the retrieved object agains the initial
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support single get operations")

        object_dict, object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(object_out, object_dict)

        object_map = self._create_primary_key_map(object_out)
        stored_get_object = await crud_instance.get(db=db, filter=object_map)

        self._test_object(stored_get_object, object_dict)

    @pytest.mark.asyncio
    async def test_create(
        self,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
    ) -> None:
        """
        A test function.

        1. Uses the create method to create the objects.
        2. Tests if the initially created objects are valid.
        """
        object_dict, object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(object_out, object_dict)

    @pytest.mark.asyncio
    async def test_create_multiple(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
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

        (
            multiple_object_dict,
            multiple_object_out,
        ) = await self._create_multiple_random_objects_crud(
            db, object_generator_func, count=count
        )
        self._test_object(multiple_object_out, multiple_object_dict)

        final_object_count = len(await crud_instance.get(db))

        assert final_object_count == initial_object_count + count

    @pytest.mark.asyncio
    async def test_create_duplicate_one_instance(
        self,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        crud_instance: CRUDBase,
        on_duplicate_params: tuple[bool, str | None],
    ) -> None:
        # TODO: currently always skips. Find out why test database doesn't register UNQIUE constraints
        pytest.skip(
            f"CRUD test for test_create_found_duplicate in crud {crud_instance.__class__.__name__} does not support ignore_duplicates"
        )

        object_dict, _ = await self._create_random_object_crud(
            db, object_generator_func
        )
        db_obj = await self._create_object_crud(
            db,
            crud_instance,
            object_dict,
            on_duplicate_params=on_duplicate_params,
        )
        assert db_obj is None

        with pytest.raises(DbObjectAlreadyExistsError):
            db_obj = await self._create_object_crud(
                db, crud_instance, object_dict, on_duplicate_params=on_duplicate_params
            )

    @pytest.mark.asyncio
    async def test_create_duplicate_multiple_instances(
        self,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        crud_instance: CRUDBase,
        on_duplicate_params: tuple[bool, str | None],
    ) -> None:
        # TODO: currently always skips. Find out why test database doesn't register UNQIUE constraints
        pytest.skip(
            f"CRUD test for test_create_found_duplicate in crud {crud_instance.__class__.__name__} does not support ignore_duplicates"
        )

        multiple_object_dict_tuple, _ = await self._create_multiple_random_objects_crud(
            db, object_generator_func, count=5
        )
        object_dict_list = list(multiple_object_dict_tuple)
        db_obj = await self._create_multiple_objects_crud(
            db,
            crud_instance=crud_instance,
            create_objects=object_dict_list,
            on_duplicate_params=on_duplicate_params,
        )
        assert db_obj is None

        with pytest.raises(DbObjectAlreadyExistsError):
            db_obj = await self._create_multiple_objects_crud(
                db,
                crud_instance,
                object_dict_list,
                on_duplicate_params=on_duplicate_params,
            )

    @pytest.mark.asyncio
    async def test_delete(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        is_hypertable: bool,
    ) -> None:
        """
        A test function.

        1. Uses the create method to create the objects.
        2. Tests if the initially created objects are valid.
        3. Creates a filter map using primary keys
        4. Deletes the object that matches the filter
        5. Tests that the deleted object is the same as the initial.
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support single get operations")

        object_dict, object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(object_out, object_dict)

        object_map = self._create_primary_key_map(object_out)
        deleted_object = await crud_instance.remove(
            db=db,
            filter=object_map,
        )
        assert deleted_object
        self._test_object(deleted_object, object_out)

    @pytest.mark.asyncio
    async def test_update(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        is_hypertable: bool,
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
        if is_hypertable:
            pytest.skip("Hypertables doesn't support single get operations")

        object_dict, object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(object_out, object_dict)

        updated_object_dict, temp_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )  # Creates a second template
        self._test_object(temp_object_out, updated_object_dict)

        object_map = self._create_primary_key_map(temp_object_out)
        deleted_object = await crud_instance.remove(
            db=db,
            filter=object_map,
        )  # Delete the template from the db
        assert deleted_object
        self._test_object(deleted_object, temp_object_out)

        ignore = get_ignore_keys(object_out, updated_object_dict)

        updated_object = await crud_instance.update(
            db, db_obj=object_out, obj_in=updated_object_dict
        )
        assert updated_object
        self._test_object(updated_object, updated_object_dict, ignore=ignore)

    @pytest.mark.asyncio
    async def test_update_not_exists(
        self,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        is_hypertable: bool,
    ) -> None:
        """
        A test function. Tests if updating an object that does not exist raises
        an error.
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support single get operations")

        object_dict, object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(object_out, object_dict)

        object_map = self._create_primary_key_map(object_out)

        await crud_instance.remove(db, filter=self._create_primary_key_map(object_out))

        with pytest.raises(DbObjectDoesNotExistError):
            await crud_instance.update(db, db_obj=object_out, obj_in=object_map)
