from sqlalchemy import Boolean, Column, Float, Integer, MetaData, String, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.schema import Table

from app.core.models.models import UnidentifiedItem as model_UnidentifiedItem
from app.core.schemas.unidentified_item import (
    UnidentifiedItem,
    UnidentifiedItemCreate,
    UnidentifiedItemUpdate,
)
from app.crud.base import CRUDBase
from app.exceptions.model_exceptions.db_exception import (
    DbObjectAlreadyExistsError,
    GeneralDBError,
)
from app.logs.logger import logger


class CRUDUnidentifiedItem(
    CRUDBase[
        model_UnidentifiedItem,
        UnidentifiedItem,
        UnidentifiedItemCreate,
        UnidentifiedItemUpdate,
    ]
):
    def __init__(self, model, schema, create_schema):
        super().__init__(model, schema, create_schema)

        self.view = Table(
            "unidentifiedItemView",
            MetaData(),
            Column("name", String),
            Column("itemBaseTypeId", Integer),
            Column("createdHoursSinceLaunch", Integer),
            Column("league", String),
            Column("currencyId", Integer),
            Column("ilvl", Integer),
            Column("currencyAmount", Float),
            Column("nItems", Integer),
            Column("identified", Boolean),
            Column("rarity", String),
        )

    def _create_bulk_insert(
        self,
        db: Session,
        *,
        model_dict_list,
        return_nothing: bool | None = None,  # noqa: ARG003
    ) -> list[model_UnidentifiedItem] | None:
        """
        Create objects with bulk_insert.

        Approx. 3 times faster with `return_nothing=True`.
        """
        logger.debug(f"Total objects to create: {len(model_dict_list)}")
        # create_stmt = f"{insert(self.view).values(model_dict_list)}".replace(
        #     '"unidentifiedItemView"', "unidentifiedItemView"
        # )
        create_stmt = str(
            insert(self.view)
            .values(model_dict_list)
            .compile(compile_kwargs={"literal_binds": True})
        ).replace('"unidentifiedItemView"', "unidentifiedItemView")
        print("jhajhdjsah", create_stmt)
        try:
            # db.execute(create_stmt, model_dict_list)
            db.execute(text(create_stmt))
            # db.execute(create_stmt)
        except Exception as e:
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
                    model_table_name=self.model.__tablename__,
                    function_name=self.create.__name__,
                    class_name=self.__class__.__name__,
                    exception=e,
                )
