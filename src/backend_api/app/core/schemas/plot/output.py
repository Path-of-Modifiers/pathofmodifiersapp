from typing import Literal

import pydantic as _pydantic


class PlotData(_pydantic.BaseModel):
    valueInChaos: list[float]
    hoursSinceLaunch: list[int]
    valueInMostCommonCurrencyUsed: list[float]
    confidence: list[Literal["low", "medium", "high"]]
    confidenceRating: Literal["low", "medium", "high"]
    mostCommonCurrencyUsed: str
