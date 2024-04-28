import asyncio
from typing import Dict, Tuple, Optional, List, Union
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Item, Account, Currency, ItemBaseType
from app.core.schemas.item import ItemCreate
from app.tests.utils.utils import (
    random_lower_string,
    random_int,
    random_bool,
    random_float,
    random_json,
    random_url,
)

from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type
from app.tests.utils.model_utils.currency import generate_random_currency


async def create_random_item_dict(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Union[
    Dict, Tuple[Dict, List[Union[Dict, Account, ItemBaseType, Currency]]]
]:
    gameItemId = random_lower_string()
    changeId = random_lower_string()
    name = random_lower_string()
    iconUrl = random_url()
    league = random_lower_string()
    typeLine = random_lower_string()
    rarity = random_lower_string()
    identified = random_bool()
    ilvl = random_int(small_int=True)
    forumNote = random_lower_string()
    currencyAmount = random_float(small_float=True)
    corrupted = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesized = random_bool()
    replica = random_bool()
    elder = random_bool()
    shaper = random_bool()
    influences_type_dict = {
        "shaper": "bool",
        "elder": "bool",
        "crusader": "bool",
        "hunter": "bool",
    }
    influences = random_json(influences_type_dict)
    searing = random_bool()
    tangled = random_bool()
    isRelic = random_bool()
    prefixes = random_int(small_int=True)
    suffixes = random_int(small_int=True)
    foilVariation = random_int(small_int=True)

    item_base_type_dict, item_base_type = await generate_random_item_base_type(db)
    baseType = item_base_type.baseType
    currency_dict, currency = await generate_random_currency(db)
    currencyId = currency.currencyId

    item = {
        "gameItemId": gameItemId,
        "changeId": changeId,  
        "name": name,
        "iconUrl": iconUrl,
        "league": league,
        "typeLine": typeLine,
        "baseType": baseType,
        "rarity": rarity,
        "identified": identified,
        "ilvl": ilvl,
        "forumNote": forumNote,
        "currencyAmount": currencyAmount,
        "currencyId": currencyId,
        "corrupted": corrupted,
        "delve": delve,
        "fractured": fractured,
        "synthesized": synthesized,
        "replica": replica,
        "elder": elder,
        "shaper": shaper,
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
    else:
        deps += [item_base_type_dict, item_base_type]
        deps += [currency_dict, currency]
        return item, deps


async def generate_random_item(
    db: Session, retrieve_dependencies: Optional[bool] = False
) -> Tuple[
    Dict, Item, Optional[List[Union[Dict, Account, ItemBaseType, Currency]]]
]:
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