import asyncio
from typing import Dict, Tuple, Optional, Union, List
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Stash, Account
from app.core.schemas.stash import StashCreate
from app.tests.utils.utils import random_lower_string, random_bool

from app.tests.utils.model_utils.account import generate_random_account


async def create_random_stash_dict(
    db: Session, retrieve_dependencies: bool
) -> Union[Dict, Tuple[Dict, Optional[List[Union[Dict, Account]]]]]:
    public = random_bool()
    league = random_lower_string()
    stashId = random_lower_string()

    account_dict, account = await generate_random_account(db)
    accountName = account.accountName

    stash = {
        "accountName": accountName,
        "public": public,
        "league": league,
        "stashId": stashId,
    }
    if not retrieve_dependencies:
        return stash
    else:
        return stash, [account_dict, account]


async def generate_random_stash(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Tuple[Dict, Stash, Optional[List[Union[Dict, Account]]]]:
    output = await create_random_stash_dict(
        db, retrieve_dependencies=retrieve_dependencies
    )
    if not retrieve_dependencies:
        stash_dict = output
    else:
        stash_dict, deps = output

    stash_create = StashCreate(**stash_dict)

    stash = await crud.CRUD_stash.create(db, obj_in=stash_create)

    if not retrieve_dependencies:
        return stash_dict, stash
    else:
        return stash_dict, stash, deps
