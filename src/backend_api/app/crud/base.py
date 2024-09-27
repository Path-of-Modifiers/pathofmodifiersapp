from itertools import islice
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, TypeAdapter
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import (
    ArgValueNotSupportedError,
    DbObjectDoesNotExistError,
    DbTooManyItemsDeleteError,
    SortingMethodNotSupportedError,
)
from app.exceptions.model_exceptions.db_exception import (
    DbObjectAlreadyExistsError,
    GeneralDBError,
)
from app.logs.logger import logger
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

        self.ignore_update_duplicates = False

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
    ) -> list[dict[str, Any]] | list[dict[str, None]]:
        """
        Map objects to the model's primary keys.

        Returns dict[str, None] when `obj_in` doesn't have primary key stated in it.
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
                raise ArgValueNotSupportedError(
                    value=obj_in,
                    function_name=self._map_obj_pks_to_value.__name__,
                    class_name=self.__class__.__name__,
                )
            obj_pks_values.append(obj_pks_value)

        return obj_pks_values

    def _batch_iterable(self, iterable, batch_size):
        iterable = iter(iterable)
        while True:
            batch = list(islice(iterable, batch_size))
            if not batch:
                break
            yield batch

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
        on_duplicate_pkey_do_nothing: bool | None = None,
        batch_size: int = 2047,  # Adding batch_size parameter to control batch size (optimized for plot query)
    ) -> ModelType | list[ModelType] | None:
        """
        Create an object in the database.

        **Parameters**

        * db: A SQLAlchemy session
        * obj_in: A Pydantic model or list of Pydantic models
        * on_duplicate_pkey_do_nothing: Ignore objects with duplicate primary keys.

        **Returns**

        * A Database object or list of Database objects or None
        * If on_duplicate_pkey_do_nothing is True, the returned objects are the non-conflicted objects.
        Duplicate objects are not returned.
        """
        self.validate(obj_in)

        primary_keys = [
            field
            for field in self.model.__table__.primary_key
            if field in self.create_schema.model_fields
        ]

        if isinstance(obj_in, list):
            model_dict_list = [obj.model_dump(exclude=primary_keys) for obj in obj_in]
        else:
            model_dict_list = [obj_in.model_dump(exclude=primary_keys)]

        created_objects = []

        # Break the model_dict_list into batches
        for batch in self._batch_iterable(model_dict_list, batch_size):
            create_statement = insert(self.model).values(batch)
            if on_duplicate_pkey_do_nothing:
                create_statement = create_statement.on_conflict_do_nothing(
                    constraint=f"{self.model.__tablename__}_pkey"
                )
            create_statement = create_statement.returning(self.model)

            try:
                logger.info(f"Total objects to create: {len(model_dict_list)}")
                objs_returned = db.execute(create_statement).scalars().all()
            except IntegrityError as e:
                db.rollback()
                reason = str(e.args[0])
                model_pks = self._map_obj_pks_to_value(model_dict_list)
                if "duplicate key value violates unique constraint" in reason:
                    raise DbObjectAlreadyExistsError(
                        model_table_name=self.model.__tablename__,
                        filter=model_pks,
                        function_name=self.create.__name__,
                        class_name=self.__class__.__name__,
                    )
                else:
                    raise GeneralDBError(
                        function_name=self.create.__name__,
                        class_name=self.__class__.__name__,
                        exception=e,
                    )
            except Exception as e:
                db.rollback()
                raise GeneralDBError(
                    function_name=self.create.__name__,
                    class_name=self.__class__.__name__,
                    exception=e,
                )

            db.commit()

            # Use `merge()` instead of `add()` and `refresh()`
            db_objs_merged = [db.merge(obj) for obj in objs_returned]
            created_objects.extend(db_objs_merged)

        if not created_objects:
            return None

        if len(created_objects) == 1:
            return created_objects[0]

        return self.validate(created_objects)

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

        # [0] because update can only update 1
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
