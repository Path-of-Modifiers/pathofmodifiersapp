from typing import Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from typing import Dict, List, Optional, Tuple, Union

from app.core.config import settings
from app.tests.api.api_test_base import TestAPI
from app.tests.crud.cascade_tests import TestCascade as UtilTestCascade
from app.crud.base import CRUDBase, ModelType


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
    ) -> Tuple[Dict, ModelType, Optional[List[Union[Dict, ModelType]]]]:
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
    ) -> List[str]:
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
        superuser_headers: Dict,
        api_deps_instances: List[Dict],
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

            dep_dict, dep_model = deps[2 * i], deps[2 * i + 1]
            self._test_object(get_crud_test_cascade_model, dep_model, dep_dict)

            if dep_model.__tablename__ in restricted_tables:
                continue

            # Get key name of dict api_deps_instances[i]
            print("YIDA", api_deps_instances, i)
            dep_route_name = list(api_deps_instances[i].keys())[0]
            print("DEP_ROUTE_NAME", dep_route_name)
            dep_unique_identifier = api_deps_instances[i].get(dep_route_name)

            response_dep = client.delete(
                f"{settings.API_V1_STR}/{dep_route_name}/{object_out_dict[dep_unique_identifier]}",
                auth=superuser_headers,
            )
            content_dep = response_dep.json()
            print("HULALANDET", content_dep, "\n")
            print(
                "BUAAA",
                f"{dep_route_name.capitalize()} with mapping ({{'{dep_unique_identifier}': '{object_out_dict[dep_unique_identifier]}'}}) deleted successfully",
            )
            assert (
                content_dep
                == f"{dep_route_name.capitalize()} with mapping ({{'{dep_unique_identifier}': '{object_out_dict[dep_unique_identifier]}'}}) deleted successfully"
            )

            assert response_dep.status_code == 200

            response = client.delete(
                f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
                auth=superuser_headers,
            )
            print("HAGLEBU", response)
            assert response.status_code == 404
