from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.api.api_routes_test_base import TestAPI
from app.tests.crud.cascade_tests import TestCascade as UtilTestCascade
from app.crud.base import ModelType
from app.tests.utils.utils import create_primary_key_map, random_based_on_type


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCascadeAPI(TestAPI):
    @pytest.mark.asyncio
    async def test_cascade_delete(
        self,
        db: Session,
        object_generator_func_w_deps: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        client: TestClient,
        route_name: str,
        unique_identifier: str,
        ignore_test_columns: List[str],
        superuser_headers: Dict,
        api_deps_instances: List[List[str]],
    ) -> None:
        """Test cascade delete function for the API.

        1. Creates the object
        2. Uses the object to determine which tables are restricted
        3. Counts how many dependencies there are
        4. Loops through all dependencies, ignoring restricted tables
        5. Deletes a dependency
        6. Checks if a query for the dependent results in a specified HTTPException

        Args:
            db (Session): DB session

            object_generator_func_w_deps
            (Tuple[ Dict, ModelType, Optional[List[Union[Dict, ModelType]]] ]):
            Object generator function with dependencies

            client (TestClient): FastAPI test client
            route_name (str): Route name
            unique_identifier (str): Unique identifier for the object
            ignore_test_columns (List[str]): Columns to ignore
            superuser_headers (Dict): Superuser headers
            api_deps_instances (List[List[str]]): API dependencies instances
        """
        _, object_out, deps = await self._create_object_cascade_crud(
            db,
            object_generator_func_w_deps,
            retrieve_dependencies=True,
        )

        # We cannot rely on errors to tell us if a table has restricted deletes,
        # this is because the item is already deleted by the time we are notified
        # that it was not allowed.
        restricted_tables = self._find_restricted_delete(
            object_out, deps
        )

        # Number of dependencies is half the length of deps list (since it is a list of pairs)
        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, deps = await self._create_object_cascade_crud(
                db,
                object_generator_func_w_deps,
                retrieve_dependencies=True,
            )  # New objects have to be created for every test, since they are constantly being deleted
            self._test_object(object_out, object_dict)

            obj_out_pk_map = create_primary_key_map(object_out)

            response_get_before_deletion = client.get(
                f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
                auth=superuser_headers,
            )
            content_before_deletion = response_get_before_deletion.json()
            assert response_get_before_deletion.status_code == 200
            self._test_object(
                object_out,
                content_before_deletion,
                ignore=ignore_test_columns,
            )

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]
            self._test_object(dep_model, dep_dict)

            if dep_model.__tablename__ in restricted_tables:
                continue

            # Get key name of dict api_deps_instances[i]
            dep_route_name = api_deps_instances[i][0]
            dep_unique_identifier = api_deps_instances[i][1]

            if dep_unique_identifier not in dep_dict:
                continue

            response_delete_dep = client.delete(
                f"{settings.API_V1_STR}/{dep_route_name}/{dep_dict[dep_unique_identifier]}",
                auth=superuser_headers,
            )
            content_dep = response_delete_dep.json()
            primary_keys_map = create_primary_key_map(dep_model)
            assert (
                content_dep
                == f"{dep_route_name} with mapping ({dep_unique_identifier}: {primary_keys_map[dep_unique_identifier]}) deleted successfully"
            )

            assert response_delete_dep.status_code == 200

            response_get_after_deletion = client.get(
                f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
                auth=superuser_headers,
            )
            assert response_get_after_deletion.status_code == 404

    @pytest.mark.asyncio
    async def test_cascade_update(
        self,
        db: Session,
        object_generator_func_w_deps: Tuple[
            Dict, ModelType, Optional[List[Union[Dict, ModelType]]]
        ],
        client: TestClient,
        route_name: str,
        unique_identifier: str,
        update_request_params_deps: List[str],
        ignore_test_columns: List[str],
        superuser_headers: Dict,
        api_deps_instances: List[List[str]],
    ) -> None:
        """Test cascade update function for the API.

        1. Creates the object
        2. Uses the object to determine which tables cascade
        3. Counts how many dependencies there are
        4. Loops through all dependencies, ignoring non cascading tables
        5. Updates a dependency
        6. Checks if the update affects the dependent

        Args:
            db (Session): DB session

            object_generator_func_w_deps
            (Tuple[ Dict, ModelType, Optional[List[Union[Dict, ModelType]]] ]):
            Object generator function with dependencies

            client (TestClient): FastAPI test client
            route_name (str): Route name
            unique_identifier (str): Unique identifier for the object

            update_request_params_deps (List[str]): List of dependencies that require
            parameters for PUT

            ignore_test_columns (List[str]): Columns to ignore
            superuser_headers (Dict): Superuser headers
            api_deps_instances (List[List[str]]): API dependencies instances
        """
        _, object_out, deps = await self._create_object_cascade_crud(
            db,
            object_generator_func_w_deps,
            retrieve_dependencies=True,
        )

        cascading_tables = self._find_cascading_update(
            object_out, deps
        )

        n_deps = len(deps) // 2
        for i in range(n_deps):
            object_dict, object_out, deps = await self._create_object_cascade_crud(
                db,
                object_generator_func_w_deps,
                retrieve_dependencies=True,
            )  # New objects have to be created for every test, since they are constantly being deleted
            self._test_object(object_out, object_dict)
            obj_out_pk_map = create_primary_key_map(
                object_out
            )  # Needs to be a global utility function

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]

            self._test_object(dep_model, dep_dict)
            if dep_model.__tablename__ not in cascading_tables:
                continue

            cascading_tables_keys = cascading_tables[dep_model.__tablename__]
            new_dep_dict = deepcopy(dep_dict)

            for key in cascading_tables_keys:
                if key not in object_dict or key not in dep_dict:
                    continue
                new_key_value = random_based_on_type(dep_dict[key])
                new_dep_dict[key] = new_key_value

                if key in obj_out_pk_map:
                    obj_out_pk_map[key] = new_key_value

                assert object_dict[key] != new_dep_dict[key]

            dep_route_name = api_deps_instances[i][0]
            dep_unique_identifier = api_deps_instances[i][1]

            dep_obj_out_pk_map = create_primary_key_map(dep_model)

            if dep_route_name in update_request_params_deps:
                response_update_dep = client.put(
                    f"{settings.API_V1_STR}/{dep_route_name}/",
                    auth=superuser_headers,
                    json=new_dep_dict,
                    params=dep_obj_out_pk_map,
                )
            else:
                response_update_dep = client.put(
                    f"{settings.API_V1_STR}/{dep_route_name}/{dep_obj_out_pk_map[dep_unique_identifier]}",
                    auth=superuser_headers,
                    json=new_dep_dict,
                )

            updated_dep_model_content = response_update_dep.json()

            assert response_update_dep.status_code == 200
            self._compare_dicts(
                updated_dep_model_content,
                new_dep_dict,
                ignore=ignore_test_columns,
            )

            # Get the original model
            response_get_model = client.get(
                f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
                auth=superuser_headers,
            )
            assert response_get_model.status_code == 200

            get_model_content = response_get_model.json()
            for key in cascading_tables_keys:
                if key not in object_dict or key not in updated_dep_model_content:
                    continue
                assert get_model_content[key] == updated_dep_model_content[key]
