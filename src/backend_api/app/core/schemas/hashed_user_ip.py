import datetime as _dt
import pydantic as _pydantic


# Shared hashed user ip props
class _BaseHashedUserIP(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    hashedIp: str


# Properties to receive on hashed user ip creation
class HashedUserIpCreate(_BaseHashedUserIP):
    pass


class HashedUserIpQuery(_BaseHashedUserIP):
    pass


# Properties shared by models stored in DB
class HashedUserIpInDBBase(_BaseHashedUserIP):
    createdAt: _dt.datetime


# Properties to return to client
class HashedUserIp(_BaseHashedUserIP):
    pass


# Properties stored in DB
class HashedUserIpInDB(_BaseHashedUserIP):
    pass
