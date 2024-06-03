import math
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.crud.base import ModelType

from app.core.config import settings
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.utils.utils import get_ignore_keys, is_courotine_function

get_crud_test_model = UtilTestCRUD()


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI:
    def _db_obj_to_dict(self, db_obj: ModelType) -> Dict:
        """Convert a SQLAlchemy model to a dictionary.
        This is done since often only the db object has the primary key set.
        In the API url, the primary key is used to identify the object.

        Args:
            db_obj (ModelType): SQLAlchemy model

        Returns:
            Dict: Dictionary representation of the SQLAlchemy model
        """

        d = {}
        for column in db_obj.__table__.columns:
            d[column.name] = getattr(db_obj, column.name)

        return d

    def _create_primary_key_map(
        self, db_obj: ModelType, get_crud_test_model: UtilTestCRUD
    ) -> Dict:
        """Create a primary key map for a db object

        Args:
            db_obj (ModelType): SQLAlchemy model

        Returns:
            Dict: Primary key map
        """
        return get_crud_test_model._create_primary_key_map(db_obj)

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

        object_out_dict = self._db_obj_to_dict(object_out)

        return object_dict, object_out, object_out_dict

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
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        get_crud_test_model: UtilTestCRUD,
        route_name: str,
    ) -> None:
        _, object_out, object_out_dict = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        print("BROWHAT", content, "ISEQUAL? \n", object_out_dict)
        self._test_object(
            get_crud_test_model=get_crud_test_model,
            obj=object_out,
            compare_obj=content,
            ignore=["updatedAt", "createdAt"],
        )

    def test_get_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: Dict[str, str],
        model_name: str,
        route_name: str,
        unique_identifier: str,
    ) -> None:
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
        _, _, object_out_dict = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
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
        not_found_object: str,
        create_random_object_func: Callable[[], Dict],
        get_crud_test_model: UtilTestCRUD,
        unique_identifier: str,
    ) -> None:
        _, object_out, object_out_dict = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )

        update_object_dict, update_object_out, update_object_out_dict = (
            await self._create_object(db, object_generator_func, get_crud_test_model)
        )
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)
        
        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errorspå
        assert delete_response.status_code == 200
        content_delete = delete_response.json()
        print(
            "GREEENVADER",
            content_delete,
            "-----",
            f"{route_name} with mapping ('{unique_identifier}' : {update_object_out_dict[unique_identifier]}) deleted successfully",
        )
        assert (
            content_delete
            == f"{route_name} with mapping ('{unique_identifier}' : {update_object_out_dict[unique_identifier]}) deleted successfully"
        )
        # if is_courotine_function(create_random_object_func):
        #     updated_db_obj = await create_random_object_func(db)
        # else:
        #     updated_db_obj = create_random_object_func()

        print("DARKVADER", object_out_dict, "-----", object_out_dict[unique_identifier])
        print("BEASTVADER", update_object_dict, "----")
        print("GREENVADER", f"{settings.API_V1_STR}/{route_name}/{update_object_out_dict[unique_identifier]}")
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
            json=update_object_dict,
        )

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
        print("IGNORINGBESATONE", object_out)
        ignore = get_ignore_keys(object_out, content)
        self._test_object(
            get_crud_test_model,
            object_out,
            content,
            ignore=ignore + ["updatedAt", "createdAt"],
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
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        update_object_dict, update_object_out, update_object_out_dict = (
            await self._create_object(db, object_generator_func, get_crud_test_model)
        ) # create the object to update and add to the db
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()
        assert (
            content_delete
            == f"{route_name} with mapping ('{unique_identifier}' : {update_object_out_dict[unique_identifier]}) deleted successfully"
        )

        not_found_object = 999
        print("KRAKKENTALEN", update_object_dict)
        print(f"{settings.API_V1_STR}/{route_name}/{not_found_object}", "ROLLUP")
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
            auth=superuser_headers,
            json=update_object_dict,
        )

        print("KRAKKEN", response.status_code)
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {not_found_object}) in the table {model_name} was found."
        )

    @pytest.mark.asyncio
    async def test_update_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        superuser_headers: Dict[str, str],
        create_random_object_func: Callable[[], Dict],
        get_crud_test_model: UtilTestCRUD,
        unique_identifier: str,
    ) -> None:
        update_object_dict, update_object_out, update_object_out_dict = (
            await self._create_object(db, object_generator_func, get_crud_test_model)
        )
        self._test_object(get_crud_test_model, update_object_out, update_object_dict)

        delete_response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{update_object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )  # delete the object to avoid unique constraint errors
        assert delete_response.status_code == 200

        content_delete = delete_response.json()
        assert (
            content_delete
            == f"{route_name} with mapping ('{unique_identifier}' : {update_object_out_dict[unique_identifier]}) deleted successfully"
        )

        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{update_object_out_dict[unique_identifier]}",
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
        model_name: str,
        route_name: str,
        get_crud_test_model: UtilTestCRUD,
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert (
            content
            == f"{route_name} with mapping ('{unique_identifier}' : {object_out_dict[unique_identifier]}) deleted successfully"
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
        get_crud_test_model,
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(
            db, object_generator_func, get_crud_test_model
        )
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
