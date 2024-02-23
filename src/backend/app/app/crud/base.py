from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session


from sqlalchemy.inspection import inspect


ModelType = TypeVar("ModelType", bound=Any)
SchemaType = TypeVar("SchemaType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `models`: A SQLAlchemy schema class
        * `schema`: A Pydantic schema (schema) class
        """
        self.model = model
        self.schema = schema

        self.validate = TypeAdapter(Union[SchemaType, List[SchemaType]]).validate_python

    async def get(
        self, db: Session, filter: Any = {}
    ) -> Optional[Union[ModelType, List[ModelType]]]:
        db_obj = db.query(self.model).filter_by(**filter).all()
        if not db_obj and not filter:  # Get all objs on an empty db
            pass
        elif not db_obj:
            raise HTTPException(
                status_code=404,
                detail=f"No object matching the query ({', '.join([key + ': ' + str(item) for key, item in filter.items()])}) in the table {self.model.__tablename__} was found.",
            )
        if len(db_obj) == 1:
            db_obj = db_obj[0]
        return self.validate(db_obj)

    async def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, List[CreateSchemaType]]
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
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return self.validate(db_obj)

    async def remove(self, db: Session, *, filter: Any) -> ModelType:
        db_objs = db.query(self.model).filter_by(**filter).all()
        if not db_objs:
            raise HTTPException(
                status_code=404,
                detail=f"No object matching the query ({', '.join([key + ': ' + str(item) for key, item in filter.items()])}) in the table {self.model.__tablename__} was found.",
            )
        elif (
            len(db_objs) > 12
        ):  # Arbitrary number, not too large, but should allow deleting all modifiers assosiated with an item
            raise HTTPException(
                status_code=403,
                detail=f"Too many objects ({len(db_objs)}) matching the query ({','.join([key + ': ' + str(item) for key, item in filter.items()])}), cannot delete and guarantee safety.",
            )
        [db.delete(obj) for obj in db_objs]
        db.commit()
        return self.validate(db_objs)
