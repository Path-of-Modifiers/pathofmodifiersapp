import datetime as _dt

import pydantic as _pydantic


# Shared currency props
class _BaseCurrency(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    tradeName: str
    valueInChaos: float
    iconUrl: str


# Properties to receive on currency creation
class CurrencyCreate(_BaseCurrency):
    pass


# Properties to receive on update
class CurrencyUpdate(_BaseCurrency):
    pass


# Properties shared by models stored in DB
class CurrencyInDBBase(_BaseCurrency):
    createdAt: _dt.datetime
    currencyId: int


# Properties to return to client
class Currency(CurrencyInDBBase):
    pass


# Properties stored in DB
class CurrencyInDB(CurrencyInDBBase):
    pass
