import asyncio
import pytest
from typing import Any, Dict, List, Optional, Union, Callable, Tuple

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.base import (
    CRUDBase,
    ModelType,
)

from app.tests.crud.crud_test_base import TestCRUD
from app.core.models.database import insp


class TestCascade(TestCRUD):
    async def _create_object(
        self,
        db,
        object_generator_func: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        retrieve_dependencies: Optional[bool] = False,
    ) -> Tuple[Dict, ModelType, Optional[List[Union[Dict, ModelType]]]]:
        if retrieve_dependencies:
            object_dict, object_out, deps = await object_generator_func(db)

            return object_dict, object_out, deps

        else:
            object_dict, object_out = await object_generator_func(db)

            return object_dict, object_out

    def _find_restrictions(self, model, deps):
        foreign_keys = insp.get_foreign_keys(model.__tablename__)
        restricted_tables = []
        for key in foreign_keys:
            if key["options"]["ondelete"] == "RESTRICT":
                restricted_tables.append(key["referred_table"])

        # Does the same for every dependency
        for dep in deps[
            1::2
        ]:  # every other element is a model, starting from the 2nd element
            foreign_keys = insp.get_foreign_keys(dep.__tablename__)
            for key in foreign_keys:
                if key["options"]["ondelete"] == "RESTRICT":
                    restricted_tables.append(key["referred_table"])

        return restricted_tables

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
        _, obj, deps = await self._create_object(
            db, object_generator_func_w_deps, retrieve_dependencies=True
        )

        restricted_tables = self._find_restrictions(obj, deps)

        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, deps = await self._create_object(
                db, object_generator_func_w_deps, retrieve_dependencies=True
            )
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
