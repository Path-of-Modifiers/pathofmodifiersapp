import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemBaseType
from app.core.schemas.item_base_type import ItemBaseTypeCreate
from app.tests.utils.utils import random_lower_string


def create_random_item_base_type_dict() -> Dict:
    baseType = random_lower_string()
    category = random_lower_string()
    subCategory = random_lower_string()

    item_base_type = {
        "baseType": baseType,
        "category": category,
        "subCategory": subCategory,
    }

    return item_base_type


async def generate_random_item_base_type(db: Session) -> ItemBaseType:
    item_base_type = create_random_item_base_type_dict()
    item_base_type_create = ItemBaseTypeCreate(**item_base_type)
    item_base_type = await crud.CRUD_itemBaseType.create(
        db, obj_in=item_base_type_create
    )

    return item_base_type
