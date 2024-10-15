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
            model_Modifier.regex,
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

        modifiers_df = pd.DataFrame(db_obj).sort_values(by="modifierId")

        grouped_modifier_df = modifiers_df.groupby(
            ["effect", "regex", "static", "relatedUniques"],
            as_index=False,
            dropna=False,
            sort=False,
        ).agg(lambda x: list(x))

        not_static_mask = grouped_modifier_df["static"].isna()
        grouped_modifier_df.loc[not_static_mask, "static"] = None
        grouped_modifier_df.loc[~not_static_mask, "regex"] = grouped_modifier_df.loc[
            ~not_static_mask, "effect"
        ]

        # Stores the listed fields in a list of dicts
        grouped_modifier_record = grouped_modifier_df[
            ["modifierId", "textRolls"]
        ].to_dict("records")

        # Removes the listed fields
        grouped_modifier_df = grouped_modifier_df.drop(
            ["modifierId", "textRolls"], axis=1
        )

        # Adds the fields back in, but as a field with dicts
        grouped_modifier_df["groupedModifier"] = grouped_modifier_record

        grouped_modifier_by_effect_record = grouped_modifier_df.to_dict("records")

        validate = TypeAdapter(
            GroupedModifierByEffect | list[GroupedModifierByEffect]
        ).validate_python

        return validate(grouped_modifier_by_effect_record)
