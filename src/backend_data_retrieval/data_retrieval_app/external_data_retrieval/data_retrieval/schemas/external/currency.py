from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CurrencyModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )


class ExchangeRatioSide(BaseModel):
    chaosValue: float | None = None


class ExchangeRatioItem(BaseModel):
    id: int

    name: str
    category: str
    leagueId: int  # supplied internally from DB

    chaos: ExchangeRatioSide
    divine: ExchangeRatioSide
