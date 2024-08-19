from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.models.models import User
from app.core.schemas.user import UserCreate
from app.crud import CRUD_user


def init_db(session: Session) -> None:
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
