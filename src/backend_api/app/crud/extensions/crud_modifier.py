from backend_api.app.core.models.models import Modifier as model_Modifier
from backend_api.app.core.models.models import ModifierRoll as model_ModifierRoll
from backend_api.app.core.schemas.modifier import (
    GroupedModifier,
    Modifier,
    ModifierCreate,
    ModifierUpdate,
)
from backend_api.app.crud.base import CRUDBase
from pydantic import TypeAdapter
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy.orm import Session


class CRUDModifier(
    CRUDBase[
        model_Modifier,
        Modifier,
        ModifierCreate,
        ModifierUpdate,
    ]
):
    def __init__(self):
        super().__init__(
            model=model_Modifier,
            schema=Modifier,
            create_schema=ModifierCreate,
        )

    async def create(
        self, db: Session, *, modifiers: list[ModifierCreate]
    ) -> list[Modifier]:
        db_modifiers = [
            model_Modifier(**modifier.model_dump(exclude="rolls"))
            for modifier in modifiers
        ]

        db.add_all(db_modifiers)
        db.flush()

        db_modifier_rolls = [
            model_ModifierRoll(
                modifierId=db_modifier.modifierId, **modifier_roll.model_dump()
            )
            for db_modifier, modifier in zip(db_modifiers, modifiers, strict=True)
            for modifier_roll in modifier.rolls
        ]
        db.add_all(db_modifier_rolls)
        db.flush()
        db.commit()

        return self.validate(db_modifiers)

    async def update(self, db: Session, *, modifier: ModifierUpdate):
        update_modifier_stmt = (
            update(model_Modifier)
            .where(model_Modifier.modifierId == modifier.modifierId)
            .values(**modifier.model_dump(exclude_unset=True, exclude_none=True))
        )
        db.execute(update_modifier_stmt)

        modifier_rolls = [
            {"modifierId": modifier.modifierId, **roll.model_dump(exclude_unset=True)}
            for roll in modifier.rolls
        ]
        if modifier_rolls:
            db.execute(update(model_ModifierRoll), modifier_rolls)
        db.commit()

    async def get_grouped_modifiers(self, db: Session) -> list[GroupedModifier]:
        grouped_modifier_rolls = (
            select(
                model_ModifierRoll.modifierId,
                func.json_agg(
                    aggregate_order_by(
                        func.json_build_object(
                            "position",
                            model_ModifierRoll.position,
                            "minRoll",
                            model_ModifierRoll.minRoll,
                            "maxRoll",
                            model_ModifierRoll.maxRoll,
                            "textRolls",
                            model_ModifierRoll.textRolls,
                        ),
                        model_ModifierRoll.modifierId,
                        model_ModifierRoll.position,
                    ),
                ).label("rolls"),
            )
            .group_by(model_ModifierRoll.modifierId)
            .cte("grouped_modifier_rolls")
        )

        stmt = select(
            *model_Modifier.__table__.columns, grouped_modifier_rolls.c.rolls
        ).join(
            grouped_modifier_rolls,
            model_Modifier.modifierId == grouped_modifier_rolls.c.modifierId,
        )
        grouped_modifiers = db.execute(stmt).mappings().all()

        return TypeAdapter(list[GroupedModifier]).validate_python(grouped_modifiers)
