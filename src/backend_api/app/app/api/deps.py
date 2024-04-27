import app.core.models.database as _database



def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()