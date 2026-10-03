from datetime import datetime

from backend_api.app.core.models.models import League as model_League
from backend_api.app.core.schemas.league import (
    League,
    LeagueCreate,
    LeagueUpdate,
)
from backend_api.app.crud.base import CRUDBase
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session


class CRUDLeague(CRUDBase[model_League, League, LeagueCreate, LeagueUpdate]):
    def __init__(self):
        super().__init__(model=model_League, schema=League, create_schema=LeagueCreate)

    async def get_active_leagues(self, db: Session) -> list[League]:
        now = datetime.now()

        stmt = select(model_League).where(
            model_League.validFrom <= now,
            model_League.validTo.is_(None) | (model_League.validTo >= now),
        )

        leagues = db.execute(stmt).scalars().all()

        validate = TypeAdapter(list[League]).validate_python

        return validate(leagues)
