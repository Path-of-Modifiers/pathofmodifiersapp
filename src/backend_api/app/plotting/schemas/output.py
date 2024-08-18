import datetime as _dt

import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: list[float]
    timeStamp: list[_dt.datetime]
    mostCommonCurrencyUsed: str
    conversionValue: list[float]
