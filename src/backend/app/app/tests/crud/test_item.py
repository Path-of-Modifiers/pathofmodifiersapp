from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.item import ItemUpdate
from backend.app.app.tests.utils.model_utils.item import create_random_item
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url