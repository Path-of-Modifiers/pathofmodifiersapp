import datetime as _dt
import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: List[float]
    timeStamp: List[_dt.datetime]
    valueInMostCommonCurrencyUsed: List[float]
    mostCommonCurrencyUsed: str
