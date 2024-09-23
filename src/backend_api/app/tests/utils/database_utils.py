from sqlalchemy import MetaData

# from app.core.models.database import sessionmanager
# from app.tests.setup_test_database import test_sessionmanager

src_db_metadata = MetaData()
test_db_metadata = MetaData()


# async def mock_src_database_for_test_db():
#     """Mock the source database to create the test database schema."""
#     async with sessionmanager.connect() as src_conn, test_sessionmanager.connect() as tgt_conn:
#         await tgt_conn.run_sync(test_db_metadata.reflect)
#         await tgt_conn.run_sync(test_db_metadata.drop_all)

#         test_db_metadata.clear()
#         await tgt_conn.run_sync(test_db_metadata.reflect)
#         await src_conn.run_sync(src_db_metadata.reflect)

#         await tgt_conn.run_sync(src_db_metadata.create_all)


# async def clear_all_tables():
#     """Clear all tables in the test database."""
#     async with test_sessionmanager.connect() as tgt_conn:
#         await tgt_conn.run_sync(test_db_metadata.reflect)

#         try:
#             for table in reversed(test_db_metadata.sorted_tables):
#                 if table.name == "alembic_version":
#                     continue
#                 elif table.name == User.__tablename__:
#                     stmt = delete(User).where(
#                         and_(
#                             User.username != settings.FIRST_SUPERUSER_USERNAME,
#                             User.username != settings.TEST_USER_USERNAME,
#                         )
#                     )
#                     await tgt_conn.execute(stmt)
#                 else:
#                     await tgt_conn.execute(delete(table))

#             print("All tables cleared successfully.")
#         except SQLAlchemyError as e:
#             print(f"Error: {e}")
#             raise e
