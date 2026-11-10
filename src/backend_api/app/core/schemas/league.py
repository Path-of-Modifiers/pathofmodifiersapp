import pydantic as _pydantic


# Shared League props
class _BaseLeague(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str
    validFrom: _pydantic.AwareDatetime
    validTo: _pydantic.AwareDatetime | None = None
    version: float

    @_pydantic.field_serializer("validFrom", "validTo")
    def serialize_valid_from(self, value: _pydantic.AwareDatetime | None) -> str:
        if value is None:
            return None
        return value.isoformat()


# Properties to receive on League creation
class LeagueCreate(_BaseLeague):
    pass


# Properties to receive on update
class LeagueUpdate(_BaseLeague):
    leagueId: int

    name: str | None = None
    validFrom: _pydantic.AwareDatetime | None = None
    validTo: _pydantic.AwareDatetime | None = None
    version: float | None = None


# Properties shared by models stored in DB
class LeagueInDBBase(_BaseLeague):
    leagueId: int


# Properties to return to client
class League(LeagueInDBBase):
    pass


# Properties stored in DB
class LeagueInDB(LeagueInDBBase):
    pass
