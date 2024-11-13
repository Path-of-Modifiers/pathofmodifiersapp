import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: list[float]
    hoursSinceLaunch: list[int]
    valueInMostCommonCurrencyUsed: list[float]
    mostCommonCurrencyUsed: str
