import asyncio
from typing import List

from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemBaseType
from backend.app.app.tests.utils.utils import random_lower_string
from backend.app.app.core.schemas.item_base_type import ItemBaseTypeCreate


async def create_random_itemBaseType(db: Session) -> ItemBaseType:
    baseType = random_lower_string()
    category = random_lower_string()
    subCategory = random_lower_string()

    item_base_type = ItemBaseTypeCreate(
        baseType=baseType, category=category, subCategory=subCategory
    )

    return await crud.CRUD_itemBaseType.create(db, obj_in=item_base_type)


async def create_random_itemBaseType_list(
    db: Session, count: int = 10
) -> List[ItemBaseType]:
    itemBaseTypes = [create_random_itemBaseType(db) for _ in range(count)]
    return await asyncio.gather(*itemBaseTypes)


async def get_random_itemBaseType(session: Session) -> ItemBaseType:
    random_itemBaseType = session.query(ItemBaseType).order_by(func.random()).first()

    if random_itemBaseType:
        print(
            f"Found already existing itemBaseType. random_itemBaseType.baseType: {random_itemBaseType.baseType}"
        )
    else:
        random_itemBaseType = create_random_itemBaseType(session)
    return random_itemBaseType
