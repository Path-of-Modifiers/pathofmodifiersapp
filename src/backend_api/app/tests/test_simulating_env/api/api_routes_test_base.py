import math
from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.core.cache.user_cache import UserCache
from app.core.config import settings
from app.crud.base import CRUDBase, ModelType
from app.exceptions import (
    DbObjectDoesNotExistError,
)
from app.exceptions.model_exceptions.db_exception import DbObjectAlreadyExistsError
from app.exceptions.model_exceptions.request_exception import InvalidTokenError
from app.tests.test_simulating_env.base_test import BaseTest
from app.tests.utils.utils import is_courotine_function


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI(BaseTest):
    async def _create_object_api(
        self,
        async_client: AsyncClient,
        create_object: dict,
        route_prefix: str,
        superuser_token_headers: dict[str, str],
        on_duplicate_params: tuple[bool, str | None],
    ) -> Response:
        """Try to create an object using the API

        Args:
            async_client (AsyncClient): httpx test async client
            create_object (Dict): Create object dictionary
            route_prefix (str): Route name
            superuser_token_headers: (dict[str, str]): Superuser headers

        Returns:
            Response: Response from the API

        """
        on_duplicate_pkey_do_nothing = on_duplicate_params[0]
        if on_duplicate_pkey_do_nothing:
            response = await async_client.post(
                f"{settings.API_V1_STR}/{route_prefix}/",
                params={"on_duplicate_pkey_do_nothing": on_duplicate_pkey_do_nothing},
                headers=superuser_token_headers,
                json=create_object,
            )
        else:
            response = await async_client.post(
                f"{settings.API_V1_STR}/{route_prefix}/",
                headers=superuser_token_headers,
                json=create_object,
            )

        return response

    async def _create_random_object_api(
        self,
        db: Session,
        create_random_object_func: Callable[[], tuple[dict, ModelType, dict]] | Any,
        async_client: AsyncClient,
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

            async_client (AsyncClient): httpx test async client
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
        response = await async_client.post(
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

    @pytest.mark.anyio
    async def test_create_instance(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route_prefix: str,
        db: Session,
        create_random_object_func: (
            Callable[[Session], Awaitable[dict]] | Callable[[], dict]
        ),
    ) -> None:
        """Test create instance

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            route_prefix (str): Route name
            db (Session): DB session

            create_random_object_func
            (Union[ Callable[[Session], Awaitable[Dict]], Callable[[], Dict] ]):
            Function to create a random object
        """
        await self._create_random_object_api(
            db,
            create_random_object_func,
            async_client,
            route_prefix,
            superuser_token_headers,
        )

    @pytest.mark.anyio
    async def test_create_on_duplicate_pkey(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        crud_instance: CRUDBase,
        route_prefix: str,
        db: Session,
        create_random_object_func: Callable[[], tuple[dict, ModelType]],
        on_duplicate_params: tuple[bool, str | None],
    ) -> None:
        """Test create found duplicate instance"""
        on_duplicate_pkey_do_nothing = on_duplicate_params[0]
        # if not on_duplicate_pkey_do_nothing:
        # TODO: Make test database mock with unique constraints
        pytest.skip(
            f"CRUD test for route {route_prefix} does not support primary key on duplicate create test"
        )

        create_obj, response = await self._create_random_object_api(
            db=db,
            create_random_object_func=create_random_object_func,
            async_client=async_client,
            route_prefix=route_prefix,
            superuser_token_headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response_create_same_obj_with_dup_pkey = await self._create_object_api(
            async_client=async_client,
            create_object=create_obj,
            route_prefix=route_prefix,
            superuser_token_headers=superuser_token_headers,
            on_duplicate_params=on_duplicate_params,
        )
        assert response_create_same_obj_with_dup_pkey.status_code == 200

        response_create_same_obj_without_dup_pkey = await self._create_object_api(
            async_client=async_client,
            create_object=create_obj,
            route_prefix=route_prefix,
            superuser_token_headers=superuser_token_headers,
            on_duplicate_params=on_duplicate_params,
        )

        obj_value_pk_filter = crud_instance._map_obj_pks_to_value(create_obj)
        db_obj_already_exist_error = DbObjectAlreadyExistsError(
            model_table_name=crud_instance.model.__tablename__,
            filter=obj_value_pk_filter,
            function_name=crud_instance.create.__name__,
            class_name=crud_instance.__class__.__name__,
        )
        assert (
            response_create_same_obj_without_dup_pkey.status_code
            == db_obj_already_exist_error.status_code
        )
        assert (
            response_create_same_obj_without_dup_pkey.status_code
            == db_obj_already_exist_error.status_code
        )

    @pytest.mark.anyio
    async def test_get_instance(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        unique_identifier: str,
        ignore_test_columns: list[str],
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        is_hypertable: bool,
    ) -> None:
        """Test get instance

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session
            unique_identifier (str): Unique identifier
            ignore_test_columns (List[str]): Columns to ignore

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            route_prefix (str): Route name
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support get individual object operations")

        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = await async_client.get(
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

    @pytest.mark.anyio
    async def test_get_instance_not_found(
        self,
        async_client: AsyncClient,
        crud_instance: CRUDBase,
        superuser_token_headers: dict[str, str],
        model_table_name: str,
        route_prefix: str,
        unique_identifier: str,
        is_hypertable: bool,
    ) -> None:
        """Test get instance not found

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            model_table_name (str): Model name
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support get individual object operations")

        not_found_object = 999
        response = await async_client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
            headers=superuser_token_headers,
        )
        db_obj_does_not_exist_error = DbObjectDoesNotExistError(
            model_table_name=model_table_name,
            filter={unique_identifier: not_found_object},
            function_name=crud_instance.get.__name__,
            class_name=crud_instance.__class__.__name__,
        )
        assert response.status_code == db_obj_does_not_exist_error.status_code
        content = response.json()
        assert content["detail"] == db_obj_does_not_exist_error.detail

    @pytest.mark.anyio
    async def test_get_instance_not_enough_permissions(
        self,
        async_client: AsyncClient,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        get_high_permissions: bool,
        route_prefix: str,
        unique_identifier: str,
        is_hypertable: bool,
    ) -> None:
        """Test get instance not enough permissions

        Currently it tests all the routes, but it should be refactored to only test the routes that require high permissions

        Args:
            async_client (AsyncClient): httpx test async client
            db (Session): DB session

            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            get_high_permissions (bool): Whether to get high permissions for GET
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier for the model
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support get individual object operations")

        if not get_high_permissions:
            return 0

        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = await async_client.get(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
        )
        content = response.json()
        invalid_token_error = InvalidTokenError(
            token=None,
            function_name=UserCache.verify_token.__name__,
            class_name=UserCache.__name__,
        )
        assert response.status_code == invalid_token_error.status_code
        assert content["detail"] == invalid_token_error.detail

    @pytest.mark.anyio
    async def test_get_instances(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        is_hypertable: bool,
    ) -> None:
        """Test get instances

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support get individual object operations")

        object_count = 5
        await self._create_multiple_random_objects_crud(
            db, object_generator_func, object_count
        )
        response = await async_client.get(
            f"{settings.API_V1_STR}/{route_prefix}/", headers=superuser_token_headers
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content) >= object_count

    @pytest.mark.anyio
    async def test_update_instance(
        self,
        request,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
        update_request_params: bool,
        ignore_test_columns: list[str],
        is_hypertable: bool,
    ) -> None:
        """Test update instance

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function
            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
            ignore_test_columns (List[str]): Columns to ignore
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support update object operations")

        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = await async_client.delete(
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
            # TODO: Change this cheap skip. Change method to do updates for hypertables (by not doing them). Since hypertable layout is
            # new and uncertain, we just skip the update test for these cheaply for now
            pytest.skip(
                f"Test with route {route_prefix} doesn't support update operations (has multiple update request params)"
            )
            # obj_out_pk_map = self._create_primary_key_map(object_out)
            # response = await async_client.put(
            #     f"{settings.API_V1_STR}/{route_prefix}/",
            #     headers=superuser_token_headers,
            #     json=update_object_dict,
            #     params=obj_out_pk_map,
            # )
        else:
            response = await async_client.put(
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

    @pytest.mark.anyio
    async def test_update_instance_not_found(
        self,
        async_client: AsyncClient,
        db: Session,
        crud_instance: CRUDBase,
        superuser_token_headers: dict[str, str],
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        update_request_params: bool,
        unique_identifier: str,
        is_hypertable: bool,
    ) -> None:
        """Test update instance not found

        Args:
            async_client (AsyncClient): httpx test async client
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
        if is_hypertable:
            pytest.skip("Hypertables doesn't support update object operations")

        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )  # create the object to update and add to the db
        self._test_object(update_object_out, update_object_dict)

        update_obj_out_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = await async_client.delete(
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
            # TODO: Change this cheap skip. Change method to do updates for hypertables (by not doing them). Since hypertable layout is
            # new and uncertain, we just skip the update test for these cheaply for now
            pytest.skip(
                f"Test with route {route_prefix} doesn't support update operations (has multiple update request params)"
            )

            # response = await async_client.put(
            #     f"{settings.API_V1_STR}/{route_prefix}/",
            #     headers=superuser_token_headers,
            #     json=update_object_dict,
            #     params=update_obj_out_pk_map,
            # )
        else:
            response = await async_client.put(
                f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
                headers=superuser_token_headers,
                json=update_object_dict,
            )

        db_obj_does_not_exist_error = DbObjectDoesNotExistError(
            model_table_name=model_table_name,
            filter=update_obj_out_pk_map,
            function_name=crud_instance.get.__name__,
            class_name=crud_instance.__class__.__name__,
        )
        assert response.status_code == db_obj_does_not_exist_error.status_code
        assert response.json()["detail"] == db_obj_does_not_exist_error.detail

    @pytest.mark.anyio
    async def test_update_instance_not_enough_permissions(
        self,
        async_client: AsyncClient,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        superuser_token_headers: dict[str, str],
        unique_identifier: str,
        update_request_params: bool,
        is_hypertable: bool,
    ) -> None:
        """Test update instance not enough permissions

        Args:
            async_client (AsyncClient): httpx test async client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            superuser_token_headers: dict[str, str] : Superuser headers
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support update object operations")

        _, object_out = await self._create_random_object_crud(db, object_generator_func)

        obj_pk_map = self._create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        self._test_object(update_object_out, update_object_dict)

        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        delete_response = await async_client.delete(
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
            response = await async_client.put(
                f"{settings.API_V1_STR}/{route_prefix}/",
                json=update_object_dict,
                params=obj_pk_map,
            )
        else:
            response = await async_client.put(
                f"{settings.API_V1_STR}/{route_prefix}/{obj_pk_map[unique_identifier]}",
                json=update_object_dict,
            )
        invalid_token_error = InvalidTokenError(
            token=None,
            function_name=UserCache.verify_token.__name__,
            class_name=UserCache.__name__,
        )
        assert response.status_code == invalid_token_error.status_code
        content = response.json()
        assert content["detail"] == invalid_token_error.detail

    @pytest.mark.anyio
    async def test_delete_instance(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
        is_hypertable: bool,
    ) -> None:
        """Test delete instance

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support delete object operations")

        _, update_object_out = await self._create_random_object_crud(
            db, object_generator_func
        )
        update_obj_pk_map = self._create_primary_key_map(update_object_out)

        response = await async_client.delete(
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

    @pytest.mark.anyio
    async def test_delete_instance_not_found(
        self,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route_prefix: str,
        model_table_name: str,
        unique_identifier: str,
        crud_instance: CRUDBase,
        is_hypertable: bool,
    ) -> None:
        """Test delete instance not found

        Args:
            async_client (AsyncClient): httpx test async client
            superuser_token_headers: dict[str, str] : Superuser headers
            model_table_name (str): Route name
            model_table_name (str): Model table name
            unique_identifier (str): Unique identifier for the model
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support delete object operations")

        not_found_object = 999
        response = await async_client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{not_found_object}",
            headers=superuser_token_headers,
        )
        db_obj_not_exists_error = DbObjectDoesNotExistError(
            model_table_name=model_table_name,
            filter={unique_identifier: not_found_object},
            function_name=crud_instance.remove.__name__,
            class_name=crud_instance.__class__.__name__,
        )
        assert response.status_code == db_obj_not_exists_error.status_code
        content = response.json()
        assert content["detail"] == db_obj_not_exists_error.detail

    @pytest.mark.anyio
    async def test_delete_instance_not_enough_permissions(
        self,
        async_client: AsyncClient,
        db: Session,
        object_generator_func: Callable[[], tuple[dict, ModelType]],
        route_prefix: str,
        unique_identifier: str,
        is_hypertable: bool,
    ) -> None:
        """Test delete instance not enough permissions

        Args:
            async_client (AsyncClient): httpx test async client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_prefix (str): Route name
            unique_identifier (str): Unique identifier
        """
        if is_hypertable:
            pytest.skip("Hypertables doesn't support delete object operations")

        _, object_out = await self._create_random_object_crud(db, object_generator_func)
        obj_out_pk_map = self._create_primary_key_map(object_out)
        response = await async_client.delete(
            f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
        )
        invalid_token_error = InvalidTokenError(
            token=None,
            function_name=UserCache.verify_token.__name__,
            class_name=UserCache.__name__,
        )
        assert response.status_code == invalid_token_error.status_code
        content = response.json()
        assert content["detail"] == invalid_token_error.detail
