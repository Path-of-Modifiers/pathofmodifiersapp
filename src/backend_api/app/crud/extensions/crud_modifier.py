from datetime import datetime, timezone

import pandas as pd
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import desc, select, text
from sqlalchemy.orm import Session

from app.core.config import settings
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
        db_modifier_rows = db.execute(stmt).mappings().all()

        if not db_modifier_rows:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        modifiers_df = pd.DataFrame(db_modifier_rows).sort_values(by="modifierId")

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
        grouped_modifier_properties_record = grouped_modifier_df[
            ["modifierId", "textRolls"]
        ].to_dict("records")

        # Removes the listed fields
        grouped_modifier_df = grouped_modifier_df.drop(
            ["modifierId", "textRolls"], axis=1
        )

        # Adds the fields back in, but as a field with dicts
        grouped_modifier_df[
            "groupedModifierProperties"
        ] = grouped_modifier_properties_record

        grouped_modifier_by_effect_record = grouped_modifier_df.to_dict("records")

        validate = TypeAdapter(
            GroupedModifierByEffect | list[GroupedModifierByEffect]
        ).validate_python

        return validate(grouped_modifier_by_effect_record)

    async def create_initial_dynamically_created_mod(self, db: Session) -> None:
        existing_dynamically_created = db.execute(
            select(model_Modifier)
            .where(model_Modifier.dynamicallyCreated)
            .order_by(desc(model_Modifier.dynamicallyCreated))
        ).first()

        if not existing_dynamically_created:
            modifier_in = ModifierCreate(
                position=0,
                effect="EMPTY",
                dynamicallyCreated=True,
                static=True,
            )
            await self.create(db=db, obj_in=modifier_in)
        else:
            "I know this shit is messy"
            # Check if latest item inserted is older than 3 days, if so then create new initial dynamic modifier
            existing_dynamically_created = existing_dynamically_created[0]

            item_result = db.execute(
                text(
                    f"""SELECT MAX("createdHoursSinceLaunch") FROM item WHERE "league"='{settings.CURRENT_SOFTCORE_LEAGUE}'"""
                )
            ).fetchone()

            existing_item_hours_since_launch = item_result[0] if item_result else None
            now = datetime.now(timezone.utc)

            league_launch_datetime = datetime.fromisoformat(settings.LEAGUE_LAUNCH_TIME)

            delta = now - league_launch_datetime
            hours_since_launch = delta.total_seconds() / 3600

            existing_item_hours_since_launch_diff = None
            if existing_item_hours_since_launch is not None:
                existing_item_hours_since_launch_diff = (
                    hours_since_launch - existing_item_hours_since_launch
                )

            min_hours_between = settings.MIN_DAYS_BEFORE_NEW_INIT_DYNAMIC_MODIFIER * 24

            if (
                existing_item_hours_since_launch is None
                or existing_item_hours_since_launch_diff is None
                or existing_item_hours_since_launch_diff > min_hours_between
            ):
                empty_filter = {"effect": "EMPTY"}
                existing_empty_mod = await self.get(db=db, filter=empty_filter)
                assert not isinstance(
                    existing_empty_mod, list
                ), "Found duplicate `EMPTY` effect in modifier table, though there should be max 1"
                await self.remove(db=db, filter=empty_filter)

                modifier_in = ModifierCreate(
                    position=0,
                    effect="EMPTY",
                    dynamicallyCreated=True,
                    static=True,
                )
                await self.create(db=db, obj_in=modifier_in)
