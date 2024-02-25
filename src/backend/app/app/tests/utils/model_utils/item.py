import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Item
from app.core.schemas.item import ItemCreate
from app.tests.utils.utils import (
    random_lower_string,
    random_int,
    random_bool,
    random_float,
    random_json,
    random_url,
)

from app.tests.utils.model_utils.stash import generate_random_stash
from app.tests.utils.model_utils.item_base_type import generate_random_item_base_type
from app.tests.utils.model_utils.currency import generate_random_currency


async def create_random_item_dict(db: Session) -> Dict:
    gameItemId = random_lower_string()
    name = random_lower_string()
    iconUrl = random_url()
    league = random_lower_string()
    typeLine = random_lower_string()
    rarity = random_lower_string()
    identified = random_bool()
    itemLevel = random_int(small_int=True)
    forumNote = random_lower_string()
    currencyAmount = random_float()
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
    foilVariation = random_int()
    inventoryId = random_lower_string()

    stash = await generate_random_stash(db)
    stashId = stash.stashId
    item_base_type = await generate_random_item_base_type(db)
    baseType = item_base_type.baseType
    currency = await generate_random_currency(db)
    currencyId = currency.currencyId

    item = {
        "gameItemId": gameItemId,
        "stashId": stashId,
        "name": name,
        "iconUrl": iconUrl,
        "league": league,
        "typeLine": typeLine,
        "baseType": baseType,
        "rarity": rarity,
        "identified": identified,
        "itemLevel": itemLevel,
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
        "inventoryId": inventoryId,
    }

    return item


async def generate_random_item(db: Session) -> Item:
    item_dict = await create_random_item_dict()
    item_create = ItemCreate(**item_dict)
    item = await crud.CRUD_item.create(db, obj_in=item_create)
    return item_dict, item
