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
        Returns the non aggregated unidentified items
        """
        stmt = select(model_UnidentifiedItem).where(
            model_UnidentifiedItem.aggregated.isnot(True),
        )

        non_aggregated = db.execute(stmt).scalars().all()

        validate = TypeAdapter(list[UnidentifiedItem]).validate_python

        return validate(non_aggregated)

    async def add_aggregated(
        self, db: Session, aggregated_objs: list[UnidentifiedItemCreate]
    ):
        stmt = delete(model_UnidentifiedItem).where(
            model_UnidentifiedItem.aggregated.isnot(True),
        )
        db.execute(stmt)

        await self.create(db, obj_in=aggregated_objs, return_nothing=True)
