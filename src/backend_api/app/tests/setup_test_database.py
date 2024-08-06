import os
from typing import Optional
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.models.database import Base


TEST_DATABASE_URL: Optional[PostgresDsn] = os.getenv("TEST_DATABASE_URL")

test_db_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_db_engine
)

Base.metadata.create_all(bind=test_db_engine)


# This is a fixture that overrides the get_db dependency of the FastAPI app.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
