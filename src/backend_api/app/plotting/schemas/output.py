import datetime as _dt

import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: list[float]
    timeStamp: list[_dt.datetime]
    valueInMostCommonCurrencyUsed: list[float]
    mostCommonCurrencyUsed: str
