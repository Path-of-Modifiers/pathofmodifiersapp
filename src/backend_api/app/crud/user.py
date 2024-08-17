from typing import List, Optional, Union
from uuid import UUID

from app.core.schemas.user import UsersPublic
from fastapi import HTTPException
from pydantic import EmailStr, TypeAdapter
from sqlalchemy.sql import select, func
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.core.models.models import User as model_User
from app.core.schemas import UserCreate, UserUpdate, User


class CRUDUser:
    """
    CRUD for User model. This class contains methods to create, update, get and authenticate users
    """

    def __init__(self):
        self.validate = TypeAdapter(Union[User, List[User]]).validate_python
        self.validate_users_public = TypeAdapter(UsersPublic).validate_python
        self.validate_user_create = TypeAdapter(UserCreate).validate_python

    def create_user(self, db: Session, *, user_create: UserCreate) -> model_User:
        """Create a new user

        Args:
            db (Session): DB session
            user_create (UserCreate): User data

        Returns:
            User: Created user
        """
        self.validate_user_create(user_create)
        
        get_user_email_filter = {"email": user_create.email}
        get_user_username_filter = {"username": user_create.username}

        user_email = self.get(db=db, filter=get_user_email_filter)
        if user_email:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        user_username = self.get(db=db, filter=get_user_username_filter)
        if user_username:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Convert the Pydantic model to a dictionary
        user_data = user_create.model_dump()

        # Replace the password field with hashed_password
        user_data["hashedPassword"] = hashed_password

        # Remove the plain-text password field, if necessary
        user_data.pop("password")

        # Create the database object with the modified data
        db_obj = model_User(**user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.validate(db_obj)

    def get_all_users(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> UsersPublic:
        """Get all users

        Args:
            db (Session): DB session
            skip (int, optional): Skip. Defaults to 0.
            limit (int, optional): Limit. Defaults to 100.

        Returns:
            List[model_User]: List of users
        """
        count_statement = select(func.count()).select_from(model_User)
        count = db.execute(count_statement).one()[0]

        users = db.query(model_User).offset(skip).limit(limit).all()

        users_public = UsersPublic(data=users, count=count)
        return self.validate_users_public(users_public)

    def update_user(
        self, db: Session, *, user_id: UUID, user_in: UserUpdate
    ) -> model_User:
        """Update user

        Args:
            db (Session): DB session
            db_user (model_User): DB user object
            user_in (UserUpdate): User data to update

        Returns:
            Any: Updated user
        """
        db_user = self.get(db=db, filter={"userId": user_id})

        if user_in.email:
            get_user_email_filter = {"email": user_in.email}
            existing_user_with_email = self.get(db=db, filter=get_user_email_filter)

            if (
                existing_user_with_email
                and existing_user_with_email.userId != db_user.userId
            ):
                raise HTTPException(
                    status_code=409,
                    detail="User with this email already exists",
                )
        if user_in.username:
            get_user_username_filter = {"username": user_in.username}
            existing_user_with_username = self.get(
                db=db, filter=get_user_username_filter
            )
            if (
                existing_user_with_username
                and existing_user_with_username.userId != db_user.userId
            ):
                raise HTTPException(
                    status_code=409,
                    detail="User with this username already exists",
                )

        obj_data = db_user.__table__.columns.keys()

        user_update_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_update_data:
            password = user_update_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashedPassword"] = hashed_password
            user_update_data.pop("password")
        for field in user_update_data:
            if field in obj_data:
                setattr(db_user, field, user_update_data[field])
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return self.validate(db_user)

    def get(
        self,
        db: Session,
        *,
        filter: dict,
    ) -> Union[model_User, List[model_User]] | None:
        """Get user by filter

        Args:
            db (Session): DB session
            filter (dict): Filter map

        Returns:
            model_User | None: model_User object or None
        """
        if not filter:
            raise HTTPException(
                status_code=400,
                detail="Could not get user. Filter parameters required.",
            )
        session_user = db.query(model_User).filter_by(**filter).all()
        if len(session_user) == 1 and filter:
            session_user = session_user[0]
        if not session_user:
            return None
        self.validate(session_user)
        return session_user

    def get_email_by_username(self, db: Session, *, username: str) -> str | None:
        """Get email by username

        Args:
            db (Session): DB session
            username (str): Username

        Returns:
            str | None: Email or None
        """
        username_map = {"username": username}
        session_user = db.query(model_User).filter_by(**username_map).first()
        if not session_user:
            return None
        return session_user.email

    def authenticate(
        self,
        db: Session,
        *,
        email: Optional[EmailStr] = None,
        username: Optional[str] = None,
        password: str,
    ) -> model_User | None:
        """Authenticate user

        Args:
            db (Session): DB session
            email (str): Email
            password (str): Password

        Returns:
            model_User | None: model_User object or None
        """
        get_user_filter = {}
        if email:
            get_user_filter["email"] = email
        if username:
            get_user_filter["username"] = username
        
        db_user = self.get(db=db, filter=get_user_filter)
        if not db_user or not verify_password(password, db_user.hashedPassword):
            raise HTTPException(
                status_code=400,
                detail="Could not authenticate. Invalid login credentials",
            )
        return self.validate(db_user)

    def set_active(
        self, db: Session, *, db_user: model_User, active: bool
    ) -> model_User:
        """Set user active status

        Args:
            db (Session): DB session
            user (model_User): User object
            active (bool): Active status

        Returns:
            model_User: Updated user
        """
        db_user = db.query(model_User).filter_by(userId=db_user.userId).first()
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="Could not set active. The user with this id does not exist in the system",
            )
        setattr(db_user, "isActive", active)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        self.validate(db_user)
        return db_user
