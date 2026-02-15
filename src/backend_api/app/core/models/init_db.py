from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.models.models import User
from app.core.schemas import UserCreate
from app.crud import CRUD_user


def init_db(session: Session) -> None:
    fix_sequences(session)

    user = session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            isSuperuser=True,
        )
        user = CRUD_user.create(db=session, user_create=user_in)


def fix_sequences(session: Session) -> None:
    "Reset the identity/sequence for tables"
    session.execute(
        text(
            """
            SELECT setval(
                pg_get_serial_sequence('item_base_type', 'itemBaseTypeId'),
                (SELECT COALESCE(MAX("itemBaseTypeId"), 0) FROM item_base_type)
            )
        """
        )
    )

    session.execute(
        text(
            """
            SELECT setval(
                pg_get_serial_sequence('modifier', 'modifierId'),
                (SELECT COALESCE(MAX("modifierId"), 0) FROM modifier)
            )
        """
        )
    )
