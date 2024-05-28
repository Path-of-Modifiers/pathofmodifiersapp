from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.models import Account as model

import app.app.api.api_v1.endpoints.account as account_api

from app.core.config import settings
from app.tests.utils.model_utils import (
    create_random_account_dict,
    generate_random_account,
)


def test_create_account(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    account = create_random_account_dict()
    response = client.post(
        f"{settings.API_V1_STR}/accounts/",
        headers=superuser_token_headers,
        json=account,
    )
    assert response.status_code == 200
    content = response.json()
    assert "accountName" in content
    assert "isBanned" in content
    assert content["accountName"] == account["accountName"]
    assert content["isBanned"] == account["isBanned"]


def test_get_account(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["accountName"] == account.accountName
    assert content["isBanned"] == account.isBanned


def test_get_account_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/accounts/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert (
        content["detail"]
        == f"No object matching the query ({model.accountName.__str__} : {content["accountName"]}) in the table {model.__tablename__} was found."
    )


def test_get_account_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == f"Unauthorize API access for {account_api.get_account.__name__}"


def test_get_accounts(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    generate_random_account(db)
    generate_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/accounts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_account(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=superuser_token_headers,
        json=updated_account,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["accountName"] == updated_account["accountName"]
    assert content["isBanned"] == updated_account["isBanned"]


def test_update_account_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/accounts/999",
        headers=superuser_token_headers,
        json=updated_account,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"No object matching the query ({model.accountName.__str__} : {content["accountName"]}) in the table {model.__tablename__} was found."


def test_update_account_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    updated_account = create_random_account_dict()
    response = client.put(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=normal_user_token_headers,
        json=updated_account,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == f"Unauthorized API access for {account_api.update_account.__name__}"


def test_delete_account(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == f"Account with mapping ({model.accountName.__str__}: {content["accountName"]}) deleted successfully"


def test_delete_account_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == f"No object matching the query ({model.accountName.__str__}: {content["accountName"]}) in the table {model.__tablename__} was found."


def test_delete_account_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    account = generate_random_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/{account.accountName}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == f"Unauthorized API access for {account_api.delete_account.__name__}"
