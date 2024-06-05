from copy import deepcopy
from typing import Callable, Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.api.api_test_base import TestAPI
from app.tests.crud.cascade_tests import TestCascade as UtilTestCascade
from app.crud.base import CRUDBase, ModelType
from app.tests.utils.utils import get_ignore_keys, random_based_on_type


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCascadeAPI(TestAPI):
    async def _create_object_cascade(
        self,
        db: pytest.Session,
        object_generator_func: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        get_crud_test_cascade_model: UtilTestCascade,
        retrieve_dependencies: Optional[bool] = False,
    ) -> Tuple[Dict, ModelType, Dict, Optional[List[Union[Dict, ModelType]]]]:
        """A private method used to create objects, with the option to retrieve dependencies.

        Args:
            db (pytest.Session): DB session
            object_generator_func (Tuple[ Dict, ModelType, Optional[List[Union[Dict, ModelType]]] ]):
            Object generator function

            retrieve_dependencies (Optional[bool], optional): Whether to retrieve dependencies.
            Defaults to False.

        Returns:
            Tuple[Dict, ModelType, Optional[List[Union[Dict, ModelType]]]]:

            Object dictionary, object instance, object_out_dict and dependencies
        """
        if retrieve_dependencies:
            object_dict, object_out, deps = (
                await get_crud_test_cascade_model._create_object_cascade(
                    db, object_generator_func, retrieve_dependencies=True
                )
            )
            object_out_dict = self._db_obj_to_dict(object_out)
            return object_dict, object_out, object_out_dict, deps
        else:
            object_dict, object_out = (
                await get_crud_test_cascade_model._create_object_cascade(
                    db, object_generator_func
                )
            )
            object_out_dict = self._db_obj_to_dict(object_out)
            return object_dict, object_out, object_out_dict

    def _get_foreign_keys(
        self, model: ModelType, get_crud_test_cascade_model: UtilTestCascade
    ) -> List[Dict]:
        """
        Uses a database inspector to learn more about the foreign keys related to the given model.
        The returned object is a list of dictionaries, where each element represents a relation to
        another table. One related table may have multiple foreign keys.
        """
        return get_crud_test_cascade_model._get_foreign_keys(model)

    def _find_restricted_delete(
        self,
        model: ModelType,
        deps: List[Union[Dict, ModelType]],
        get_crud_test_cascade_model: UtilTestCascade,
    ) -> List[str]:
        """
        Retrieves all tables related to model, which are not allowed to be deleted
        """
        return get_crud_test_cascade_model._find_restricted_delete(model, deps)

    def _find_cascading_update(
        self,
        model: ModelType,
        deps: List[Union[Dict, ModelType]],
        get_crud_test_cascade_model: UtilTestCascade,
    ) -> Dict[str, str]:
        """
        Retrieves all tables related to model, which delete all dependent entries
        """
        return get_crud_test_cascade_model._find_cascading_update(model, deps)

    @pytest.mark.asyncio
    async def test_cascade_delete(
        self,
        db: pytest.Session,
        object_generator_func_w_deps: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        client: TestClient,
        route_name: str,
        unique_identifier: str,
        get_crud_test_cascade_model: UtilTestCascade,
        ignore_test_columns: List[str],
        superuser_headers: Dict,
        api_deps_instances: List[List[str]],
    ) -> None:
        """
        A method for testing cascade delete
        """

        _, obj, _, deps = await self._create_object_cascade(
            db,
            object_generator_func_w_deps,
            get_crud_test_cascade_model,
            retrieve_dependencies=True,
        )

        # We cannot rely on errors to tell us if a table has restricted deletes,
        # this is because the item is already deleted by the time we are notified
        # that it was not allowed.
        restricted_tables = self._find_restricted_delete(
            obj, deps, get_crud_test_cascade_model
        )

        print("TOYOTA", deps)

        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, object_out_dict, deps = (
                await self._create_object_cascade(
                    db,
                    object_generator_func_w_deps,
                    get_crud_test_cascade_model,
                    retrieve_dependencies=True,
                )
            )  # New objects have to be created for every test, since they are constantly being deleted
            self._test_object(get_crud_test_cascade_model, object_out, object_dict)

            response_get_before_deletion = client.get(
                f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
                auth=superuser_headers,
            )
            content_before_deletion = response_get_before_deletion.json()
            assert response_get_before_deletion.status_code == 200
            self._test_object(
                get_crud_test_cascade_model,
                object_out,
                content_before_deletion,
                ignore=ignore_test_columns,
            )

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]
            self._test_object(get_crud_test_cascade_model, dep_model, dep_dict)

            if dep_model.__tablename__ in restricted_tables:
                continue

            # Get key name of dict api_deps_instances[i]
            print("YIDA", api_deps_instances, i)
            dep_route_name = api_deps_instances[i][0]
            print("DEP_ROUTE_NAME", dep_route_name)
            print("DEP_VADERFADERDICT", dep_dict)
            print("DEP_VADERFADERMODEL", dep_model)
            dep_unique_identifier = api_deps_instances[i][1]
            if dep_unique_identifier not in dep_dict:
                continue

            response_delete_dep = client.delete(
                f"{settings.API_V1_STR}/{dep_route_name}/{dep_dict[dep_unique_identifier]}",
                auth=superuser_headers,
            )
            content_dep = response_delete_dep.json()
            primary_keys_map = self._create_primary_key_map(
                dep_model, get_crud_test_cascade_model
            )
            print("HULALANDET", content_dep, "\n")
            print(
                "BUAAA",
                f"{dep_route_name} with mapping ({dep_unique_identifier}: {primary_keys_map[dep_unique_identifier]}) deleted successfully",
            )
            assert (
                content_dep
                == f"{dep_route_name} with mapping ({dep_unique_identifier}: {primary_keys_map[dep_unique_identifier]}) deleted successfully"
            )

            print("HULALANDET", content_dep, "\n")
            # print(
            #     "BUAAA",
            #     f"{dep_route_name} with mapping ({{'{dep_unique_identifier}': '{object_out_dict[dep_unique_identifier]}'}}) deleted successfully",
            # )

            assert response_delete_dep.status_code == 200

            response_get_after_deletion = client.get(
                f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
                auth=superuser_headers,
            )
            print("HAGLEBU", response_get_after_deletion)
            assert response_get_after_deletion.status_code == 404

    @pytest.mark.asyncio
    async def test_cascade_update(
        self,
        db: pytest.Session,
        object_generator_func_w_deps: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        client: TestClient,
        route_name: str,
        unique_identifier: str,
        get_crud_test_cascade_model: UtilTestCascade,
        special_update_params_deps: List[str],
        ignore_test_columns: List[str],
        superuser_headers: Dict,
        api_deps_instances: List[List[str]],
    ) -> None:
        """
        A test function.

        1. Creates the object
        2. Uses the object to determine which tables cascade
        3. Counts how many dependencies there are
        4. Loops through all dependencies, ignoring non cascading tables
        5. Updates a dependency
        6. Checks if the update affects the dependent
        """
        _, obj, _, deps = await self._create_object_cascade(
            db,
            object_generator_func_w_deps,
            get_crud_test_cascade_model,
            retrieve_dependencies=True,
        )

        cascading_tables = self._find_cascading_update(
            obj, deps, get_crud_test_cascade_model
        )

        n_deps = len(deps) // 2
        for i in range(n_deps):
            # object_dict, object_out, _, deps = await self._create_object_cascade(
            #     db,
            #     object_generator_func_w_deps,
            #     get_crud_test_cascade_model,
            #     retrieve_dependencies=True,
            # )
            object_dict, object_out, object_out_dict, deps = (
                await self._create_object_cascade(
                    db,
                    object_generator_func_w_deps,
                    get_crud_test_cascade_model,
                    retrieve_dependencies=True,
                )
            )  # New objects have to be created for every test, since they are constantly being deleted
            self._test_object(get_crud_test_cascade_model, object_out, object_dict)
            obj_map = self._create_primary_key_map(
                object_out, get_crud_test_cascade_model
            )  # Needs to be a global utility function

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]

            self._test_object(get_crud_test_cascade_model, dep_model, dep_dict)
            if dep_model.__tablename__ not in cascading_tables:
                continue

            cascading_tables_keys = cascading_tables[dep_model.__tablename__]
            new_dep_dict = deepcopy(dep_dict)

            for key in cascading_tables_keys:
                if key not in object_dict or key not in dep_dict:
                    continue
                new_key_value = random_based_on_type(dep_dict[key])
                new_dep_dict[key] = new_key_value

                if key in obj_map:
                    obj_map[key] = new_key_value

                assert object_dict[key] != new_dep_dict[key]

            # updated_dep_model = await crud_deps_instances[i].update(
            #     db, db_obj=dep_model, obj_in=new_dep_dict
            # )
            dep_route_name = api_deps_instances[i][0]
            dep_unique_identifier = api_deps_instances[i][1]
            # print(
            #     "ABOBA",
            #     dep_route_name,
            #     dep_unique_identifier,
            #     "!!!",
            #     new_dep_dict[dep_unique_identifier],
            # )

            # Update the dependency

            # response_update_dep = client.put(
            #     f"{settings.API_V1_STR}/{dep_route_name}/{dep_dict[dep_unique_identifier]}",
            #     auth=superuser_headers,
            #     json=new_dep_dict,
            # )
            primary_keys_map_object_out = self._create_primary_key_map(
                dep_model, get_crud_test_cascade_model
            )
            print(
                "HAGGLEBU",
                dep_route_name,
                dep_unique_identifier,
                new_dep_dict,
                dep_dict,
            )

            print("HULAHULA", primary_keys_map_object_out)
            if dep_route_name in special_update_params_deps:
                print("KRAQQEDUPDATEINSTANCE")

                response_update_dep = client.put(
                    f"{settings.API_V1_STR}/{dep_route_name}/",
                    auth=superuser_headers,
                    json=new_dep_dict,
                    params=primary_keys_map_object_out,
                )
            else:
                response_update_dep = client.put(
                    f"{settings.API_V1_STR}/{dep_route_name}/{primary_keys_map_object_out[dep_unique_identifier]}",
                    auth=superuser_headers,
                    json=new_dep_dict,
                )

            updated_dep_model_content = response_update_dep.json()
            print("UPDATED_DEP_MODEL_DARK_VADER", updated_dep_model_content)
            print("RESPONSEVADER_STATUS", response_update_dep.status_code)
            assert response_update_dep.status_code == 200
            self._compare_dicts(
                updated_dep_model_content,
                new_dep_dict,
                ignore=ignore_test_columns,
            )

            print("GRAVERN", updated_dep_model_content)
            print("SJUKERN", object_dict)

            # Get the original model
            response_get_model = client.get(
                f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
                auth=superuser_headers,
            )
            assert response_get_model.status_code == 200

            get_model_content = response_get_model.json()
            for key in cascading_tables_keys:
                if key not in object_dict or key not in updated_dep_model_content:
                    continue
                assert get_model_content[key] == updated_dep_model_content[key]
