from typing import Any, List, Union

from fastapi import HTTPException
from pydantic import TypeAdapter

from sqlalchemy.orm import Session
from sqlalchemy import Column, select
from sqlalchemy import func
from sqlalchemy import String, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.schemas.modifier import (
    ModifierCreate,
    ModifierUpdate,
    Modifier,
    GroupedModifierByEffect,
)
from app.core.models.models import Modifier as model_Modifier
from app.crud.base import CRUDBase, SchemaType


class CRUDModifier(
    CRUDBase[
        model_Modifier,
        Modifier,
        ModifierCreate,
        ModifierUpdate,
    ]
):

    def _create_array_agg(self, column: Column[Any], type_=String):
        return func.array_agg(column, type_=type_).label(column.name)

    async def get_grouped_modifier_by_effect(self, db: Session):
        modifier_agg = self._create_array_agg(
            model_Modifier.modifierId, type_=ARRAY(Integer)
        )
        position_agg = self._create_array_agg(
            model_Modifier.position, type_=ARRAY(Integer)
        )
        minRoll_agg = self._create_array_agg(model_Modifier.minRoll, type_=ARRAY(Float))
        maxRoll_agg = self._create_array_agg(model_Modifier.maxRoll, type_=ARRAY(Float))
        textRolls_agg = self._create_array_agg(
            model_Modifier.textRolls, type_=ARRAY(String)
        )
        static_agg = self._create_array_agg(model_Modifier.static, type_=ARRAY(Boolean))

        statement = (
            select(
                modifier_agg,
                position_agg,
                minRoll_agg,
                maxRoll_agg,
                textRolls_agg,
                model_Modifier.effect,
                static_agg,
            )
            .group_by(model_Modifier.effect)
            .order_by(model_Modifier.effect)
        )

        db_obj = db.execute(statement).mappings().all()

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        if len(db_obj) == 1:
            db_obj = db_obj[0]

        validate = TypeAdapter(
            Union[GroupedModifierByEffect, List[GroupedModifierByEffect]]
        ).validate_python

        return validate(db_obj)
