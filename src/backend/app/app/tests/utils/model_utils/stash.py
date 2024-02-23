from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Stash
from app.core.schemas.stash import StashCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.utils import random_int
from app.tests.utils.utils import random_bool
from app.tests.utils.utils import random_float
from app.tests.utils.utils import random_json



def create_random_stash(db: Session) -> Stash:
    accountName = random_lower_string()
    public = random_bool()
    league = random_lower_string()
    stashId = random_lower_string()

    stash = StashCreate(
        accountName=accountName,
        public=public,
        league=league,
        stashId=stashId,
    )

    return crud.CRUD_stash.create(db, obj_in=stash)