from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.modifier import ModifierUpdate
from backend.app.app.tests.utils.model_utils.modifier import create_random_modifier
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url