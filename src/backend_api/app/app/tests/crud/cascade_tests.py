import asyncio
import pytest
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from copy import deepcopy

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.base import (
    CRUDBase,
    ModelType,
)

from app.tests.crud.crud_test_base import TestCRUD
from app.core.models.database import insp
from app.tests.utils.utils import random_based_on_type


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCascade(TestCRUD):
    async def _create_object_cascade(
        self,
        db: Session,
        object_generator_func: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        retrieve_dependencies: Optional[bool] = False,
    ) -> Tuple[Dict, ModelType, Optional[List[Union[Dict, ModelType]]]]:
        """A private method used to create objects, with option to retrieve dependencies

        Args:
            db (Session): Database session
            object_generator_func (Tuple[ Dict, ModelType, Optional[List[Union[Dict, ModelType]]] ]): A tuple containing the object dictionary, the object model and optionally a list of dependencies
            retrieve_dependencies (Optional[bool], optional): Optional whether to retrieve dependencies. Defaults to False.

        Returns:
            Tuple[Dict, ModelType, Optional[List[Union[Dict, ModelType]]]]: A tuple containing the object dictionary, the object model and optionally a list of dependencies
        """
        if retrieve_dependencies:
            object_dict, object_out, deps = await object_generator_func(db)

            return object_dict, object_out, deps

        else:
            object_dict, object_out = await object_generator_func(db)

            return object_dict, object_out

    def _get_foreign_keys(self, model: ModelType) -> List[Dict]:
        """
        Uses a database inspector to learn more about the foreign keys related to the given model.
        The returned object is a list of dictionaries, where each element represents a relation to
        another table. One related table may have multiple foreign keys.
        """
        foreign_keys = insp.get_foreign_keys(model.__tablename__)
        return foreign_keys

    def _find_restricted_delete(
        self, model: ModelType, deps: List[Union[Dict, ModelType]]
    ) -> List[str]:
        """
        Retrieves all tables related to model, which are not allowed to be deleted
        """
        foreign_keys = self._get_foreign_keys(model)
        restricted_tables = []
        for key in foreign_keys:
            if key["options"]["ondelete"] == "RESTRICT":
                restricted_tables.append(key["referred_table"])

        # Does the same for every dependency
        for dep in deps[
            1::2
        ]:  # every other element is a model, starting from the 2nd element
            foreign_keys = self._get_foreign_keys(dep)
            for key in foreign_keys:
                if key["options"]["ondelete"] == "RESTRICT":
                    restricted_tables.append(key["referred_table"])

        return restricted_tables

    def _find_cascading_update(
        self, model: ModelType, deps: List[Union[Dict, ModelType]]
    ) -> Dict[str, str]:
        """
        Retrieves all tables related to model, which delete all dependent entries
        """
        foreign_keys = self._get_foreign_keys(model)
        cascading_tables = {}
        for key in foreign_keys:
            if "onupdate" in key["options"]:
                if key["options"]["onupdate"] == "CASCADE":
                    cascading_tables[key["referred_table"]] = key["referred_columns"]

        # Does the same for every dependency
        for dep in deps[
            1::2
        ]:  # every other element is a model, starting from the 2nd element
            foreign_keys = self._get_foreign_keys(dep)
            for key in foreign_keys:
                if "onupdate" in key["options"]:
                    if key["options"]["onupdate"] == "CASCADE":
                        cascading_tables[key["referred_table"]] = key[
                            "referred_columns"
                        ]

        return cascading_tables

    @pytest.mark.asyncio
    async def test_cascade_delete(
        self,
        db: Session,
        crud_instance: CRUDBase,
        crud_deps_instances: List[CRUDBase],
        object_generator_func_w_deps: Callable[
            [], Tuple[Dict, ModelType, List[Union[Dict, ModelType]]]
        ],
    ) -> None:
        """
        A test function.

        1. Creates the object
        2. Uses the object to determine which tables are restricted
        3. Counts how many dependencies there are
        4. Loops through all dependencies, ignoring restricted tables
        5. Deletes a dependency
        6. Checks if a query for the dependent results in a specified HTTPException
        """
        _, obj, deps = await self._create_object_cascade(
            db, object_generator_func_w_deps, retrieve_dependencies=True
        )

        # We cannot rely on errors to tell us if a table has restricted deletes,
        # this is because the item is already deleted by the time we are notified
        # that it was not allowed.
        restricted_tables = self._find_restricted_delete(obj, deps)

        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, deps = await self._create_object_cascade(
                db, object_generator_func_w_deps, retrieve_dependencies=True
            )  # New objects have to be created for every test, since they are constantly being deleted
            self._test_object(object_out, object_dict)
            obj_map = self._create_primary_key_map(object_out)

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]
            self._test_object(dep_model, dep_dict)

            if dep_model.__tablename__ in restricted_tables:
                continue

            dep_map = self._create_primary_key_map(dep_model)
            deleted_dep_model = await crud_deps_instances[i].remove(
                db=db, filter=dep_map
            )

            assert deleted_dep_model
            self._test_object(deleted_dep_model, dep_model)

            with pytest.raises(HTTPException) as excinfo:
                await crud_instance.remove(db, filter=obj_map)
            assert excinfo.value.status_code == 404

    @pytest.mark.asyncio
    async def test_cascade_update(
        self,
        db: Session,
        crud_instance: CRUDBase,
        crud_deps_instances: List[CRUDBase],
        object_generator_func_w_deps: Callable[
            [], Tuple[Dict, ModelType, List[Union[Dict, ModelType]]]
        ],
    ) -> None:
        """
        A test function.

        1. Creates the object
        2. Uses the object to determine which tables cascade
        3. Counts how many dependncies there are
        4. Loops through all dependencies, ignoring non cascading tables
        5. Updates a dependency
        6. Checks if the update affects the dependent
        """
        _, obj, deps = await self._create_object_cascade(
            db, object_generator_func_w_deps, retrieve_dependencies=True
        )

        cascading_tables = self._find_cascading_update(obj, deps)
        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, deps = await self._create_object_cascade(
                db, object_generator_func_w_deps, retrieve_dependencies=True
            )
            self._test_object(object_out, object_dict)
            obj_map = self._create_primary_key_map(object_out)

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]
            self._test_object(dep_model, dep_dict)
            if dep_model.__tablename__ not in cascading_tables:
                continue

            keys = cascading_tables[dep_model.__tablename__]
            new_dep_dict = deepcopy(dep_dict)
            for key in keys:
                if key not in object_dict or key not in dep_dict:
                    continue
                new_key_value = random_based_on_type(dep_dict[key])
                new_dep_dict[key] = new_key_value
                object_dict[key] = new_key_value
                if key in obj_map:
                    obj_map[key] = new_key_value

            updated_dep_model = await crud_deps_instances[i].update(
                db, db_obj=dep_model, obj_in=new_dep_dict
            )
            self._test_object(updated_dep_model, new_dep_dict)

            new_updated_object = await crud_instance.get(db, filter=obj_map)

            self._test_object(new_updated_object, object_dict)
