from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.models.models import Account, Stash
from app.core.schemas.stash import StashCreate
from app.tests.utils.model_utils.account import generate_random_account
from app.tests.utils.utils import random_bool, random_lower_string


async def create_random_stash_dict(
    db: AsyncSession, retrieve_dependencies: bool | None = False
) -> dict | tuple[dict, list[dict | Account]]:
    """Create a random stash dictionary.

    Args:
        db (AsyncSession): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Union[Dict, Tuple[Dict, List[Union[Dict, Account]]]]: \n
        Random stash dictionary or tuple with random stash dictionary and dependencies.
    """
    stashId = random_lower_string()
    public: bool = random_bool()
    league = random_lower_string()

    # Set the dependencies
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
    else:  # Gather dependencies and return them
        deps = []
        deps += [account_dict, account]
        return stash, deps


async def generate_random_stash(
    db: AsyncSession, retrieve_dependencies: bool | None = False
) -> tuple[dict, Stash, list[dict | Account] | None]:
    """Generates a random stash.

    Args:
        db (AsyncSession): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Tuple[Dict, Stash, List[Union[Dict, Account]]]]: \n
        Random stash dictionary, Stash db object and dependencies.
    """
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
