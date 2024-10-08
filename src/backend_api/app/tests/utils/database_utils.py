from sqlalchemy import Engine, MetaData, delete
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.models.database import engine as src_db_engine
from app.core.models.models import User

src_db_metadata = MetaData()
test_db_metadata = MetaData()


def mock_src_database_for_test_db(test_db_engine: Engine):
    """Mock the source database to create the test database schema."""

    src_conn = src_db_engine.connect()
    tgt_conn = test_db_engine.connect()
    test_db_metadata.reflect(bind=test_db_engine)

    # drop all tables in test database
    for table in reversed(test_db_metadata.sorted_tables):
        table.drop(bind=test_db_engine)

    # Delete all data in test database
    for table in reversed(test_db_metadata.sorted_tables):
        table.delete()

    test_db_metadata.clear()
    test_db_metadata.reflect(bind=test_db_engine)
    src_db_metadata.reflect(bind=src_db_engine)

    # create all tables in test database
    for table in src_db_metadata.sorted_tables:
        table.create(bind=test_db_engine)

    tgt_conn.commit()

    src_conn.close()
    tgt_conn.close()


def clear_all_tables(test_db_engine: Engine):
    """Clear all tables in the test database."""
    print("Clearing all tables...")

    src_conn = test_db_engine.connect()
    transaction = src_conn.begin()

    test_db_metadata.reflect(bind=test_db_engine)

    try:
        for table in reversed(test_db_metadata.sorted_tables):
            print(f"Clearing table {table.name}...")
            if table.name == "alembic_version":
                continue
            elif table.name == User.__tablename__:
                # Don't delete first superuser row or test user row
                stmt = delete(User).where(
                    User.username != settings.FIRST_SUPERUSER_USERNAME
                    or User.username != settings.TEST_USER_USERNAME
                )
                src_conn.execute(stmt)
            else:
                src_conn.execute(table.delete())
        transaction.commit()
        print("All tables cleared successfully.")
    except SQLAlchemyError as e:
        transaction.rollback()
        print(f"Error: {e}")
    finally:
        src_conn.close()
