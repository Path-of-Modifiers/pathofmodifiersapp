import uuid
from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
)

from app.core.schemas.wrap_validator import custom_error_msg


class UsernameValidationError(ValueError):
    @classmethod
    def from_validator_exc(
        cls,
        field_name: str | None,
        exc: Exception | None,
    ) -> Exception:
        return cls(
            f"The field {field_name} can not contain special symbols or white/empty space.",
        )


string_username_pattern = r"^[\p{L}\p{N}_]+$"

UsernameStr = Annotated[
    str,
    StringConstraints(pattern=string_username_pattern),
    custom_error_msg(UsernameValidationError.from_validator_exc),
]


# Shared properties
class _BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: UsernameStr
    email: EmailStr
    isActive: bool | None = True
    isSuperuser: bool | None = False
    rateLimitTier: int | None = 0
    isBanned: bool | None = False


# Properties to receive via API on creation
class UserCreate(_BaseUser):
    password: str = Field(min_length=8)


class UserRegisterPreEmailConfirmation(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: str = Field(min_length=8)


class UserRegisterPostEmailConfirmation(BaseModel):
    token: str


# Properties to receive via API on update, all are optional
class UserUpdate(_BaseUser):
    email: EmailStr | None = None
    username: UsernameStr | None = None
    password: str | None = Field(default=None, min_length=8)


class UserUpdateMe(BaseModel):
    email: EmailStr | None = None
    username: UsernameStr | None = None


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)


class UserInCache(_BaseUser):
    userId: uuid.UUID


# Properties to return via API, id is always required
class UserPublic(_BaseUser):
    userId: uuid.UUID


# Properties on multiple users
class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


# Properties to return to client
class UserInDBBase(_BaseUser):
    userId: uuid.UUID
    hashedPassword: str
    createdAt: datetime | None
    updatedAt: datetime | None


# Properties returned to client
class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
