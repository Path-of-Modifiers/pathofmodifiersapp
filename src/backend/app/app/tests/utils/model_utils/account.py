from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_bool
from backend.app.app.core.models.models import Account
from backend.app.app.core.schemas.account import AccountCreate


def create_random_account(db: Session) -> Account:
    accountName = random_lower_string()
    isBanned = random_bool()

    account = AccountCreate(
        accountName=accountName,
        isBanned=isBanned,
    )

    return crud.CRUD_account.create(db, obj_in=account)