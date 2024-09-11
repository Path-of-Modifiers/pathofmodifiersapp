from typing import Any, Generic, TypeVar

from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session

from app.exceptions import (
    DbObjectAlreadyExistsError,
    DbObjectDoesNotExistError,
    DbTooManyItemsDeleteError,
    SortingMethodNotSupportedError,
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
        ignore_duplicates: bool = False,
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
        self.ignore_duplicates = ignore_duplicates

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
            raise SortingMethodNotSupportedError(
                sort=sort,
                available_sorting_choices=available_sorting_choices,
                function_name=self._sort_objects.__name__,
                class_name=self.__class__.__name__,
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

    def _map_obj_pks_to_value(
        self,
        obj_in: (
            SchemaType
            | CreateSchemaType
            | UpdateSchemaType
            | list[SchemaType | CreateSchemaType | UpdateSchemaType]
        ),
    ) -> list[dict[str, Any]]:
        """A private method used to map schema objects to the model's primary keys"""
        self.validate(obj_in)

        if not isinstance(obj_in, list):
            obj_in = [obj_in]

        obj_pks = [key.name for key in self.model.__table__.primary_key]

        obj_pks_values = []
        for obj in obj_in:
            obj_pks_value = {key: getattr(obj, key) for key in obj_pks}
            obj_pks_values.append(obj_pks_value)

        return obj_pks_values

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
            raise DbObjectDoesNotExistError(
                model_table_name=self.model.__tablename__,
                filter=filter,
                function_name=self.get.__name__,
                class_name=self.__class__.__name__,
            )
        if len(db_obj) == 1 and filter:
            db_obj = db_obj[0]
        else:
            db_obj = self._sort_objects(db_obj, key=sort_key, sort=sort)
        return self.validate(db_obj)

    async def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType | list[CreateSchemaType],
    ) -> ModelType:
        if not self.ignore_duplicates:
            obj_pks_value_filters = self._map_obj_pks_to_value(obj_in)
            for obj_in_pks_filter in obj_pks_value_filters:
                # May need to change self.get handling when obj does not exist
                try:
                    existing_db_obj = await self.get(db, filter=obj_in_pks_filter)
                except DbObjectDoesNotExistError:
                    existing_db_obj = None
                if existing_db_obj:
                    raise DbObjectAlreadyExistsError(
                        model_table_name=self.model.__tablename__,
                        filter=obj_in_pks_filter,
                        function_name=self.create.__name__,
                        class_name=self.__class__.__name__,
                    )
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
            raise DbObjectDoesNotExistError(
                model_table_name=self.model.__tablename__,
                filter=filter,
                function_name=self.remove.__name__,
                class_name=self.__class__.__name__,
            )
        elif (
            len(db_objs) > max_deletion_limit
        ):  # Arbitrary number, not too large, but should allow deleting all modifiers assosiated with an item
            raise DbTooManyItemsDeleteError(
                model_table_name=self.model.__tablename__,
                filter=filter,
                function_name=self.remove.__name__,
                class_name=self.__class__.__name__,
            )

        if len(db_objs) == 1:
            db_objs = db_objs[0]
            db.delete(db_objs)
        else:
            db_objs = self._sort_objects(db_objs, key=sort_key, sort=sort)
            [db.delete(obj) for obj in db_objs]
        db.commit()
        return self.validate(db_objs)
