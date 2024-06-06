import math
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.crud.base import ModelType
from app.core.config import settings
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.utils import create_primary_key_map, is_courotine_function

get_crud_test_model = UtilTestCRUD()


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI:
    async def _create_object(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType, Dict]], Any],
        get_crud_test_model: UtilTestCRUD,
    ) -> Tuple[Dict, ModelType]:
        """Generate an object and return the object dictionary and the object itself

        Args:
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]], Any]): Function
            to generate the object
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance


        Returns:
            Tuple[Dict, ModelType]: Object dictionary, the object itself and the db object dictionary
        """

        object_dict, object_out = await get_crud_test_model._create_object(
            db, object_generator_func
        )

        return object_dict, object_out

    async def _create_multiple_objects(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
        count: int,
        get_crud_test_model: UtilTestCRUD,
    ) -> Tuple[Tuple[Dict], Tuple[ModelType]]:
        """Create multiple objects

        Args:
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]], Any]): Function
            to generate the object
            count (int): Number of objects to create
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance

        Returns:
            Tuple[Tuple[Dict], Tuple[ModelType]]: Tuple of object dictionaries and objects
        """

        multiple_object_dict, multiple_object_out = (
            await get_crud_test_model._create_multiple_objects(
                db, object_generator_func, count
            )
        )

        return multiple_object_dict, multiple_object_out

    def _test_object(
        self,
        get_crud_test_model: UtilTestCRUD,
        obj: Union[ModelType, List[ModelType]],
        compare_obj: Optional[
            Union[Dict, List[Dict], ModelType, List[ModelType]]
        ] = None,
        ignore: Optional[List[str]] = [],
    ):
        """Test if two objects are the same

        Args:
            obj (Union[ModelType, List[ModelType]]): Object to test
            compare_obj (Optional[ Union[Dict, List[Dict], ModelType, List[ModelType]] ], optional): Comparing object. Defaults to None.
            ignore (Optional[List[str]], optional): List of ignored attributes. Defaults to [].
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
        """
        get_crud_test_model._test_object(obj, compare_obj, ignore)

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
        print("BRAGE:::::   ", content)
        print("DRAGE:::::   ", create_obj)
        self._compare_dicts(create_obj, content)

    @pytest.mark.asyncio
    async def test_get_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        unique_identifier: str,
        ignore_test_columns: List[str],
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        get_crud_test_model: UtilTestCRUD,
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

            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            route_name (str): Route name
        """
        _, object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        obj_out_pk_map = create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        print("BROWHAT", content, "ISEQUAL? \n", obj_out_pk_map)
        self._test_object(
            get_crud_test_model=get_crud_test_model,
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
        get_crud_test_model: UtilTestCRUD,
        unique_identifier: str,
    ) -> None:
        """Test get instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]]]):
            Object generator function

            get_high_permissions (bool): Whether to get high permissions for GET
            route_name (str): Route name
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            unique_identifier (str): Unique identifier for the model
        """
        _, object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        obj_out_pk_map = create_primary_key_map(object_out)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
        )
        print("JAKSEN", response.status_code)
        if get_high_permissions:
            content = response.json()
            assert response.status_code == 401
            assert content["detail"] == "Not authenticated"
        else:
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_instances(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        get_crud_test_model: UtilTestCRUD,
        route_name: str,
    ) -> None:
        """Test get instances

        Args:
            client (TestClient): FastAPI test client
            superuser_headers (Dict[str, str]): Superuser headers
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            route_name (str): Route name
        """
        await self._create_multiple_objects(
            db, object_generator_func, 5, get_crud_test_model
        )
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content) >= 5

    @pytest.mark.asyncio
    async def test_update_instance(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        get_crud_test_model: UtilTestCRUD,
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
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
            ignore_test_columns (List[str]): Columns to ignore
        """
        _, object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        obj_out_pk_map = create_primary_key_map(object_out)

        print("HAGGLEBU", update_request_params)
        update_object_dict, update_object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)

        update_obj_pk_map = create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errorspå
        assert delete_response.status_code == 200
        content_delete = delete_response.json()

        print(
            "GREEENVADER",
            content_delete,
            "-----",
            f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully",
        )
        assert (
            content_delete
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully"
        )
        # if is_courotine_function(create_random_object_func):
        #     updated_db_obj = await create_random_object_func(db)
        # else:
        #     updated_db_obj = create_random_object_func()

        print("DARKVADER", obj_out_pk_map[unique_identifier])
        print("BEASTVADER", update_object_dict, "----")
        print(
            "GREENVADER",
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
        )

        if update_request_params:
            print("KRAQQEDUPDATEINSTANCE")
            obj_out_pk_map = create_primary_key_map(object_out)
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
        print("RESPURL", response.url)

        print(
            "DARKVADERUNIQUE",
            route_name,
            "-----",
            unique_identifier,
            "-----",
            response.status_code,
        )
        assert response.status_code == 200
        content = response.json()
        # print(
        #     "TESTUPDATEINSTANCE\ncontent:  ",
        #     content,
        #     "\nupdated_db_obj:  ",
        #     updated_db_obj,
        # )
        print("IGNORINGBESAT", content)
        print("IGNORINGBESATONE", object_out.__dict__)
        print("POKEMONBM :::: ", ignore_test_columns)
        self._test_object(
            get_crud_test_model,
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
        # We need to c
        update_object_dict, update_object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )  # create the object to update and add to the db
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)

        update_obj_out_pk_map = create_primary_key_map(update_object_out)

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

        print("KRAKKENTALEN", update_object_dict)
        print(f"{settings.API_V1_STR}/{route_name}/{not_found_object}", "ROLLUP")

        if update_request_params:
            print("KRAQQEDNOTFOUND")
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/",
                auth=superuser_headers,
                json=update_object_dict,
                params=update_obj_out_pk_map,
            )
        else:
            print(
                "YODAPÅTURE", f"{settings.API_V1_STR}/{route_name}/{not_found_object}"
            )
            response = client.put(
                f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
                auth=superuser_headers,
                json=update_object_dict,
            )

        print("KRAKKEN", response.status_code)
        assert response.status_code == 404
        content = response.json()
        print("YOUTUBERN :::::", content["detail"])
        print(
            "YOUTUBERNXXXXXX :::  ",
            f"No object matching the query ({', '.join([key + ': ' + str(item) for key, item in update_obj_out_pk_map.items()])}) in the table {model_name} was found.",
        )
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
        get_crud_test_model: UtilTestCRUD,
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
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            unique_identifier (str): Unique identifier
            update_request_params (bool): Whether the update request requires params
        """
        _, object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )

        obj_pk_map = create_primary_key_map(object_out)

        update_object_dict, update_object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)

        update_obj_pk_map = create_primary_key_map(update_object_out)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()

        print(
            "KRAKKEDNOPERMISSIONS :::: ",
            f"{route_name} with mapping ({', '.join([key + ': ' + str(item) for key, item in update_obj_pk_map.items()])}) deleted successfully",
        )
        assert (
            content_delete
            == f"{route_name} with mapping ({unique_identifier}: {update_obj_pk_map[unique_identifier]}) deleted successfully"
        )

        if update_request_params:
            print("KRAQQEDNOPERMISSIONS")
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
        beast_status_code = response.status_code
        print("UGLAKRAKKEDNOPERMISSIONS ::: ", beast_status_code)
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
        get_crud_test_model: UtilTestCRUD,
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
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            unique_identifier (str): Unique identifier
        """
        _, update_object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        update_obj_pk_map = create_primary_key_map(update_object_out)

        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_obj_pk_map[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        update_obj_pk_map = create_primary_key_map(update_object_out)
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
        get_crud_test_model: UtilTestCRUD,
        unique_identifier: str,
    ) -> None:
        """Test delete instance not enough permissions

        Args:
            client (TestClient): FastAPI test client
            db (Session): DB session

            object_generator_func
            (Union[Callable[[], Tuple[Dict, ModelType]]]): Object generator function

            route_name (str): Route name
            get_crud_test_model (UtilTestCRUD): UtilTestCRUD instance
            unique_identifier (str): Unique identifier
        """
        _, object_out = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        obj_out_pk_map = create_primary_key_map(object_out)
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{obj_out_pk_map[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
