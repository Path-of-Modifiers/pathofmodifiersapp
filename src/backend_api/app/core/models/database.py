from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URI))
async_engine = create_async_engine(  # This engine is used for plotting queries
    str(settings.ASYNC_DATABASE_URI), echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, autobegin=False
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


insp = inspect(engine)
