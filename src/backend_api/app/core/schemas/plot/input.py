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
    synthesized: bool | None = None
    replica: bool | None = None
    influences: Influences | None = None
    searing: bool | None = None
    tangled: bool | None = None
    isRelic: bool | None = None
    foilVariation: int | None = None


class BaseSpecs(_pydantic.BaseModel):
    baseType: str | None = None
    category: str | None = None
    subCategory: str | None = None


class ModifierLimitations(_pydantic.BaseModel):
    maxRoll: float | None = None
    minRoll: float | None = None
    textRoll: int | None = None


class WantedModifier(_pydantic.BaseModel):
    modifierId: int
    modifierLimitations: ModifierLimitations | None = None


class PlotQuery(_pydantic.BaseModel):
    league: str
    itemSpecifications: ItemSpecs | None = None
    baseSpecifications: BaseSpecs | None = None
    wantedModifiers: list[WantedModifier]
