import pydantic as _pydantic


# Shared currency props
class _BaseCurrencyPrice(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    currencyId: int
    leagueId: int
    createdHoursSinceLaunch: int
    valueInChaos: float


# Properties to receive on currency creation
class CurrencyPriceCreate(_BaseCurrencyPrice):
    pass


# Properties to receive on update
class CurrencyPriceUpdate(_BaseCurrencyPrice):
    pass


# Properties shared by models stored in DB
class CurrencyPriceInDBBase(_BaseCurrencyPrice):
    pass


# Properties to return to client
class CurrencyPrice(CurrencyPriceInDBBase):
    pass


# Properties stored in DB
class CurrencyPriceInDB(CurrencyPriceInDBBase):
    pass


# Shared currency props
class _BaseCurrencyType(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str
    tradeName: str


# Properties to receive on currency creation
class CurrencyTypeCreate(_BaseCurrencyType):
    pass


# Properties to receive on update
class CurrencyTypeUpdate(_BaseCurrencyType):
    currencyId: int


# Properties shared by models stored in DB
class CurrencyTypeInDBBase(_BaseCurrencyType):
    currencyId: int


# Properties to return to client
class CurrencyType(CurrencyTypeInDBBase):
    pass


# Properties stored in DB
class CurrencyTypeInDB(CurrencyTypeInDBBase):
    pass


class Currency(_pydantic.BaseModel):
    currencyId: int
    tradeName: str
    name: str

    leagueId: int
    createdHoursSinceLaunch: int
    valueInChaos: float


class CurrencyQuery(_pydantic.BaseModel):
    createdHoursSinceLaunch: int | None = None
    currencyId: int | None = None
    tradeName: str | None = None
    leagueId: int | None = None
