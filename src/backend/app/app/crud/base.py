from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

SchemaType = TypeVar("SchemaType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ListCreateSchemaType = TypeVar("ListCreateSchemaType", bound=List[BaseModel])
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ListUpdateSchemaType = TypeVar("ListUpdateSchemaType", bound=List[BaseModel])


class CRUDBase(Generic[SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, schema: Type[SchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `schema`: A SQLAlchemy schema class
        * `schema`: A Pydantic schema (schema) class
        """
        self.schema = schema

    async def get(self, db: Session, id: Any) -> Optional[SchemaType]:
        db_obj = db.query(self.schema).filter(self.schema.id == id).first()
        if db_obj is None:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.schema)} not found"
            )
        return db_obj
    
    async def get_all(self, db: Session) -> List[SchemaType]:
        db_all_obj = db.query(self.schema).all()
        if db_all_obj is None:
            raise HTTPException(
                status_code=404, detail=f"All objects in {type(self.schema)} not found"
            )
        return db_all_obj

    async def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, ListCreateSchemaType]
    ) -> SchemaType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.schema(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: SchemaType,
        obj_in: Union[UpdateSchemaType, ListUpdateSchemaType, Dict[str, Any]],
    ) -> SchemaType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # update_data = obj_in.dict(exclude_unset=True)
            update_data = obj_in.model_dump()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: int) -> SchemaType:
        obj = db.query(self.schema).get(id)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"Object in {type(self.schema)} not found"
            )
        db.delete(obj)
        db.commit()
        return obj
