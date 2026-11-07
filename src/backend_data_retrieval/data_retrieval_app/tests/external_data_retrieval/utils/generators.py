import random
import uuid
from math import floor

from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)


def make_id() -> str:
    return str(uuid.uuid4())


def make_valid_note(
    *, price: int | None = None, rng: random.Random | None = None
) -> str:
    if rng is None:
        rng = random.Random()

    if price is None:
        price = max(
            1,
            floor(
                rng.gauss(
                    script_settings.MEAN_ITEM_PRICE,
                    sigma=script_settings.STD_ITEM_PRICE,
                )
            ),
        )

    currency = rng.choice(script_settings.ITEM_NOTE_CURRENCY_TYPES)

    return f"~b/o {price} {currency}"


def make_random_league(rng: random.Random | None = None) -> str:
    if rng is None:
        rng = random.Random()

    return rng.choice(script_settings.LEAGUES)
