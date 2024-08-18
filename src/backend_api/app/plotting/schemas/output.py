import datetime as _dt
from typing import List
import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: List[float]
    timeStamp: List[_dt.datetime]
    valueInMostCommonCurrencyUsed: List[float]
    mostCommonCurrencyUsed: str
