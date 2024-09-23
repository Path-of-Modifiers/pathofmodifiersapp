from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models.models import User
from app.core.schemas.user import UserCreate
from app.crud import CRUD_user


async def init_db(db: AsyncSession) -> None:
    async with db.begin():
        superuser_stmt = select(User).where(User.email == settings.FIRST_SUPERUSER)
        result = await db.execute(superuser_stmt)
    user = result.scalars().first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            isSuperuser=True,
        )
        user = await CRUD_user.create(db=db, user_create=user_in)
