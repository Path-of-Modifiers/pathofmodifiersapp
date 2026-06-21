from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import func, select
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
            func.min(model_Modifier.effect).label("effect"),
            func.coalesce(
                func.min(model_Modifier.regex),
                func.min(model_Modifier.effect),
            ).label("regex"),
            func.min(model_Modifier.relatedUniques).label("relatedUniques"),
            func.bool_or(model_Modifier.static).label("static"),
            func.json_build_object(
                "position",
                func.json_agg(model_Modifier.position),
                "textRolls",
                func.json_agg(model_Modifier.textRolls),
            ).label("groupedModifierProperties"),
        ).group_by(model_Modifier.modifierId)

        grouped_modifier_by_effect_record = db.execute(stmt).mappings().all()

        if not grouped_modifier_by_effect_record:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        validate = TypeAdapter(
            GroupedModifierByEffect | list[GroupedModifierByEffect]
        ).validate_python

        return validate(grouped_modifier_by_effect_record)
