from sqlalchemy import MetaData, create_engine, event
from app.core.models.database import engine as src_db_engine


src_db_metadata = MetaData()

test_db_engine = create_engine(
    "postgresql://test-pom-oltp-user:test-pom-oltp-password@test-db/test-pom-oltp-db"
)

test_db_metadata = MetaData()


@event.listens_for(src_db_metadata, "column_reflect")
def genericize_datatypes(inspector, tablename, column_dict):
    column_dict["type"] = column_dict["type"].as_generic(allow_nulltype=True)


def mock_src_database_for_test_db():
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

