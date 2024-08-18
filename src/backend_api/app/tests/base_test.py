import asyncio
import math
from collections.abc import Callable
from typing import Any

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app.core.models.database import insp
from app.crud.base import (
    ModelType,
)
from app.tests.utils.utils import get_extract_functions


class BaseTest:
    def extract_value_key(self, dict: dict) -> Any:
        # Example: Dynamically choose a key (e.g., the first key in the dictionary)
        key = next(
            iter(dict), None
        )  # Get the first key, or None if the dictionary is empty
        return dict[key] if key else None

    def _f_ext_value_attr(self, obj: ModelType) -> Any:
        fields = self._f_ext_fields(obj)
        return [getattr(obj, f) for f in fields]

    def _f_ext_fields(self, obj: ModelType) -> list[str]:
        return obj.__table__.columns.keys()

    async def _create_object_crud(
        self,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]] | Any,
    ) -> tuple[dict, ModelType]:
        """
        A private method used to create objects
        """
        object_dict, object_out = await object_generator_func(db)

        return object_dict, object_out

    async def _create_multiple_objects_crud(
        self,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]] | Any,
        count: int,
    ) -> tuple[tuple[dict], tuple[ModelType]]:
        """
        A private method used to create multiple objects
        """
        multiple_object_dict, multiple_object_out = zip(
            *await asyncio.gather(
                *(
                    self._create_object_crud(db, object_generator_func)
                    for _ in range(count)
                )
            ),
            strict=False,
        )  # Create multiple objects
        return multiple_object_dict, multiple_object_out

    def _test_object(
        self,
        obj: ModelType | list[ModelType],
        compare_obj: dict | list[dict] | ModelType | list[ModelType] | None = None,
        ignore: list[str] | None = None,
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
        if ignore is None:
            ignore = []
        if compare_obj is not None:
            if isinstance(obj, (list | tuple)) and isinstance(
                compare_obj, (list | tuple)
            ):
                for obj_model, compare_obj_model in zip(obj, compare_obj, strict=False):
                    self._test_object(obj_model, compare_obj_model)

            else:
                # Checks type of objects
                assert not isinstance(obj, (list | tuple))
                assert not isinstance(compare_obj, (list | tuple))
                # Different ways to extract fields depending on input type

                extract_value, extract_fields = get_extract_functions(compare_obj)

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

    async def _create_object_cascade_crud(
        self,
        db: Session,
        object_generator_func: tuple[dict, ModelType, list[dict | ModelType] | None],
        retrieve_dependencies: bool | None = False,
    ) -> tuple[dict, ModelType, list[dict | ModelType] | None]:
        """A private method used to create objects, with option to retrieve dependencies

        Args:
            db (Session): Database session
            object_generator_func (tuple[ dict, ModelType, list[dict | ModelType]]]): A tuple containing the object dictionary, the object model and optionally a list of dependencies
            retrieve_dependencies (bool, optional): whether to retrieve dependencies. Defaults to False.

        Returns:
            tuple[dict, ModelType, list[dict | ModelType]]]: A tuple containing the object dictionary, the object model and optionally a list of dependencies
        """
        if retrieve_dependencies:
            object_dict, object_out, deps = await object_generator_func(db)

            return object_dict, object_out, deps

        else:
            object_dict, object_out = await object_generator_func(db)

            return object_dict, object_out

    def _get_foreign_keys(self, model: ModelType) -> list[dict]:
        """
        Uses a database inspector to learn more about the foreign keys related to the given model.
        The returned object is a list of dictionaries, where each element represents a relation to
        another table. One related table may have multiple foreign keys.
        """
        foreign_keys = insp.get_foreign_keys(model.__tablename__)
        return foreign_keys

    def _find_restricted_delete(
        self, model: ModelType, deps: list[dict | ModelType]
    ) -> list[str]:
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
        self, model: ModelType, deps: list[dict | ModelType]
    ) -> dict[str, str]:
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

    def _create_primary_key_map(self, obj: ModelType) -> dict[str, Any]:
        """
        The CRUD get method uses filters. We can send in a map of primary keys to
        get the object we are looking for
        """
        object_map = {
            key.name: getattr(obj, key.name) for key in obj.__table__.primary_key
        }
        return object_map
