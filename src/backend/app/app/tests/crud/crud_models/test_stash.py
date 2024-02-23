from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.stash import StashUpdate
from backend.app.app.tests.utils.model_utils.stash import create_random_stash
from backend.app.app.tests.utils.utils import random_float, random_lower_string, random_url