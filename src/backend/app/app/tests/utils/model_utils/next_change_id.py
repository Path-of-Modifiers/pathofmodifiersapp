import asyncio
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import NextChangeId
from app.core.schemas.next_change_id import NextChangeIdCreate
from app.tests.utils.utils import random_lower_string


def create_random_next_change_id_dict() -> Dict:
    nextChangeId = random_lower_string()

    next_change_id = {
        "nextChangeId": nextChangeId,
    }

    return next_change_id


async def generate_random_next_change_id(db: Session) -> Tuple[Dict, NextChangeId]:
    next_change_id_dict = create_random_next_change_id_dict()
    next_change_id_create = NextChangeIdCreate(**next_change_id_dict)
    next_change_id = await crud.CRUD_nextChangeId.create(
        db, obj_in=next_change_id_create
    )

    return next_change_id_dict, next_change_id
