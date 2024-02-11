import datetime as _dt 
import sqlalchemy as _sql

import database as _database

class Contact(_database.Base):
    __tablename__ = "contacts"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True)
    phone = _sql.Column(_sql.String, unique=True)
    created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    updated_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)