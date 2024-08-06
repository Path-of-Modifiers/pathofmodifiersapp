import datetime as _dt
from typing import Optional, List
import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: List[float]
    timeStamp: List[_dt.datetime]
    mostCommonCurrencyUsed: str
    conversionValue: List[float]
