from app import crud
from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Item
from app.core.schemas.item import ItemCreate
from app.tests.utils.utils import random_lower_string


def create_random_item(db: Session) -> Item:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, id=id)
    return crud.Item.create(db=db, obj_in=item_in)

