import math
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union
from fastapi import Response
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.crud.base import ModelType
from app.core.config import settings
from app.tests.utils.utils import is_courotine_function
from app.tests.base_test import BaseTest


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI(BaseTest):
    async def _create_object_api(
        self,
        db: Session,
        create_random_object_func: Union[
            Callable[[], Tuple[Dict, ModelType, Dict]], Any
        ],
        client: TestClient,
        route_name: str,
        superuser_headers: Dict[str, str],
    ) -> Tuple[Dict, Response]:
        """Create an object using the API

        Also tests correct response codes and if the object created is
        the same as the object returned by the API

        Args:
            db (Session): DB session

            create_random_object_func
            (Union[Callable[[], Tuple[Dict, ModelType, Dict]], Any]):
            Create random object function

            client (TestClient): FastAPI test client
            route_name (str): Route name
            superuser_headers (Dict[str, str]): Superuser headers

        Returns:
            Dict: Object dictionary created
            Response: Response from the API
        """

        if is_courotine_function(create_random_object_func):
            create_obj = await create_random_object_func(db)
        else:
            create_obj = create_random_object_func()
        response = client.post(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
            json=create_obj,
        )

        assert response.status_code == 200

        content = response.json()

        self._compare_dicts(create_obj, content)

        return create_obj, response

    def _compare_dicts(
        self,
        dict1: Dict,
        dict2: Dict,
        ignore: Optional[List[str]] = [],
    ) -> None:
        """Compare two dictionaries

        Args:
            dict1 (Dict): Dictionary 1
            dict2 (Dict): Dictionary 2
            ignore (Optional[List[str]], optional): Keys to ignore. Defaults to [].
        """
        for key in dict1:
            if key in ignore:
                continue
            if isinstance(dict1[key], float):
                assert math.isclose(
                    dict1[key],
                    dict2[key],
                    rel_tol=1e-3,
                )
            else:
                assert dict1[key] == dict2[key]

    @pytest.mark.asyncio
    async def test_create_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        route_name: str,
        db: Session,
        create_random_object_func: Union[
            Callable[[Session], Awaitable[Dict]], Callable[[], Dict]
        ],
    ) -> None:
        """Test create instance

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            route_name (str): Route name
            db (Session): DB session

            create_random_object_func
            (Union[ Callable[[Session], Awaitable[Dict]], Callable[[], Dict] ]):
            Function to create a random object
        """
        await self._create_object_api(
            db, create_random_object_func, client, route_name, superuser_headers
        )

    @pytest.mark.asyncio
    async def test_get_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        unique_identifier: str,
        ignore_test_columns: List[str],
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
    ) -> None:
        """Test get instance

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            db (Session): DB session
            unique_identifier (str): Unique identifier
            ignore_test_columns (List[str]): Columns to ignore

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            route_name (str): Route name
        """
        _, object_out = await self._create_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        self._test_object(
            obj=object_out,
            compare_obj=content,
            ignore=ignore_test_columns,
        )

    def test_get_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        model_name: str,
        route_name: str,
        unique_identifier: str,
    ) -> None:
        """Test get instance not found

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            model_name (str): Model name
            route_name (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        not_found_object = 999
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
            auth=superuser_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {not_found_object}) in the table {model_name} was found."
        )

    @pytest.mark.asyncio
    async def test_get_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        get_high_permissions: bool,
        route_name: str,
        unique_identifier: str,
    ) -> None:
        """Test get instance not enough permissions

        Currently it tests all the routes, but it should be refactored to only test the routes that require high permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            get_high_permissions (bool): Whether to get high permissions for GET
            route_name (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        if not get_high_permissions:
            return 0

        _, object_out = await self._create_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
        )
        content = response.json()
        assert response.status_code == 401
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_get_instances(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
    ) -> None:
        """Test get instances

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
        """
        object_count = 5
        await self._create_multiple_objects_crud(db, object_generator_func, object_count)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content) >= object_count

    @pytest.mark.asyncio
    async def test_update_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        unique_identifier: str,
        update_request_params: bool,
        ignore_test_columns: List[str],
    ) -> None:
        """Test update instance

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function
            route_name (str): Route name
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
            ignore_test_columns (List[str]): Columns to ignore
        """
        _, object_out = await self._create_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errorspå
        assert delete_response.status_code == 200
        content_delete = delete_response.json()

        assert (
            content_delete
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully"
        )

        if update_request_params:
            obj_out_pk_map = self._create_primary_key_map(object_out)
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/",
                auth=superuser_headers,
                json=update_object_dict,
                params=obj_out_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
                auth=superuser_headers,
                json=update_object_dict,
            )

        assert response.status_code == 200
        content = response.json()

        self._test_object(
            update_object_out,
            content,
            ignore=ignore_test_columns,
        )

    @pytest.mark.asyncio
    async def test_update_instance_not_found(
        self,
        client: TestClient,
        db: Session,
        superuser_headers: Dict[str, str],
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        model_name: str,
        update_request_params: bool,
        unique_identifier: str,
    ) -> None:
        """Test update instance not found

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session
            superuser_headers (Dict[str, str]): Superuser headers

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
            model_name (str): Model name
            update_request_params (bool): Whether the update request requires params
            unique_identifier (str): Unique identifier
        """
        update_object_dict, update_object_out = await self._create_object_crud(
            db, object_generator_func
        )  # create the object to update and add to the db
        self._test_object(update_object_out, update_object_dict)

        update_obj_out_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_out_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()

        assert (
            content_delete
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_out_pk_map[unique_identifier]}) deleted successfully"
        )

        not_found_object = 999
        for key in update_obj_out_pk_map:
            update_obj_out_pk_map[key] = not_found_object

        if update_request_params:
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/",
                auth=superuser_headers,
                json=update_object_dict,
                params=update_obj_out_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
                auth=superuser_headers,
                json=update_object_dict,
            )

        assert response.status_code == 404

        content = response.json()

        assert (
            content["detail"]
            == f"No object matching the query ({', '.join([key + ': ' + str(item) for key, item in update_obj_out_pk_map.items()])}) in the table {model_name} was found."
        )

    @pytest.mark.asyncio
    async def test_update_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        superuser_headers: Dict[str, str],
        unique_identifier: str,
        update_request_params: bool,
    ) -> None:
        """Test update instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
            superuser_headers (Dict[str, str]): Superuser headers
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
        """
        _, object_out = await self._create_object_crud(db, object_generator_func)

        obj_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()

        assert (
            content_delete
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully"
        )

        if update_request_params:
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/",
                json=update_object_dict,
                params=obj_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/{obj_pk_map[unique_identifier]}",
                json=update_object_dict,
            )

        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_delete_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        unique_identifier: str,
    ) -> None:
        """Test delete instance

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
            unique_identifier (str): Unique identifier
        """
        _, update_object_out = await self._create_object_crud(db, object_generator_func)
        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        update_obj_pk_map = self._create_primary_key_map(update_object_out)
        assert (
            content
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully"
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        route_name: str,
        model_name: str,
        unique_identifier: str,
    ) -> None:
        """Test delete instance not found

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            route_name (str): Route name
            model_name (str): Model name
            unique_identifier (str): Unique identifier for the model
        """
        not_found_object = 999
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
            auth=superuser_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {not_found_object}) in the table {model_name} was found."
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        unique_identifier: str,
    ) -> None:
        """Test delete instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
            unique_identifier (str): Unique identifier
        """
        _, object_out = await self._create_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
