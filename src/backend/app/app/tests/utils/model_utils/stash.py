import asyncio
from typing import List

from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Stash
from app.core.schemas.stash import StashCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_bool
from app.tests.utils.model_utils.account import get_random_account

async def create_random_stash(db: Session) -> Stash:
    account = await get_random_account(db)
    
    accountName = account.accountName
    public = random_bool()
    league = random_lower_string()
    stashId = random_lower_string()

    stash = StashCreate(
        accountName=accountName,
        public=public,
        league=league,
        stashId=stashId,
    )

    return await crud.CRUD_stash.create(db, obj_in=stash)


async def create_random_stash_list(db: Session, count: int = 10) -> List[Stash]:
    stashes = [create_random_stash(db) for _ in range(count)]
    return await asyncio.gather(*stashes)


async def get_random_stash(session: Session) -> Stash:
    random_stash = session.query(Stash).order_by(func.random()).first()

    if random_stash:
        print(
            f"Found already existing stash. random_stash.stashId: {random_stash.stashId}"
        )
    else:
        random_stash = create_random_stash(session)
    return random_stash