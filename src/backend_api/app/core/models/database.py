from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Mapped type models because scalars functions:
class Base(DeclarativeBase):
    pass


DATABASE_URI = str(settings.DATABASE_URI)

engine = create_async_engine(DATABASE_URI, pool_size=300, max_overflow=0)


def inspect_foreign_keys(conn, model):
    inspector = inspect(conn)
    # return any value to the caller
    return inspector.get_foreign_keys(model.__tablename__)


async def get_foreign_keys(model):
    async with engine.connect() as conn:
        foreign_keys = await conn.run_sync(inspect_foreign_keys, model)

    return foreign_keys


# From https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
# class DatabaseSessionManager:
#     def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
#         self._engine = create_async_engine(host, **engine_kwargs)
#         self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

#     @property
#     def insp(self):
#         return

#     async def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         await self._engine.dispose()

#         self._engine = None
#         self._sessionmaker = None

#     @asynccontextmanager
#     async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception as e:
#                 await connection.rollback()
#                 raise e

#     @asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         session = self._sessionmaker()
#         try:
#             yield session
#         except Exception as e:
#             await session.rollback()
#             raise e


# sessionmanager = DatabaseSessionManager(
#     str(settings.DATABASE_URI), engine_kwargs={"pool_size": 300, "max_overflow": 0}
# )
