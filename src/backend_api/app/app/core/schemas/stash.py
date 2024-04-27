import datetime as _dt
from typing import Optional
import pydantic as _pydantic


# Shared stash props
class _BaseStash(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    accountName: str
    public: bool
    league: str


# Properties to receive on stash creation
class StashCreate(_BaseStash):
    stashId: str


# Properties to receive on update
class StashUpdate(_BaseStash):
    pass


# Properties shared by models stored in DB
class StashInDBBase(_BaseStash):
    stashId: str
    createdAt: _dt.datetime
    updatedAt: Optional[_dt.datetime] = None


# Properties to return to client
class Stash(StashInDBBase):
    pass


# Properties stored in DB
class StashInDB(StashInDBBase):
    pass
