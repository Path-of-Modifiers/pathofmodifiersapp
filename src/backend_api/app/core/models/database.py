from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URI))
async_engine = create_async_engine(  # This engine is used for plotting queries
    str(settings.DATABASE_URI), isolation_level="READ UNCOMMITTED", echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

Base = declarative_base()

insp = inspect(engine)
