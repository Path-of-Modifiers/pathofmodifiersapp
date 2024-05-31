from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.crud.base import ModelType

from app.core.config import settings
from app.tests.crud.crud_test_base import TestCRUD


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

    async def _create_object(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
    ) -> Tuple[Dict, ModelType]:
        """Generate an object and return the object dictionary and the object itself

        Args:
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]], Any]): Function
            to generate the object

        Returns:
            Tuple[Dict, ModelType]: Object dictionary, the object itself and the db object dictionary
        """
        crud_test = TestCRUD()

        object_dict, object_out = await crud_test._create_object(
            db, object_generator_func
        )

        object_out_dict = self._db_obj_to_dict(object_out)

        return object_dict, object_out, object_out_dict

    async def _create_multiple_objects(
        self,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]], Any],
        count: int,
    ) -> Tuple[Tuple[Dict], Tuple[ModelType]]:
        """Create multiple objects

        Args:
            db (Session): DB session
            object_generator_func (Union[Callable[[], Tuple[Dict, ModelType]], Any]): Function
            to generate the object
            count (int): Number of objects to create

        Returns:
            Tuple[Tuple[Dict], Tuple[ModelType]]: Tuple of object dictionaries and objects
        """
        crud_test = TestCRUD()

        multiple_object_dict, multiple_object_out = (
            await crud_test._create_multiple_objects(db, object_generator_func, count)
        )

        return multiple_object_dict, multiple_object_out

    def _test_object(
        self,
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
        """
        crud_test = TestCRUD()

        crud_test._test_object(obj, compare_obj, ignore)

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
            assert dict1[key] == dict2[key]

    def test_create_instance(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        route_name: str,
        create_random_object_func: Callable[[], Dict],
    ) -> None:
        create_obj = create_random_object_func()
        response = client.post(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
            json=create_obj,
        )
        assert response.status_code == 200
        content = response.json()
        self._compare_dicts(create_obj, content)

    @pytest.mark.asyncio
    async def test_get_instance(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        unique_identifier: str,
    ) -> None:
        _, object_out, object_out_dict = await self._create_object(
            db, object_generator_func
        )
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        print("BROWHAT", content, "ISEQUAL? \n", object_out_dict)
        self._test_object(object_out, content, ignore=["updatedAt", "createdAt"])

    def test_get_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
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
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(db, object_generator_func)
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
        superuser_headers: dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
    ) -> None:
        await self._create_multiple_objects(db, object_generator_func, 5)
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
        superuser_headers: dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(db, object_generator_func)
        updated_db_obj = create_random_object_func()
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
            json=updated_db_obj,
        )
        assert response.status_code == 200
        content = response.json()
        self._compare_dicts(updated_db_obj, content)

    def test_update_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        route_name: str,
        model_name: str,
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        updated_instance = create_random_object_func()
        not_found_object = 999
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{not_found_object}",
            auth=superuser_headers,
            json=updated_instance,
        )
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
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(db, object_generator_func)
        updated_instance = create_random_object_func()
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            json=updated_instance,
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_delete_instance(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        model_name: str,
        route_name: str,
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(db, object_generator_func)
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert (
            content
            == f"{model_name.capitalize()} with mapping ({{'{unique_identifier}': '{object_out_dict[unique_identifier]}'}}) deleted successfully"
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
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
        unique_identifier: str,
    ) -> None:
        _, _, object_out_dict = await self._create_object(db, object_generator_func)
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{object_out_dict[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
