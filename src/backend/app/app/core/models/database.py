import sqlalchemy as _sql
import sqlalchemy.orm as _orm

from app.core.config import settings
from sqlalchemy.inspection import inspect

engine = _sql.create_engine(settings.DATABASE_URL.unicode_string())

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _orm.declarative_base()

insp = inspect(engine)
