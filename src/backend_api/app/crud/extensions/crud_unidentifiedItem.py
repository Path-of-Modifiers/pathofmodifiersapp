from pydantic import TypeAdapter
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.models.models import UnidentifiedItem as model_UnidentifiedItem
from app.core.schemas.unidentified_item import (
    UnidentifiedItem,
    UnidentifiedItemCreate,
    UnidentifiedItemUpdate,
)
from app.crud.base import CRUDBase


class CRUDUnidentifiedItem(
    CRUDBase[
        model_UnidentifiedItem,
        UnidentifiedItem,
        UnidentifiedItemCreate,
        UnidentifiedItemUpdate,
    ]
):
    async def get_non_aggregated(self, db: Session) -> list[UnidentifiedItem]:
        """
        Returns the non aggregated unidentified items for the last 10 recorded hours
            (not necessarily the last 10 hours)
        """
        last_10_recorded_hours = (
            select(model_UnidentifiedItem.createdHoursSinceLaunch.distinct())
            .where(model_UnidentifiedItem.aggregated.isnot(True))
            .order_by(model_UnidentifiedItem.createdHoursSinceLaunch.desc())
            .limit(10)
        )
        stmt = select(model_UnidentifiedItem).where(
            model_UnidentifiedItem.createdHoursSinceLaunch.in_(last_10_recorded_hours),
            model_UnidentifiedItem.aggregated.isnot(True),
        )

        non_aggregated = db.execute(stmt).scalars().all()

        validate = TypeAdapter(list[UnidentifiedItem]).validate_python

        return validate(non_aggregated)

    async def add_aggregated(
        self, db: Session, aggregated_objs: list[UnidentifiedItemCreate]
    ) -> list[UnidentifiedItem]:
        last_10_recorded_hours = (
            select(model_UnidentifiedItem.createdHoursSinceLaunch.distinct())
            .where(model_UnidentifiedItem.aggregated.isnot(True))
            .order_by(model_UnidentifiedItem.createdHoursSinceLaunch.desc())
            .limit(10)
        )
        stmt = delete(model_UnidentifiedItem).where(
            model_UnidentifiedItem.createdHoursSinceLaunch.in_(last_10_recorded_hours),
            model_UnidentifiedItem.aggregated.isnot(True),
        )
        non_aggregated_objs = db.execute(stmt)

        await self.create(db, obj_in=aggregated_objs, return_nothing=True)

        return non_aggregated_objs
