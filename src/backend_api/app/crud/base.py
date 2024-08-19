from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session

from app.api.api_message_util import (
    get_no_obj_matching_query_msg,
    get_sorting_method_not_supported_msg,
    get_too_many_items_delete_msg,
)
from app.utils.sort_algorithms import sort_with_reference

ModelType = TypeVar("ModelType", bound=Any)
SchemaType = TypeVar("SchemaType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: type[ModelType],
        schema: type[SchemaType],
        create_schema: type[CreateSchemaType],
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `models`: A SQLAlchemy schema class
        * `schema`: A Pydantic schema (schema) class
        """
        self.model = model
        self.schema = schema
        self.create_schema = create_schema

        self.validate = TypeAdapter(SchemaType | list[SchemaType]).validate_python

    def _sort_objects(
        self,
        objs: list[ModelType],
        key: str | None = None,
        sort: str | None = None,
    ) -> list[ModelType]:
        available_sorting_choices = ["asc", "dec"]
        if sort is None:
            return objs
        elif sort not in available_sorting_choices:
            raise NotImplementedError(
                get_sorting_method_not_supported_msg(sort, available_sorting_choices)
            )
        if sort in ["asc", "dec"]:
            unsorted_extracted_column = []
            for obj in objs:
                unsorted_extracted_column.append(getattr(obj, key))

            sorted_objs = sort_with_reference(objs, unsorted_extracted_column)

            if sort == "asc":
                return sorted_objs
            else:
                return sorted_objs[::-1]

    async def get(
        self,
        db: Session,
        filter: dict[str, Any] | None = None,
        *,
        sort_key: str | None = None,
        sort: str | None = None,
    ) -> ModelType | list[ModelType] | None:
        if filter is None:
            db_obj = db.query(self.model).all()
        else:
            db_obj = db.query(self.model).filter_by(**filter).all()
        if not db_obj and not filter:  # Get all objs on an empty db
            pass
        elif not db_obj:
            raise HTTPException(
                status_code=404,
                detail=get_no_obj_matching_query_msg(filter, self.model).message,
            )
        if len(db_obj) == 1 and filter:
            db_obj = db_obj[0]
        else:
            db_obj = self._sort_objects(db_obj, key=sort_key, sort=sort)
        return self.validate(db_obj)

    async def create(
        self, db: Session, *, obj_in: CreateSchemaType | list[CreateSchemaType]
    ) -> ModelType:
        if isinstance(obj_in, list):
            db_obj = [self.model(**obj.model_dump()) for obj in obj_in]
            db.add_all(db_obj)
            db.commit()
            [db.refresh(obj) for obj in db_obj]
        else:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return self.validate(db_obj)

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        obj_data = db_obj.__table__.columns.keys()

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()
        for field in obj_data:
            if field in update_data:
                # print(field, update_data[field])
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return self.validate(db_obj)

    async def remove(
        self,
        db: Session,
        *,
        filter: Any,
        sort_key: str | None = None,
        sort: str | None = None,
        max_deletion_limit: int | None = 12,
    ) -> ModelType:
        db_objs = db.query(self.model).filter_by(**filter).all()
        if not db_objs:
            raise HTTPException(
                status_code=404,
                detail=get_no_obj_matching_query_msg(filter, self.model).message,
            )
        elif (
            len(db_objs) > max_deletion_limit
        ):  # Arbitrary number, not too large, but should allow deleting all modifiers assosiated with an item
            raise HTTPException(
                status_code=403,
                detail=get_too_many_items_delete_msg(
                    filter, max_deletion_limit
                ).message,
            )

        if len(db_objs) == 1:
            db_objs = db_objs[0]
            db.delete(db_objs)
        else:
            db_objs = self._sort_objects(db_objs, key=sort_key, sort=sort)
            [db.delete(obj) for obj in db_objs]
        db.commit()
        return self.validate(db_objs)
