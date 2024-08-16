from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
import uuid


# Shared properties
class _BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    hashedPassword: str
    isActive: Optional[bool] = True
    isSuperuser: Optional[bool] = False
    rateLimitTier: Optional[int] = 0
    isBanned: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(_BaseUser):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


# Properties to receive via API on update, all are optional
class UserUpdate(_BaseUser):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=255)


class UpdatePassword(BaseModel):
    currentPassword: str = Field(min_length=8, max_length=40)
    newPassword: str = Field(min_length=8, max_length=40)


# Properties to return via API, id is always required
class UserPublic(_BaseUser):
    userId: uuid.UUID


# Properties on multiple users
class UsersPublic(BaseModel):
    data: List[UserPublic]
    count: int


# Properties to return to client
class UserInDBBase(_BaseUser):
    userId: uuid.UUID
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


# Properties returned to client
class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
