import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Stash
from app.core.schemas.stash import StashCreate
from app.tests.utils.utils import random_lower_string, random_bool

from account import generate_random_account


async def create_random_stash_dict(db: Session) -> Dict:
    account = generate_random_account(db)

    accountName = account.accountName
    public = random_bool()
    league = random_lower_string()
    stashId = random_lower_string()

    stash = {
        "accountName": accountName,
        "public": public,
        "league": league,
        "stashId": stashId,
    }

    return stash


async def generate_random_stash(db: Session) -> Stash:
    stash_dict = create_random_stash_dict(db)
    stash_create = StashCreate(**stash_dict)

    stash = await crud.CRUD_stash.create(db, obj_in=stash_create)
    return stash_dict, stash
