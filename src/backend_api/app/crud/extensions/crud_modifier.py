import pandas as pd
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models.models import Modifier as model_Modifier
from app.core.schemas.modifier import (
    GroupedModifierByEffect,
    Modifier,
    ModifierCreate,
    ModifierUpdate,
)
from app.crud.base import CRUDBase


class CRUDModifier(
    CRUDBase[
        model_Modifier,
        Modifier,
        ModifierCreate,
        ModifierUpdate,
    ]
):
    async def get_grouped_modifier_by_effect(self, db: Session):
        stmt = select(
            model_Modifier.modifierId,
            model_Modifier.effect,
            model_Modifier.textRolls,
            model_Modifier.relatedUniques,
            model_Modifier.static,
        )
        db_obj = db.execute(stmt).mappings().all()

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        modifiers_df = pd.DataFrame(db_obj)

        grouped_modifier_df = modifiers_df.groupby("effect", as_index=False).agg(
            lambda x: list(x)
        )

        grouped_modifier_record = grouped_modifier_df.to_dict("records")

        validate = TypeAdapter(
            GroupedModifierByEffect | list[GroupedModifierByEffect]
        ).validate_python

        return validate(grouped_modifier_record)
