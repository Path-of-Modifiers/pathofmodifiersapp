import pydantic as _pydantic


# Shared currency props
class _BaseCurrency(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    tradeName: str
    valueInChaos: float
    leagueId: int


# Properties to receive on currency creation
class CurrencyCreate(_BaseCurrency):
    createdHoursSinceLaunch: int


# Properties to receive on update
class CurrencyUpdate(_BaseCurrency):
    pass


# Properties shared by models stored in DB
class CurrencyInDBBase(_BaseCurrency):
    createdHoursSinceLaunch: int
    currencyId: int


# Properties to return to client
class Currency(CurrencyInDBBase):
    pass


# Properties stored in DB
class CurrencyInDB(CurrencyInDBBase):
    pass


class CurrencyQuery(_pydantic.BaseModel):
    createdHoursSinceLaunch: int | None = None
    tradeName: str | None = None
    leagueId: int | None = None
