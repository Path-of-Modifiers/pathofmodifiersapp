from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemBaseType
from app.tests.utils.utils import random_lower_string
from backend.app.app.core.schemas.item_base_type import ItemBaseTypeCreate


def create_random_item_base_type(db: Session) -> ItemBaseType:
    baseType = random_lower_string()
    category = random_lower_string()
    subCategory = random_lower_string()

    item_base_type = ItemBaseTypeCreate(
        baseType=baseType, category=category, subCategory=subCategory
    )

    return crud.CRUD_itemBaseType.create(db, obj_in=item_base_type)
