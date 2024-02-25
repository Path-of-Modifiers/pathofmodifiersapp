import asyncio
from typing import Dict
from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Modifier
from app.core.schemas.modifier import ModifierCreate
from app.tests.utils.utils import (
    random_lower_string,
    random_int,
    random_bool,
    random_float,
)


def create_random_modifier_dict() -> Dict:
    modifierId = random_int()
    position = random_int(small_int=True)
    static = random_bool()
    if not static:
        if random_bool():  # Random chance to choose numeric rolls or text rolls
            minRoll = random_float(small_float=True)
            maxRoll = random_float(small_float=True)
            if minRoll > maxRoll:
                minRoll, maxRoll = maxRoll, minRoll
            textRoll = None
        else:
            minRoll = None
            maxRoll = None
            textRoll = random_lower_string()
        effect = (
            random_lower_string() + "#"
        )  # "#" is required if the modifier is not static
        regex = random_lower_string()
    else:
        minRoll = None
        maxRoll = None
        textRoll = None
        effect = random_lower_string()
        regex = None

    implicit = random_bool()
    explicit = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesized = random_bool()
    corrupted = random_bool()
    enchanted = random_bool()
    veiled = random_bool()

    modifier_dict = {
        "modifierId": modifierId,
        "position": position,
        "minRoll": minRoll,
        "maxRoll": maxRoll,
        "textRoll": textRoll,
        "static": static,
        "effect": effect,
        "regex": regex,
        "implicit": implicit,
        "explicit": explicit,
        "delve": delve,
        "fractured": fractured,
        "synthesized": synthesized,
        "corrupted": corrupted,
        "enchanted": enchanted,
        "veiled": veiled,
    }

    return modifier_dict


async def generate_random_modifier(db: Session) -> Modifier:
    modifier_dict = await create_random_modifier_dict()
    modifier_create = ModifierCreate(**modifier_dict)
    modifier = await crud.CRUD_modifier.create(db, obj_in=modifier_create)
    return modifier_dict, modifier
