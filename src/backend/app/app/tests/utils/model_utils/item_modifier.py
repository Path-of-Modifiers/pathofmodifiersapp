from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemModifier
from app.core.schemas.item_modifier import ItemModifierCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_int
from app.tests.utils.utils import random_bool
from app.tests.utils.utils import random_float
from app.tests.utils.utils import random_json


def create_random_item_modifier(db: Session) -> ItemModifier:
    itemId = random_int()
    gameItemId = random_lower_string()
    modifierId = random_int()
    position = random_int()
    range_value = random_int()

    item_modifier = ItemModifierCreate(
        itemId=itemId,
        gameItemId=gameItemId,
        modifierId=modifierId,
        position=position,
        range=range_value,
    )