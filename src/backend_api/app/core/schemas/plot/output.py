import pydantic as _pydantic


class Datum(_pydantic.BaseModel):
    hoursSinceLaunch: int
    valueInChaos: float
    valueInMostCommonCurrencyUsed: float


class LinkedPrices(_pydantic.BaseModel):
    gameItemId: str
    data: list[Datum]


class LeagueData(_pydantic.BaseModel):
    league: str
    linkedPrices: list[LinkedPrices] | None = None
    unlinkedPrices: list[Datum] | None = None


class PlotData(_pydantic.BaseModel):
    mostCommonCurrencyUsed: str
    data: list[LeagueData]
