import datetime as _dt
import pydantic as _pydantic


# Shared hashed user ip props
class _BaseTemporaryHashedUserIP(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    hashedIp: str


# Properties to receive on hashed user ip creation
class TemporaryHashedUserIpCreate(_BaseTemporaryHashedUserIP):
    pass


# Properties shared by models stored in DB
class TemporaryHashedUserIpInDBBase(_BaseTemporaryHashedUserIP):
    createdAt: _dt.datetime


# Properties to return to client
class TemporaryHashedUserIp(_BaseTemporaryHashedUserIP):
    pass


# Properties stored in DB
class TemporaryHashedUserIpInDB(_BaseTemporaryHashedUserIP):
    pass
