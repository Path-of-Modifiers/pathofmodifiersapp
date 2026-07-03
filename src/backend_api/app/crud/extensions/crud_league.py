from datetime import datetime

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models.models import League as model_League
from app.core.schemas.league import (
    League,
    LeagueCreate,
    LeagueUpdate,
)
from app.crud.base import CRUDBase


class CRUDLeague(CRUDBase[model_League, League, LeagueCreate, LeagueUpdate]):
    async def get_active_leagues(self, db: Session) -> list[str]:
        now = datetime.now()

        stmt = select(model_League.name).where(
            model_League.validFrom <= now,
            model_League.validTo.is_(None) | (model_League.validTo >= now),
        )

        leagues = db.execute(stmt).mappings().all()

        validate = TypeAdapter(list[str]).validate_python

        return validate(leagues)
