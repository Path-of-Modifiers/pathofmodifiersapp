import asyncio
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Account
from app.core.schemas.account import AccountCreate
from app.tests.utils.utils import random_lower_string, random_bool


def create_random_account_dict() -> Dict:
    """Create a random account dictionary.

    Returns:
        Dict: Account dictionary with random values.
    """

    accountName = random_lower_string()
    isBanned = random_bool()

    account = {
        "accountName": accountName,
        "isBanned": isBanned,
    }

    return account


async def generate_random_account(db: Session) -> Tuple[Dict, Account]:
    """Generates a random account.

    Args:
        db (Session): DB session.

    Returns:
        Tuple[Dict, Account]: Random account dictionary and Account db object.
    """

    account_dict = create_random_account_dict()
    account_create = AccountCreate(**account_dict)
    account = await crud.CRUD_account.create(db, obj_in=account_create)
    return account_dict, account
