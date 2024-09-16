from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.api_message_util import (
    get_delete_return_msg,
)
from app.api.deps import (
    get_current_active_superuser,
    get_db,
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
async def get_account(accountName: str, db: Session = Depends(get_db)):
    """
    Get the account by filter with key and value for "accountName" .

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
    db: Session = Depends(get_db),
):
    """
    Get all accounts.

    Returns a list of all accounts.
    """
    all_accounts = await CRUD_account.get(db=db)

    return all_accounts


@router.post(
    "/",
    response_model=schemas.AccountCreate | list[schemas.AccountCreate] | None,
    dependencies=[
        Depends(get_current_active_superuser),
    ],
)
async def create_account(
    account: schemas.AccountCreate | list[schemas.AccountCreate],
    on_duplicate_pkey_do_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create one or a list of accounts.

    Returns the created account or list of accounts.
    """

    return await CRUD_account.create(
        db=db, obj_in=account, on_duplicate_pkey_do_nothing=on_duplicate_pkey_do_nothing
    )


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
    db: Session = Depends(get_db),
):
    """
    Update an account by key and value for "accountName".

    Returns the updated account.
    """
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
async def delete_account(accountName: str, db: Session = Depends(get_db)):
    """
    Delete an account by key and value "accountName".

    Returns a message indicating the account was deleted.
    Always deletes one account.
    """

    account_map = {"accountName": accountName}
    await CRUD_account.remove(db=db, filter=account_map)

    return get_delete_return_msg(
        model_table_name=Account.__tablename__, filter=account_map
    ).message
