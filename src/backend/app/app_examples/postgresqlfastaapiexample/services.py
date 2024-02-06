from typing import TYPE_CHECKING, List

import database as _database
import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_contact(contact: _schemas.CreateContact, db: "Session"
) -> _schemas.Contact:
    contact = _models.Contact(**contact.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    print("EMAIL: " + contact.email)
    return _schemas.Contact.model_validate(contact)

async def get_all_contacts(db: "Session") -> List[_schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.model_validate, contacts))

async def get_contact(contact_id: int, db: "Session"):
    contact = db.query(_models.Contact).filter(_models.Contact.id == contact_id).first()
    return contact

async def delete_contact(contact: _models.Contact, db: "Session"):
    db.delete(contact)
    db.commit()

async def update_contact(contact_data: _schemas.CreateContact, contact: _models.Contact, db: "Session"
) -> _schemas.Contact:
    contact.name = contact_data.name
    contact.email = contact_data.email
    contact.phone = contact_data.phone
    contact.updated_at = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(contact)

    return _schemas.Contact.model_validate(contact)


