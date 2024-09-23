from typing import Any

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import Boolean, Column, Float, Integer, String, func, select
from sqlalchemy.dialects.postgresql import ARRAY, aggregate_order_by
from sqlalchemy.ext.asyncio import AsyncSession

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
    def _create_array_agg(self, column: Column[Any], type_: ARRAY) -> Column[Any]:
        return func.array_agg(column, type_=type_).label(column.name)

    def _create_array_agg_position(self) -> Column[Any]:
        return func.array_agg(
            aggregate_order_by(model_Modifier.position, model_Modifier.position.asc()),
            type_=ARRAY(Integer),
        ).label(model_Modifier.position.name)

    async def get_grouped_modifier_by_effect(
        self, db: AsyncSession
    ) -> GroupedModifierByEffect:
        modifier_agg = self._create_array_agg(
            model_Modifier.modifierId, type_=ARRAY(Integer)
        )
        position_agg = self._create_array_agg_position()
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
            .order_by(
                model_Modifier.effect,
            )
        )

        result = await db.execute(statement)
        mapped_result = result.mappings().all()

        if not mapped_result:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        if len(mapped_result) == 1:
            mapped_result = mapped_result[0]

        validate = TypeAdapter(
            GroupedModifierByEffect | list[GroupedModifierByEffect]
        ).validate_python

        return validate(mapped_result)
