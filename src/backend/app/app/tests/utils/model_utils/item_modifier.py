import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemModifier
from app.core.schemas.item_modifier import ItemModifierCreate
from app.tests.utils.utils import random_int

from item import generate_random_item
from modifier import generate_random_modifier


async def create_random_item_modifier_dict(db: Session) -> Dict:
    range_value = random_int()

    item = await generate_random_item(db)
    itemId = item.itemId
    gameItemId = item.gameItemId
    modifier = await generate_random_modifier(db)
    modifierId = modifier.modifierId
    position = modifier.position

    item_modifier_dict = {
        "itemId": itemId,
        "gameItemId": gameItemId,
        "modifierId": modifierId,
        "position": position,
        "range_value": range_value,
    }
    return item_modifier_dict


async def generate_random_item_modifier(db: Session) -> ItemModifier:
    item_modifier_dict = create_random_item_modifier_dict()
    item_modifier_create = ItemModifierCreate(**item_modifier_dict)
    item_modifier = await crud.CRUD_item_modifier.create(
        db, obj_in=item_modifier_create
    )
    return item_modifier_dict, item_modifier
