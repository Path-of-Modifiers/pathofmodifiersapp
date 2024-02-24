from typing import Generator
import pytest
from sqlalchemy.orm import Session
from app.core.models.database import engine


# @pytest.fixture(scope="session")
# def db() -> Generator:
#     with Session(engine) as session:
#         yield session
#     session.rollback()
#     session.close()