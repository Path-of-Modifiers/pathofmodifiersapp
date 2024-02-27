import asyncio
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemModifier
from app.core.schemas.item_modifier import ItemModifierCreate
from app.tests.utils.utils import random_int, random_float

from app.tests.utils.model_utils.item import generate_random_item
from app.tests.utils.model_utils.modifier import generate_random_modifier


async def create_random_item_modifier_dict(db: Session) -> Dict:
    range_value = random_float()

    _, item = await generate_random_item(db)
    itemId = item.itemId
    _, modifier = await generate_random_modifier(db)
    modifierId = modifier.modifierId
    position = modifier.position

    item_modifier_dict = {
        "itemId": itemId,
        "modifierId": modifierId,
        "position": position,
        "range": range_value,
    }
    return item_modifier_dict


async def generate_random_item_modifier(db: Session) -> Tuple[Dict, ItemModifier]:
    item_modifier_dict = await create_random_item_modifier_dict(db)
    item_modifier_create = ItemModifierCreate(**item_modifier_dict)
    item_modifier = await crud.CRUD_itemModifier.create(db, obj_in=item_modifier_create)
    return item_modifier_dict, item_modifier
