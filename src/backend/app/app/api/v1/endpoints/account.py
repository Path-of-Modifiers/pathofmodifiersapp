from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.deps import get_db

import app.api.deps as deps

from app.crud import CRUD_account

import app.core.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.get(
    "/{accountName}",
    response_model=Union[schemas.Account, List[schemas.Account]],
)
async def get_account(accountName: str, db: Session = Depends(get_db)):
    """
    Get account by "accountName".
    """
    account_map = {"accountName": accountName}
    account = await CRUD_account.get(db=db, filter=account_map)

    return account


@router.get("/", response_model=Union[schemas.Account, List[schemas.Account]])
async def get_all_accounts(db: Session = Depends(get_db)):
    """
    Get all accounts.
    """
    all_accounts = await CRUD_account.get(db=db)

    return all_accounts


@router.post(
    "/",
    response_model=Union[schemas.AccountCreate, List[schemas.AccountCreate]],
)
async def create_account(
    account: Union[schemas.AccountCreate, List[schemas.AccountCreate]],
    db: Session = Depends(get_db),
):
    """
    Create a new account.
    """
    return await CRUD_account.create(db=db, obj_in=account)


@router.put("/{accountName}", response_model=schemas.Account)
async def update_account(
    accountName: str,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update an account by "accountName".
    """
    account_map = {"accountName": accountName}
    account = await CRUD_account.get(
        db=db,
        filter=account_map,
    )

    return await CRUD_account.update(db_obj=account, obj_in=account_update, db=db)


@router.delete("/{accountName}", response_model=str)
async def delete_account(accountName: str, db: Session = Depends(get_db)):
    """
    Delete an account by "accountName".
    """
    account_map = {"accountName": accountName}
    await CRUD_account.remove(db=db, filter=account_map)

    return f"Account with mapping ({account_map}) deleted successfully"
