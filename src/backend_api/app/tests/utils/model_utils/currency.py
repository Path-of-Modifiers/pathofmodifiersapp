from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency, League
from app.core.schemas import CurrencyCreate
from app.tests.utils.model_utils.league import generate_random_league
from app.tests.utils.utils import (
    random_float,
    random_int,
    random_lower_string,
)


async def create_random_currency_dict(
    db: Session, retrieve_dependencies: bool | None = False
) -> dict | tuple[dict, list[dict | League]]:
    """Create a random currency dictionary.

    Args:
        db (Session): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Union[ Dict, Tuple[ Dict, List[ Union[ Dict, League] ], ], ]: \n
        Random Currency dictionary or tuple with random Currency dictionary and dependencies.
    """
    tradeName = random_lower_string()
    valueInChaos = random_float()
    createdHoursSinceLaunch = random_int(small_int=True)

    league_dict, league = await generate_random_league(db)
    leagueId = league.leagueId

    currency = {
        "tradeName": tradeName,
        "valueInChaos": valueInChaos,
        "createdHoursSinceLaunch": createdHoursSinceLaunch,
        "leagueId": leagueId,
    }
    if not retrieve_dependencies:
        return currency
    else:
        deps = []
        deps += [league_dict, league]
        return currency, deps


async def generate_random_currency(
    db: Session, retrieve_dependencies: bool | None = False
) -> tuple[dict, Currency, list[dict | League] | None]:
    """Generates a random currency.

    Args:
        db (Session): DB session.

    Returns:
        Tuple[ Dict, Currency,  List[ Union[ Dict, League, ] ] ], ]: \n
        Random currency dict and Currency db object and optional dependencies.
    """
    output = await create_random_currency_dict(db, retrieve_dependencies)
    if not retrieve_dependencies:
        currency_dict = output
    else:
        currency_dict, deps = output
    currency_create = CurrencyCreate(**currency_dict)
    currency = await crud.CRUD_currency.create(db, obj_in=currency_create)

    if not retrieve_dependencies:
        return currency_dict, currency
    else:
        return currency_dict, currency, deps
