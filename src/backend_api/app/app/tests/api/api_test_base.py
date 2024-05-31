from typing import Callable, Dict, Tuple, Union
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.crud.base import ModelType

from app.core.config import settings


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestAPI:

    def test_create_instance(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        route_name: str,
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        instance = create_random_object_func()
        response = client.post(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
            json=instance,
        )
        assert response.status_code == 200
        content = response.json()
        assert unique_identifier in content
        for key in instance:
            assert content[key] == instance[key]

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
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        for key in instance_dict:
            assert content[key] == instance_dict[key]

    def test_get_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        create_random_object_func: Callable[[], Dict],
        model_name: str,
        route_name: str,
        unique_identifier: str,
    ) -> None:
        create_object = create_random_object_func()
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{create_object[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {create_object[unique_identifier]}) in the table {model_name} was found."
        )

    @pytest.mark.asyncio
    async def test_get_instance_not_enough_permissions(
        self,
        client: TestClient,
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
        unique_identifier: str,
    ) -> None:
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_get_instances(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        db: Session,
        object_generator_func: Union[Callable[[], Tuple[Dict, ModelType]]],
        route_name: str,
    ) -> None:
        await object_generator_func(db)
        await object_generator_func(db)
        response = client.get(
            f"{settings.API_V1_STR}/{route_name}/",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert len(content[0]) >= 2

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
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        updated_instance = create_random_object_func()
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
            auth=superuser_headers,
            json=updated_instance,
        )
        assert response.status_code == 200
        content = response.json()
        for key in updated_instance:
            assert content[key] == updated_instance[key]

    def test_update_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        route_name: str,
        model_name: str,
        create_random_object_func: Callable[[], Dict],
        unique_identifier: str,
    ) -> None:
        create_object = create_random_object_func()
        updated_instance = create_random_object_func()
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{create_object[unique_identifier]}",
            auth=superuser_headers,
            json=updated_instance,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {create_object[unique_identifier]}) in the table {model_name} was found."
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
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        updated_instance = create_random_object_func()
        response = client.put(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
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
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert (
            content
            == f"{model_name.capitalize()} with mapping ({unique_identifier} : {instance_dict[unique_identifier]}) deleted successfully"
        )

    @pytest.mark.asyncio
    async def test_delete_instance_not_found(
        self,
        client: TestClient,
        superuser_headers: dict[str, str],
        create_random_object_func: Callable[[], Dict],
        route_name: str,
        model_name: str,
        unique_identifier: str,
    ) -> None:
        create_object = create_random_object_func()
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{create_object[unique_identifier]}",
            auth=superuser_headers,
        )
        assert response.status_code == 404
        content = response.json()
        assert (
            content["detail"]
            == f"No object matching the query ({unique_identifier}: {create_object[unique_identifier]}) in the table {model_name} was found."
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
        instance = await object_generator_func(db)
        instance_dict = instance[0]
        response = client.delete(
            f"{settings.API_V1_STR}/{route_name}/{instance_dict[unique_identifier]}",
        )
        assert response.status_code == 401
        content = response.json()
        assert content["detail"] == "Not authenticated"
