import asyncio
from typing import List
from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from backend.app.app.tests.utils.utils import random_lower_string
from backend.app.app.tests.utils.utils import random_bool
from backend.app.app.core.models.models import Account
from backend.app.app.core.schemas.account import AccountCreate


async def create_random_account(db: Session) -> Account:
    accountName = random_lower_string()
    isBanned = random_bool()

    account = AccountCreate(
        accountName=accountName,
        isBanned=isBanned,
    )

    return await crud.CRUD_account.create(db, obj_in=account)


async def create_random_account_list(db: Session, count: int = 10) -> List[Account]:
    accounts = [create_random_account(db) for _ in range(count)]
    return await asyncio.gather(*accounts)


async def get_random_account(session: Session) -> Account:
    # Use func.random() for databases that support it (e.g., PostgreSQL)
    # For SQLite, you can use func.random() as well. For MySQL, use func.rand()
    # It returns random number between 0 and 1
    random_account = session.query(Account).order_by(func.random()).first()

    if random_account:
        print(
            f"Found already existing account. random_account.accountName: {random_account.accountName}"
        )
    else:
        random_account = create_random_account(session)
    return random_account
