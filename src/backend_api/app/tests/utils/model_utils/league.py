from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import League
from app.core.schemas import LeagueCreate
from app.tests.utils.utils import (
    random_datetime,
    random_lower_string,
)


def create_random_league_dict() -> dict:
    """Create a random league dictionary.

    Returns:
        Dict: League dictionary with random values.
    """
    name = random_lower_string()
    validFrom = random_datetime()
    validTo = random_datetime(min_time=validFrom)

    league = {
        "name": name,
        "validFrom": validFrom,
        "validTo": validTo,
    }

    return league


async def generate_random_league(db: Session) -> tuple[dict, League]:
    """Generates a random league.

    Args:
        db (Session): DB session.

    Returns:
        Tuple[Dict, League]: Random league dict and League db object.
    """
    league_dict = create_random_league_dict()
    league_create = LeagueCreate(**league_dict)
    league = await crud.CRUD_league.create(db, obj_in=league_create)
    return league_dict, league
