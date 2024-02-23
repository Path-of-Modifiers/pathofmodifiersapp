from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.item_modifier import ItemModifierUpdate
from backend.app.app.tests.utils.model_utils.item_modifier import ItemModifier
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url