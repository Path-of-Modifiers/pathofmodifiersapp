from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Modifier
from app.core.schemas.modifier import ModifierCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_int
from app.tests.utils.utils import random_bool
from app.tests.utils.utils import random_float
from app.tests.utils.utils import random_json


def create_random_modifier(db: Session) -> Modifier:
    modifierId = random_int()
    position = random_int()
    minRoll = random_int()
    maxRoll = random_int()
    textRoll = random_lower_string()
    static = random_bool()
    effect = random_lower_string()
    regex = random_lower_string()
    implicit = random_bool()
    explicit = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesized = random_bool()
    corrupted = random_bool()
    enchanted = random_bool()
    veiled = random_bool()

    modifier = Modifier(
        modifierId=modifierId,
        position=position,
        minRoll=minRoll,
        maxRoll=maxRoll,
        textRoll=textRoll,
        static=static,
        effect=effect,
        regex=regex,
        implicit=implicit,
        explicit=explicit,
        delve=delve,
        fractured=fractured,
        synthesized=synthesized,
        corrupted=corrupted,
        enchanted=enchanted,
        veiled=veiled,
    )

    return crud.CRUD_modifier.create(db, obj_in=modifier)
