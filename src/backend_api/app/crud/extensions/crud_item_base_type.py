from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def get_base_types(self, db: AsyncSession) -> list[BaseType]:
        statement = select(model_item_base_type.baseType)

        result = await db.execute(statement)
        mapped_result = result.mappings().all()

        if not mapped_result:
            raise HTTPException(
                status_code=404,
                detail=f"No objects found in the table {self.model.__tablename__}.",
            )

        if len(mapped_result) == 1:
            mapped_result = mapped_result[0]

        validate = TypeAdapter(BaseType | list[BaseType]).validate_python

        return validate(mapped_result)

    async def get_unique_item_categories(self, db: AsyncSession):
        statement = select(model_item_base_type.category).distinct()

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
            ItemBaseTypeCategory | list[ItemBaseTypeCategory]
        ).validate_python

        return validate(mapped_result)

    async def get_unique_item_sub_categories(self, db: AsyncSession):
        statement = (
            select(model_item_base_type.subCategory)
            .distinct()
            .where(model_item_base_type.subCategory.isnot(None))
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
            ItemBaseTypeSubCategory | list[ItemBaseTypeSubCategory]
        ).validate_python

        return validate(mapped_result)
