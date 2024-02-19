from typing import TYPE_CHECKING, List

import app.core.models.models as _models
import app.core.schemas as _schemas
import app.core.models.database as _database
import pydantic as _pydantic

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_commit_refresh(field: _pydantic.BaseModel, db: "Session"):
    db.add(field)
    db.commit()
    db.refresh(field)
