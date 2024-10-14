import datetime as _dt

import pydantic as _pydantic


# Shared account props
class _BaseAccount(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    accountName: str
    isBanned: bool | None = None


# Properties to receive on account creation
class AccountCreate(_BaseAccount):
    pass


# Properties to receive on update
class AccountUpdate(_BaseAccount):
    pass


# Properties shared by models stored in DB
class AccountInDBBase(_BaseAccount):
    createdAt: _dt.datetime
    updatedAt: _dt.datetime | None = None


# Properties to return to client
class Account(AccountInDBBase):
    pass


# Properties stored in DB
class AccountInDB(AccountInDBBase):
    pass
