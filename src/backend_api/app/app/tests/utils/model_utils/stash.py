import asyncio
from typing import Dict, List, Optional, Tuple, Union
from sqlalchemy.orm import Session

from app import crud
from app.tests.conftest import db
from app.core.models.models import Account, Stash
from app.core.schemas.stash import StashCreate
from app.tests.utils.utils import random_lower_string, random_bool
from app.tests.utils.model_utils.account import generate_random_account


async def create_random_stash_dict(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Union[Dict, Tuple[Dict, List[Union[Dict, Account]]]]:
    stashId = random_lower_string()
    public: bool = random_bool()
    league = random_lower_string()

    account_dict, account = await generate_random_account(db)
    accountName = account.accountName

    stash = {
        "stashId": stashId,
        "accountName": accountName,
        "public": public,
        "league": league,
    }

    if not retrieve_dependencies:
        return stash
    else:
        deps = []
        deps += [account_dict, account]
        return stash, deps


async def generate_random_stash(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Tuple[Dict, Stash, Optional[List[Union[Dict, Account]]]]:
    output = await create_random_stash_dict(db, retrieve_dependencies)
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
