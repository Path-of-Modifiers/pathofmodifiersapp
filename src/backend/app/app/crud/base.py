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

    async def get(self, db: Session, filter: Any) -> Optional[Union[ModelType, List[ModelType]]]:
        db_obj = db.query(self.model).filter_by(**filter).all()
        if not db_obj:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.model)} not found"
            )
        return self.validate(db_obj)

    async def get_all(self, db: Session) -> List[ModelType]:
        db_all_obj = db.query(self.model).all()
        if db_all_obj is None:
            raise HTTPException(
                status_code=404, detail=f"All objects in {type(self.model)} not found"
            )
        return self.validate(db_all_obj)

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
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()
            for field in obj_in:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        return self.validate(db_obj)

    async def remove(self, db: Session, *, filter: Any) -> ModelType:
        objs = db.query(self.model).filter_by(**filter).all()
        if not objs:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.model)} not found"
            )
        elif (
            len(objs) > 12
        ):  # Arbitrary number, not too large, but should allow deleting all modifiers assosiated with an item
            raise HTTPException(
                status_code=403,
                detail=f"Too many objects ({len(objs)}) matched the query, cannot delete and guarantee safety",
            )
        [db.delete(obj) for obj in objs]
        db.commit()
        return self.validate(objs)
