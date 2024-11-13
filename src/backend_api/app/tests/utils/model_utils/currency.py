from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency
from app.core.schemas import CurrencyCreate
from app.tests.utils.utils import (
    random_float,
    random_int,
    random_lower_string,
)


def create_random_currency_dict() -> dict:
    """Create a random currency dictionary.

    Returns:
        Dict: Currency dictionary with random values.
    """
    tradeName = random_lower_string()
    valueInChaos = random_float()
    createdHoursSinceLaunch = random_int(small_int=True)

    currency = {
        "tradeName": tradeName,
        "valueInChaos": valueInChaos,
        "createdHoursSinceLaunch": createdHoursSinceLaunch,
    }

    return currency


async def generate_random_currency(db: Session) -> tuple[dict, Currency]:
    """Generates a random currency.

    Args:
        db (Session): DB session.

    Returns:
        Tuple[Dict, Currency]: Random currency dict and Currency db object.
    """
    currency_dict = create_random_currency_dict()
    currency_create = CurrencyCreate(**currency_dict)
    currency = await crud.CRUD_currency.create(db, obj_in=currency_create)
    return currency_dict, currency
