import datetime as _dt
from typing import Optional
import pydantic as _pydantic


# Shared account props
class _BaseAccount(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    accountName: str
    isBanned: Optional[bool]


# Properties to receive on account creation
class CreateAccount(_BaseAccount):
    pass


# Properties to receive on update
class UpdateAccount(_BaseAccount):
    pass


# Properties shared by models stored in DB
class AccountInDBBase(_BaseAccount):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]
    id: int


# Properties to return to client
class Account(AccountInDBBase):
    pass


# Properties stored in DB
class AccountInDB(AccountInDBBase):
    pass
