from typing import Any, Generic, TypeVar

from pydantic import BaseModel, TypeAdapter
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.exceptions import (
    DbObjectDoesNotExistError,
    DbTooManyItemsDeleteError,
    SortingMethodNotSupportedError,
    ValueNotSupportedError,
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
        obj_in: dict[str, Any] | list[dict[str, Any]] | ModelType | list[ModelType],
    ) -> list[dict[str, Any]]:
        """
        Map objects to the model's primary keys.

        Always returns a list.
        """
        if not isinstance(obj_in, list):
            obj_in = [obj_in]

        obj_pks = [key.name for key in self.model.__table__.primary_key]

        obj_pks_values = []
        for obj in obj_in:
            if isinstance(obj, dict):
                obj_pks_value = {key: obj.get(key) for key in obj_pks}
            elif isinstance(obj, self.model):
                obj_pks_value = {key: getattr(obj, key) for key in obj_pks}
            else:
                raise ValueNotSupportedError(
                    value=obj_in,
                    function_name=self._map_obj_pks_to_value.__name__,
                    class_name=self.__class__.__name__,
                )
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
    ) -> ModelType | None:
        # pk_column_names = self.model.__table__.primary_key.columns.keys()
        if isinstance(obj_in, list):
            db_obj = [self.model(**obj.model_dump()) for obj in obj_in]
            create_satement = (
                insert(self.model)
                .values(db_obj)
                .on_conflict_do_nothing(constraint=f"{self.model.__tablename__}_pkey")
            )
            db_obj = db.execute(create_satement)
            if db_obj:
                self.validate(db_obj)
                db.commit()
                [db.refresh(obj) for obj in db_obj]
        else:
            create_satement = (
                insert(self.model)
                .values(obj_in.model_dump())
                .on_conflict_do_nothing(constraint=f"{self.model.__tablename__}_pkey")
            )
            db_obj = db.execute(create_satement)
            if db_obj:
                self.validate(db_obj)
                db.commit()
                db.refresh(db_obj)
        return db_obj

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

        db_obj_primary_keys = self._map_obj_pks_to_value(db_obj)[0]
        check_db_obj_exists = (
            db.query(self.model).filter_by(**db_obj_primary_keys).first()
        )
        if not check_db_obj_exists:
            raise DbObjectDoesNotExistError(
                model_table_name=self.model.__tablename__,
                filter=db_obj_primary_keys,
                function_name=self.update.__name__,
                class_name=self.__class__.__name__,
            )

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
