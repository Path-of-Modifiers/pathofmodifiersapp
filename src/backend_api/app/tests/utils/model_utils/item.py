from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Currency, Item, ItemBaseType
from app.core.schemas.item import ItemCreate
from app.tests.utils.model_utils.currency import generate_random_currency
from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type
from app.tests.utils.utils import (
    random_bool,
    random_float,
    random_int,
    random_json,
    random_lower_string,
)


async def create_random_item_dict(
    db: Session, retrieve_dependencies: bool | None = False
) -> dict | tuple[dict, list[dict | ItemBaseType | Currency]]:
    """Create a random item dictionary.

    Args:
        db (Session): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Union[ Dict, Tuple[ Dict, List[ Union[ Dict, ItemBaseType, Currency, ] ], ], ]: \n
        Random item dictionary or tuple with random item dictionary and dependencies.
    """
    name = random_lower_string()
    league = random_lower_string()
    typeLine = random_lower_string()
    ilvl = random_int(small_int=True)
    rarity = random_lower_string()
    identified = random_bool()
    currencyAmount = random_float(small_float=True)
    corrupted = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesised = random_bool()
    replica = random_bool()
    influences_type_dict = {
        "elder": "bool",
        "shaper": "bool",
        "crusader": "bool",
        "redeemer": "bool",
        "hunter": "bool",
        "warlord": "bool",
    }
    influences = random_json(influences_type_dict)
    searing = random_bool()
    tangled = random_bool()
    isRelic = random_bool()
    prefixes = random_int(small_int=True)
    suffixes = random_int(small_int=True)
    foilVariation = random_int(small_int=True)
    createdHoursSinceLaunch = random_int(small_int=True)

    item_base_type_dict, item_base_type = await generate_random_item_base_type(db)
    itemBaseTypeId = item_base_type.itemBaseTypeId
    currency_dict, currency = await generate_random_currency(db)
    currencyId = currency.currencyId

    item = {
        "name": name,
        "league": league,
        "itemBaseTypeId": itemBaseTypeId,
        "createdHoursSinceLaunch": createdHoursSinceLaunch,
        "typeLine": typeLine,
        "ilvl": ilvl,
        "rarity": rarity,
        "identified": identified,
        "currencyAmount": currencyAmount,
        "currencyId": currencyId,
        "corrupted": corrupted,
        "delve": delve,
        "fractured": fractured,
        "synthesised": synthesised,
        "replica": replica,
        "influences": influences,
        "searing": searing,
        "tangled": tangled,
        "isRelic": isRelic,
        "prefixes": prefixes,
        "suffixes": suffixes,
        "foilVariation": foilVariation,
    }

    if not retrieve_dependencies:
        return item
    else:  # Gather dependencies and return
        deps = []
        deps += [item_base_type_dict, item_base_type]
        deps += [currency_dict, currency]
        return item, deps


async def generate_random_item(
    db: Session, retrieve_dependencies: bool | None = False
) -> tuple[
    dict,
    Item,
    list[dict | ItemBaseType | Currency] | None,
]:
    """Generate a random item.

    Args:
        db (Session): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Tuple[ Dict, Item,  List[ Union[ Dict, ItemBaseType, Currency, ] ] ], ]: \n
        Random item dict and Item db object and optional dependencies.
    """
    output = await create_random_item_dict(db, retrieve_dependencies)
    if not retrieve_dependencies:
        item_dict = output
    else:
        item_dict, deps = output
    item_create = ItemCreate(**item_dict)
    item = await crud.CRUD_item.create(db, obj_in=item_create)

    if not retrieve_dependencies:
        return item_dict, item
    else:
        return item_dict, item, deps
