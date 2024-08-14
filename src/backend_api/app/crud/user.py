from typing import Any, List, Union

from pydantic import TypeAdapter
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.core.models.models import User as model_User
from app.core.schemas import UserCreate, UserUpdate, User


class CRUDUser:
    """
    CRUD for User model. This class contains methods to create, update, get and authenticate users
    """

    def __init__(self):
        self.validate = TypeAdapter(Union[User, List[User]]).validate_python

    def create_user(self, *, session: Session, user_create: UserCreate) -> model_User:
        """Create a new user

        Args:
            session (Session): DB session
            user_create (UserCreate): User data

        Returns:
            User: Created user
        """

        db_obj = self.validate(
            user_create,
            update={"hashed_password": get_password_hash(user_create.password)},
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update_user(
        self, *, session: Session, db_user: model_User, user_in: UserUpdate
    ) -> Any:
        """Update user

        Args:
            session (Session): DB session
            db_user (model_User): DB user object
            user_in (UserUpdate): User data to update

        Returns:
            Any: Updated user
        """

        user_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        for field in db_user:
            if field in user_in:
                setattr(db_user, field, user_in[field])
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def get_user_by_email(self, *, session: Session, email: str) -> model_User | None:
        """Get user by email

        Args:
            session (Session): DB session
            email (str): Email

        Returns:
            model_User | None: model_User object or None
        """

        statement = select(model_User).where(model_User.email == email)
        session_user = session.exec(statement).first()
        return session_user

    def authenticate(
        self, *, session: Session, email: str, password: str
    ) -> model_User | None:
        """Authenticate user

        Args:
            session (Session): DB session
            email (str): Email
            password (str): Password

        Returns:
            model_User | None: model_User object or None
        """

        db_user = self.get_user_by_email(session=session, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashedPassword):
            return None
        return db_user
