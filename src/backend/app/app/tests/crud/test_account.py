from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.account import Account, AccountCreate, AccountUpdate
from app import crud
from backend.app.app.tests.utils.model_utils.account import create_random_account
from backend.app.app.tests.utils.utils import random_lower_string



async def test_create_account(db: Session) -> None:
    account = await create_random_account(db)
    assert account.accountName == account.accountName
    assert account.isBanned == account.isBanned
    
    
async def test_get_account(db: Session) -> None:
    account = await create_random_account(db)
    account_name_map = {"accountName": account.accountName}
    stored_account = await crud.CRUD_account.get(db, filter=account_name_map)
    assert stored_account
    assert account.accountName == stored_account.accountName
    assert account.isBanned == stored_account.isBanned
    
    
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
    assert account.accountName == deleted_account.accountName
    assert account.isBanned == deleted_account.isBanned