import datetime as _dt

import pydantic as _pydantic


# Shared League props
class _BaseLeague(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str
    validFrom: _dt.datetime
    validTo: _dt.datetime | None = None
    version: float


# Properties to receive on League creation
class LeagueCreate(_BaseLeague):
    pass


# Properties to receive on update
class LeagueUpdate(_BaseLeague):
    leagueId: int


# Properties shared by models stored in DB
class LeagueInDBBase(_BaseLeague):
    leagueId: int


# Properties to return to client
class League(LeagueInDBBase):
    pass


# Properties stored in DB
class LeagueInDB(LeagueInDBBase):
    pass
