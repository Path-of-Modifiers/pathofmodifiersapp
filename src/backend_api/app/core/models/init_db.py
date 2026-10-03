from backend_api.app.core.config import settings
from backend_api.app.core.models.models import User
from backend_api.app.core.schemas.user import UserCreate
from backend_api.app.crud import CRUD_user
from sqlalchemy import select
from sqlalchemy.orm import Session


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
