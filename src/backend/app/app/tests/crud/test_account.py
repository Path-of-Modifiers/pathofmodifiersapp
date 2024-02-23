from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.account import AccountUpdate
from backend.app.app.tests.utils.model_utils.account import (
    create_random_account,
    create_random_account_list,
)
from backend.app.app.tests.utils.utils import random_bool, random_lower_string


async def test_create_account(db: Session) -> None:
    account = await create_random_account(db)
    stored_created_account = await crud.CRUD_account.create(db, obj_in=account)
    assert stored_created_account
    assert stored_created_account.accountName == account.accountName
    assert stored_created_account.isBanned == account.isBanned


async def test_get_account(db: Session) -> None:
    account = await create_random_account(db)
    account_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_map)
    assert stored_account
    assert stored_account.accountName == account.accountName
    assert stored_account.isBanned == account.isBanned


async def test_create_multiple_accounts(db: Session) -> None:
    accounts = await create_random_account_list(db=db, count=5)
    stored_accounts = await crud.CRUD_account.get(db)
    assert len(stored_accounts) == 5
    for stored_account in stored_accounts:
        assert stored_account in accounts


async def test_get_all_account(db: Session) -> None:
    account = await create_random_account(db)
    account_name_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_name_map)
    assert stored_account
    all_accounts = await crud.CRUD_account.get(db)
    assert stored_account in all_accounts


async def test_update_account(db: Session) -> None:
    account = await create_random_account(db)
    account_name_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_name_map)
    random_account_name = random_lower_string()
    account_update = AccountUpdate(accountName=random_account_name, isBanned=True)
    updated_account = await crud.CRUD_account.update(
        db, db_obj=stored_account, obj_in=account_update
    )
    assert updated_account
    assert updated_account.accountName == random_account_name
    assert updated_account.isBanned == True


async def test_delete_account(db: Session) -> None:
    account = await create_random_account(db)
    account_name_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_name_map)
    deleted_account = await crud.CRUD_account.remove(db, filter=account_name_map)
    account_name_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_name_map)
    assert stored_account is None
    assert deleted_account
    assert deleted_account.accountName == account.accountName
    assert deleted_account.isBanned == account.isBanned
