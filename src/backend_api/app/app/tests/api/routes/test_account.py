from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.models import Account as model

import app.api.api_v1.endpoints.account as account_api

from app.core.config import settings
from app.tests.utils.model_utils import (
    create_random_account_dict,
    generate_random_account,
)
from app.tests.api.utils import get_superuser_headers


def test_create_account(client: TestClient) -> None:
    account = create_random_account_dict()
    response = client.post(
        f"{settings.API_V1_STR}/account/",
        headers=get_superuser_headers(),
        json=account,
    )
    assert response.status_code == 200
    content = response.json()
    assert "accountName" in content
    assert "isBanned" in content
    assert content["accountName"] == account["accountName"]
    assert content["isBanned"] == account["isBanned"]


async def test_get_account(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/account/{account.accountName}",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 200
    content = response.json()
    assert content["accountName"] == account.accountName
    assert content["isBanned"] == account.isBanned


def test_get_account_not_found(
    client: TestClient,
) -> None:
    accountNameTest = "999"
    response = client.get(
        f"{settings.API_V1_STR}/account/{accountNameTest}",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 404
    content = response.json()
    assert (
        content["detail"]
        == f"Not Found"
    )


async def test_get_account_not_enough_permissions(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/account/{account.accountName}",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 400
    content = response.json()
    assert (
        content["detail"]
        == f"Unauthorize API access for {account_api.get_account.__name__}"
    )


async def test_get_account(client: TestClient, db: Session) -> None:
    await generate_random_account(db)
    await generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/account/",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


async def test_update_account(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/account/{account.accountName}",
        headers=get_superuser_headers(),
        json=updated_account,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["accountName"] == updated_account["accountName"]
    assert content["isBanned"] == updated_account["isBanned"]


async def test_update_account_not_found(
    client: TestClient,
) -> None:
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/account/999",
        headers=get_superuser_headers(),
        json=updated_account,
    )
    assert response.status_code == 404
    content = response.json()
    assert (
        content["detail"]
        == f"No object matching the query ({model.accountName.__str__} : {content['accountName']}) in the table {model.__tablename__} was found."
    )


async def test_update_account_not_enough_permissions(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/account/{account.accountName}",
        headers=get_superuser_headers(),
        json=updated_account,
    )
    assert response.status_code == 400
    content = response.json()
    assert (
        content["detail"]
        == f"Unauthorized API access for {account_api.update_account.__name__}"
    )


async def test_delete_account(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/account/{account.accountName}",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 200
    content = response.json()
    assert (
        content["message"]
        == f"Account with mapping ({model.accountName.__str__}: {content['accountName']}) deleted successfully"
    )


async def test_delete_account_not_found(client: TestClient) -> None:
    response = await client.delete(
        f"{settings.API_V1_STR}/account/999",
        headers=get_superuser_headers(),
    )
    assert response.status_code == 404
    content = response.json()
    assert (
        content["detail"]
        == f"No object matching the query ({model.accountName.__str__}: {content['accountName']}) in the table {model.__tablename__} was found."
    )


async def test_delete_account_not_enough_permissions(client: TestClient, db: Session) -> None:
    account = await generate_random_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/account/{account.accountName}",
    )
    assert response.status_code == 400
    content = response.json()
    assert (
        content["detail"]
        == f"Unauthorized API access for {account_api.delete_account.__name__}"
    )
