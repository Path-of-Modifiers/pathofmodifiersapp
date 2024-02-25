import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Account
from app.core.schemas.account import AccountCreate
from utils import random_lower_string, random_bool


def create_random_account_dict() -> Dict:
    accountName = random_lower_string()
    isBanned = random_bool()

    account = {
        "accountName": accountName,
        "isBanned": isBanned,
    }

    return account


async def generate_random_account(db: Session) -> Account:
    account_dict = create_random_account_dict()
    account_create = AccountCreate(**account_dict)
    account = await crud.CRUD_account.create(db, obj_in=account_create)
    return account
