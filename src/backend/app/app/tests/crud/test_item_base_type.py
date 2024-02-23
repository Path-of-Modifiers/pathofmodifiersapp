from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.item_base_type import ItemBaseTypeUpdate
from backend.app.app.tests.utils.model_utils.item_base_type import create_random_itemBaseType
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url