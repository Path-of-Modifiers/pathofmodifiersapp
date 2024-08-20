from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_db_obj_already_exists_msg,
    get_delete_return_msg,
)
from app.api.deps import (
    SessionDep,
    get_current_active_superuser,
)
from app.core.models.models import Account
from app.crud import CRUD_account

router = APIRouter()


account_prefix = "account"


@router.get(
    "/{accountName}",
    response_model=schemas.Account,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_account(accountName: str, db: SessionDep):
    """
    Get the account by mapping with key and value for "accountName" .

    Always returns one account.
    """

    account_map = {"accountName": accountName}
    account = await CRUD_account.get(db=db, filter=account_map)

    return account


@router.get(
    "/",
    response_model=schemas.Account | list[schemas.Account],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def get_all_accounts(
    db: SessionDep,
):
    """
    Get all accounts.

    Returns a list of all accounts.
    """
    all_accounts = await CRUD_account.get(db=db)

    return all_accounts


@router.post(
    "/",
    response_model=schemas.AccountCreate | list[schemas.AccountCreate],
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_account(
    account: schemas.AccountCreate | list[schemas.AccountCreate],
    db: SessionDep,
):
    """
    Create one or a list of accounts.

    Returns the created account or list of accounts.
    """
    db_account = db.get(Account, account.accountName)
    if db_account:
        raise HTTPException(
            status_code=400,
            detail=get_db_obj_already_exists_msg(
                account_prefix, account.accountName
            ).message,
        )

    return await CRUD_account.create(db=db, obj_in=account)


@router.put(
    "/{accountName}",
    response_model=schemas.Account,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def update_account(
    accountName: str,
    account_update: schemas.AccountUpdate,
    db: SessionDep,
):
    """
    Update an account by key and value for "accountName".

    Returns the updated account.
    """
    db_account_update = db.get(Account, account_update.accountName)
    if db_account_update and db_account_update.accountName != accountName:
        raise HTTPException(
            status_code=400,
            detail=get_db_obj_already_exists_msg(
                account_prefix, account_update.accountName
            ).message,
        )

    account_map = {"accountName": accountName}
    account = await CRUD_account.get(
        db=db,
        filter=account_map,
    )

    return await CRUD_account.update(db_obj=account, obj_in=account_update, db=db)


@router.delete(
    "/{accountName}",
    response_model=str,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def delete_account(accountName: str, db: SessionDep):
    """
    Delete an account by key and value "accountName".

    Returns a message indicating the account was deleted.
    Always deletes one account.
    """

    account_map = {"accountName": accountName}
    await CRUD_account.remove(db=db, filter=account_map)

    return get_delete_return_msg(
        model_table_name=Account.__tablename__, mapping=account_map
    ).message
