import pydantic as _pydantic

from app.core.schemas.item import Influences


class ItemSpecs(_pydantic.BaseModel):
    name: str | None = None
    identified: bool | None = None
    minIlvl: int | None = None
    maxIlvl: int | None = None
    rarity: str | None = None
    corrupted: bool | None = None
    delve: bool | None = None
    fractured: bool | None = None
    synthesised: bool | None = None
    replica: bool | None = None
    influences: Influences | None = None
    searing: bool | None = None
    tangled: bool | None = None
    foilVariation: int | None = None


class BaseSpecs(_pydantic.BaseModel):
    itemBaseTypeId: int | None = None
    category: str | None = None
    subCategory: str | None = None


class ModifierLimitations(_pydantic.BaseModel):
    maxRoll: float | None = None
    minRoll: float | None = None
    textRoll: int | None = None


class WantedModifier(_pydantic.BaseModel):
    modifierId: int
    modifierLimitations: ModifierLimitations | None = None


class BasePlotQuery(_pydantic.BaseModel):
    league: list[str] | str
    itemSpecifications: ItemSpecs | None = None
    baseSpecifications: BaseSpecs | None = None
    end: int | None = None
    start: int | None = None


class PlotQuery(BasePlotQuery):
    "Plots for items with or without modifiers"

    wantedModifiers: list[list[WantedModifier]] | None = None
    dataPointsPerHour: int = 5


class IdentifiedPlotQuery(BasePlotQuery):
    "Plots for items with modifiers"

    wantedModifiers: list[list[WantedModifier]]
    dataPointsPerHour: int = 5


class UnidentifiedPlotQuery(BasePlotQuery):
    """Plots for unidentified items"""
