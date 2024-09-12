import math
from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.core.config import settings
from app.crud.base import CRUDBase, ModelType
from app.exceptions import (
    DbObjectDoesNotExistError,
)
from app.exceptions.model_exceptions.db_exception import DbObjectAlreadyExistsError
from app.tests.base_test import BaseTest
from app.tests.utils.utils import is_courotine_function


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI(BaseTest):
    async def _create_object_api(
        self,
        client: TestClient,
        create_object: dict,
        route_prefix: str,
        superuser_token_headers: dict[str, str],
    ) -> Response:
        """Try to create an object using the API

        Args:
            client (TestClient): FastAPI test client
            create_object (Dict): Create object dictionary
            route_prefix (str): Route name
            superuser_token_headers: (dict[str, str]): Superuser headers

        Returns:
            Response: Response from the API

        """

        response = client.post(
            f"{settings.API_V1_STR}/{route_prefix}/",
            headers=superuser_token_headers,
            json=create_object,
        )

        return response

    async def _create_random_object_api(
        self,
        db: Session,
        create_random_object_func: Callable[[], tuple[dict, ModelType, dict]] | Any,
        client: TestClient,
        route_prefix: str,
        superuser_token_headers: dict[str, str],
    ) -> tuple[dict, Response]:
        """Create a random object using the API

        Also tests correct response codes and if the object created is
        the same as the object returned by the API

        Args:
            db (Session): DB session

            create_random_object_func
            (Union[Callable[[], Tuple[Dict, ModelType, Dict]], Any]):
            Create random object function

            client (TestClient): FastAPI test client
            route_prefix (str): Route name
            superuser_token_headers: (dict[str, str]): Superuser headers

        Returns:
            Dict: Object dictionary created
            Response: Response from the API
        """
        if is_courotine_function(create_random_object_func):
            create_obj = await create_random_object_func(db)
        else:
            create_obj = create_random_object_func()
        response = client.post(
            f"{settings.API_V1_STR}/{route_prefix}/",
            headers=superuser_token_headers,
            json=create_obj,
        )

        assert response.status_code == 200

        content = response.json()

        self._compare_dicts(create_obj, content)

        return create_obj, response

    def _compare_dicts(
        self,
        dict1: dict,
        dict2: dict,
        ignore: list[str] | None = None,
    ) -> None:
        """Compare two dictionaries

        Args:
            dict1 (Dict): Dictionary 1
            dict2 (Dict): Dictionary 2
            ignore (list[str] | optional): Keys to ignore. Defaults to [].
        """
        if ignore is None:
            ignore = []
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
        superuser_token_headers: dict[str, str],
        route_prefix: str,
        db: Session,
        create_random_object_func: (
            Callable[[Session], Awaitable[dict]] | Callable[[], dict]
        ),
    ) -> None:
        """Test create instance

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            route_prefix (str): Route name
            db (Session): DB session

            create_random_object_func
            (Union[ Callable[[Session], Awaitable[Dict]], Callable[[], Dict] ]):
            Function to create a random object
        """
        await self._create_random_object_api(
            db, create_random_object_func, client, route_prefix, superuser_token_headers
        )

    @pytest.mark.asyncio
    async def test_create_found_duplicate(
        self,
        client: TestClient,
        crud_instance: CRUDBase,
        superuser_token_headers: dict[str, str],
        route_prefix: str,
        db: Session,
        create_random_object_func: Callable[[], tuple[dict, ModelType]],
    ) -> None:
        """Test create found duplicate instance"""
        if crud_instance.ignore_duplicates:
            pytest.skip(
                f"API test for test_create_found_duplicate in route {route_prefix} does not support ignore_duplicates"
            )

        create_obj, response = await self._create_random_object_api(
            db,
            create_random_object_func,
            client,
            route_prefix,
            superuser_token_headers,
        )
        create_obj_create_schema = crud_instance.create_schema(**create_obj)
        obj_pks_value_filter = crud_instance._map_obj_pks_to_value(
            create_obj_create_schema
        )[0]
        response = await self._create_object_api(
            client,
            create_obj,
            route_prefix,
            superuser_token_headers,
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == DbObjectAlreadyExistsError(
                model_table_name=crud_instance.model.__tablename__,
                filter=obj_pks_value_filter,
                function_name=crud_instance.create.__name__,
                class_name=crud_instance.__class__.__name__,
            ).detail
        )

    @pytest.mark.asyncio
    async def test_get_instance(
        self,
        client: TestClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        unique_identifier: str,
        ignore_test_columns: list[str],
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
    ) -> None:
        """Test get instance

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session
            unique_identifier (str): Unique identifier
            ignore_test_columns (List[str]): Columns to ignore

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            route_prefix (str): Route name
        """
        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
            headers=superuser_token_headers,
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
        crud_instance: CRUDBase,
        superuser_token_headers: dict[str, str],
        model_table_name: str,
        route_prefix: str,
        unique_identifier: str,
    ) -> None:
        """Test get instance not found

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            model_table_name (str): Model name
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        not_found_object = 999
        response = client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == DbObjectDoesNotExistError(
                model_table_name=model_table_name,
                filter={unique_identifier: not_found_object},
                function_name=crud_instance.get.__name__,
                class_name=crud_instance.__class__.__name__,
            ).detail
        )

    @pytest.mark.asyncio
    async def test_get_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        crud_instance: CRUDBase,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        get_high_permissions: bool,
        route_prefix: str,
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
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        if not get_high_permissions:
            return 0

        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
        )
        content = response.json()
        assert response.status_code == 401
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_get_instances(
        self,
        client: TestClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
    ) -> None:
        """Test get instances

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
        """
        object_count = 5
        await self._create_multiple_objects_crud(
            db, object_generator_func, object_count
        )
        response = client.get(
            f"{settings.API_V1_STR}/{route_prefix}/", headers=superuser_token_headers
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content) >= object_count

    @pytest.mark.asyncio
    async def test_update_instance(
        self,
        client: TestClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
        update_request_params: bool,
        ignore_test_columns: list[str],
    ) -> None:
        """Test update instance

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
            ignore_test_columns (List[str]): Columns to ignore
        """
        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{update_obj_pk_map[unique_identifier]}",
            headers=superuser_token_headers,
        )  # delete the object to avoid unique constraint errorspå
        assert delete_response.status_code == 200
        content_delete = delete_response.json()

        assert (
            content_delete
            == get_delete_return_msg(
                model_table_name=model_table_name,
                filter={unique_identifier: update_obj_pk_map[unique_identifier]},
            ).message
        )

        if update_request_params:
            obj_out_pk_map = self._create_primary_key_map(object_out)
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/",
                headers=superuser_token_headers,
                json=update_object_dict,
                params=obj_out_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
                headers=superuser_token_headers,
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
        crud_instance: CRUDBase,
        superuser_token_headers: dict[str, str],
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        update_request_params: bool,
        unique_identifier: str,
    ) -> None:
        """Test update instance not found

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session
            superuser_token_headers: dict[str, str] : Superuser headers

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            model_table_name (str): Model name
            model_table_name (str): Model name
            update_request_params (bool): Whether the update request requires params
            unique_identifier (str): Unique identifier
        """
        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )  # create the object to update and add to the db
        self._test_object(update_object_out, update_object_dict)

        update_obj_out_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{update_obj_out_pk_map[unique_identifier]}",
            headers=superuser_token_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()

        assert (
            content_delete
            == get_delete_return_msg(
                model_table_name=model_table_name,
                filter={unique_identifier: update_obj_out_pk_map[unique_identifier]},
            ).message
        )

        not_found_object = 999
        for key in update_obj_out_pk_map:
            update_obj_out_pk_map[key] = not_found_object

        if update_request_params:
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/",
                headers=superuser_token_headers,
                json=update_object_dict,
                params=update_obj_out_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
                headers=superuser_token_headers,
                json=update_object_dict,
            )

        assert response.status_code == 404

        content = response.json()

        assert (
            content["detail"]
            == DbObjectDoesNotExistError(
                model_table_name=model_table_name,
                filter=update_obj_out_pk_map,
                function_name=crud_instance.get.__name__,
                class_name=crud_instance.__class__.__name__,
            ).detail
        )

    @pytest.mark.asyncio
    async def test_update_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        superuser_token_headers: dict[str, str],
        unique_identifier: str,
        update_request_params: bool,
    ) -> None:
        """Test update instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            superuser_token_headers: dict[str, str] : Superuser headers
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
        """
        _, object_out = await self._create_random_object_crud(db, object_generator_func)

        obj_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{update_obj_pk_map[unique_identifier]}",
            headers=superuser_token_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()

        assert (
            content_delete
            == get_delete_return_msg(
                model_table_name=model_table_name,
                filter={unique_identifier: update_obj_pk_map[unique_identifier]},
            ).message
        )

        if update_request_params:
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/",
                json=update_object_dict,
                params=obj_pk_map,
            )
        else:
            response = client.put(
                f"{settings.API_V1_STR}/{route_prefix}/{obj_pk_map[unique_identifier]}",
                json=update_object_dict,
            )

        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_delete_instance(
        self,
        client: TestClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
    ) -> None:
        """Test delete instance

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
        """
        _, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{update_obj_pk_map[unique_identifier]}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        update_obj_pk_map = self._create_primary_key_map(update_object_out)
        assert (
            content
            == get_delete_return_msg(
                model_table_name=model_table_name,
                filter={unique_identifier: update_obj_pk_map[unique_identifier]},
            ).message
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_found(
        self,
        client: TestClient,
        superuser_token_headers: dict[str, str],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
        crud_instance: CRUDBase,
    ) -> None:
        """Test delete instance not found

        Args:
            client (TestClient): FastAPI test client
            superuser_token_headers: dict[str, str] : Superuser headers
            model_table_name (str): Route name
            model_table_name (str): Model table name
            unique_identifier (str): Unique identifier for the model
        """
        not_found_object = 999
        response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == DbObjectDoesNotExistError(
                model_table_name=model_table_name,
                filter={unique_identifier: not_found_object},
                function_name=crud_instance.remove.__name__,
                class_name=crud_instance.__class__.__name__,
            ).detail
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        unique_identifier: str,
    ) -> None:
        """Test delete instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
        """
        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
