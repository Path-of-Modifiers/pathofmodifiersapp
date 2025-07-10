from typing import Literal

import pydantic as _pydantic


class Datum(_pydantic.BaseModel):
    hoursSinceLaunch: int
    valueInChaos: float
    valueInMostCommonCurrencyUsed: float
    confidence: Literal["low", "medium", "high"]


class TimeseriesData(_pydantic.BaseModel):
    name: str
    data: list[Datum]
    confidenceRating: Literal["low", "medium", "high"]


class PlotData(_pydantic.BaseModel):
    mostCommonCurrencyUsed: str
    data: list[TimeseriesData]
