import asyncio
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency
from app.core.schemas import CurrencyCreate
from app.tests.utils.utils import random_lower_string, random_float, random_url


def create_random_currency_dict() -> Dict:
    """Create a random currency dictionary.

    Returns:
        Dict: Currency dictionary with random values.
    """
    tradeName = random_lower_string()
    valueInChaos = random_float()
    iconUrl = random_url()

    currency = {
        "tradeName": tradeName,
        "valueInChaos": valueInChaos,
        "iconUrl": iconUrl,
    }

    return currency


async def generate_random_currency(db: Session) -> Tuple[Dict, Currency]:
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
