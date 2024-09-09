from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models.models import ItemBaseType as model_item_base_type
from app.core.schemas.item_base_type import (
    BaseType,
    ItemBaseType,
    ItemBaseTypeCategory,
    ItemBaseTypeCreate,
    ItemBaseTypeSubCategory,
    ItemBaseTypeUpdate,
)
from app.crud.base import CRUDBase


class CRUDItemBaseType(
    CRUDBase[
        model_item_base_type,
        ItemBaseType,
        ItemBaseTypeCreate,
        ItemBaseTypeUpdate,
    ]
):
    async def get_base_types(self, db: Session):
        statement = select(model_item_base_type.baseType)

        db_obj = db.execute(statement).mappings().all()

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        if len(db_obj) == 1:
            db_obj = db_obj[0]

        validate = TypeAdapter(BaseType | list[BaseType]).validate_python

        return validate(db_obj)

    async def get_unique_item_categories(self, db: Session):
        statement = select(model_item_base_type.category).distinct()

        db_obj = db.execute(statement).mappings().all()

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        if len(db_obj) == 1:
            db_obj = db_obj[0]

        validate = TypeAdapter(
            ItemBaseTypeCategory | list[ItemBaseTypeCategory]
        ).validate_python

        return validate(db_obj)

    async def get_unique_item_sub_categories(self, db: Session):
        statement = (
            select(model_item_base_type.subCategory)
            .distinct()
            .where(model_item_base_type.subCategory.isnot(None))
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
            ItemBaseTypeSubCategory | list[ItemBaseTypeSubCategory]
        ).validate_python

        return validate(db_obj)
