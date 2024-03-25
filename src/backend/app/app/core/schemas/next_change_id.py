import datetime as _dt
from typing import Optional
import pydantic as _pydantic


# Shared account props
class _BaseNextChangeId(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    nextChangeId: str


# Properties to receive on account creation
class NextChangeIdCreate(_BaseNextChangeId):
    pass


# Properties to receive on update
class NextChangeIdUpdate(_BaseNextChangeId):
    pass


# Properties shared by models stored in DB
class NextChangeIdInDBBase(_BaseNextChangeId):
    id: int


# Properties to return to client
class NextChangeId(NextChangeIdInDBBase):
    pass


# Properties stored in DB
class NextChangeIdInDB(NextChangeIdInDBBase):
    pass
