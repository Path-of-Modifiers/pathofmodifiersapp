from uuid import UUID

from pydantic import EmailStr, TypeAdapter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from app.core.models.models import User as model_User
from app.core.schemas import User, UserCreate, UserUpdate
from app.core.schemas.user import UpdatePassword, UsersPublic
from app.core.security import get_password_hash, verify_password
from app.exceptions import (
    DbObjectAlreadyExistsError,
    DbObjectDoesNotExistError,
    InvalidPasswordError,
    NewPasswordIsSameError,
)


class CRUDUser:
    """
    CRUD for User model. This class contains methods to create, update, get and authenticate users
    """

    def __init__(self):
        self.validate = TypeAdapter(User | list[User]).validate_python
        self.validate_users_public = TypeAdapter(UsersPublic).validate_python
        self.validate_user_create = TypeAdapter(UserCreate).validate_python

    def check_exists_raise(
        self,
        db: Session,
        *,
        filter: dict[str, str],
    ):
        """Check if object exists, raise an exception if it does

        Args:
            db (Session): DB session
            filter (dict): Filter map
            user_in (User, optional): User object. Defaults to None.
        """
        existing_user = self.get(db=db, filter=filter)

        if existing_user:
            raise DbObjectAlreadyExistsError(
                model_table_name=model_User.__tablename__,
                filter=filter,
                function_name=self.check_exists_raise.__name__,
                class_name=self.__class__.__name__,
            )

    def create(self, db: Session, *, user_create: UserCreate) -> model_User:
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

        self.check_exists_raise(db=db, filter=get_user_email_filter)
        self.check_exists_raise(db=db, filter=get_user_username_filter)

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

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> UsersPublic:
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

    def update(self, db: Session, *, user_id: UUID, user_in: UserUpdate) -> model_User:
        """Update user

        Args:
            db (Session): DB session
            db_user (model_User): DB user object
            user_in (UserUpdate): User data to update

        Returns:
            Any: Updated user
        """
        user_id_map = {"userId": user_id}
        db_user = self.get(db=db, filter=user_id_map)

        if not db_user:
            raise DbObjectDoesNotExistError(
                model_table_name=model_User.__tablename__,
                filter=user_id_map,
                function_name=self.update.__name__,
                class_name=self.__class__.__name__,
            )

        if user_in.email:
            email_filter = {"email": user_in.email}
            self.check_exists_raise(db=db, filter=email_filter)
        if user_in.username:
            get_user_username_filter = {"username": user_in.username}
            self.check_exists_raise(db=db, filter=get_user_username_filter)

        obj_data = db_user.__table__.columns.keys()

        user_update_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user_update_data:
            password = user_update_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashedPassword"] = hashed_password
            user_update_data.pop("password")
            user_update_data.update(extra_data)
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
    ) -> model_User | list[model_User] | None:
        """Get user by filter

        Args:
            db (Session): DB session
            filter (dict): Filter map

        Returns:
            model_User | None: model_User object or None
        """
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
        session_user = self.get(db=db, filter=username_map)
        if not session_user:
            return None
        return session_user.email

    def authenticate(
        self,
        db: Session,
        *,
        email_or_username: EmailStr | str | None,
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
        if email_or_username is not None:
            if "@" in email_or_username:
                get_user_filter["email"] = email_or_username
            else:
                get_user_filter["username"] = email_or_username

        db_user = self.get(db=db, filter=get_user_filter)
        if not db_user or not verify_password(password, db_user.hashedPassword):
            return None
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
            raise DbObjectDoesNotExistError(
                model_table_name=model_User.__tablename__,
                filter={"userId": db_user.userId},
                function_name=self.set_active.__name__,
                class_name=self.__class__.__name__,
            )
        db_user.isActive = active
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        self.validate(db_user)
        return db_user

    def update_password(
        self, db: Session, *, db_user: model_User, body: UpdatePassword
    ) -> model_User:
        """Update user password

        Args:
            db (Session): DB session
            db_user (model_User): User object
            body (UpdatePassword): Password data

        Returns:
            model_User: Updated user
        """
        if not verify_password(body.current_password, db_user.hashedPassword):
            raise InvalidPasswordError(
                function_name=self.update_password.__name__,
                class_name=self.__class__.__name__,
            )
        if body.current_password == body.new_password:
            raise NewPasswordIsSameError(
                function_name=self.update_password.__name__,
                class_name=self.__class__.__name__,
            )
        hashed_password = get_password_hash(body.new_password)
        db_user.hashedPassword = hashed_password
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        self.validate(db_user)
        return db_user
