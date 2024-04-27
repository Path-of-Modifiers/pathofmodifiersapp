from typing import Optional, List
import pydantic as _pydantic

from app.core.schemas.item import Influences


class ItemSpecs(_pydantic.BaseModel):
    name: Optional[str] = None
    identified: Optional[bool] = None
    ilvl: Optional[int] = None
    rarity: Optional[str] = None
    corrupted: Optional[bool] = None
    delve: Optional[bool] = None
    fractured: Optional[bool] = None
    synthesized: Optional[bool] = None
    replica: Optional[bool] = None
    influences: Optional[Influences] = None
    searing: Optional[bool] = None
    tangled: Optional[bool] = None
    isRelic: Optional[bool] = None
    foilVariation: Optional[int] = None


class BaseSpecs(_pydantic.BaseModel):
    baseType: Optional[str] = None
    category: Optional[str] = None
    subCategory: Optional[str] = None


class ModifierLimitations(_pydantic.BaseModel):
    maxRoll: Optional[float] = None
    minRoll: Optional[float] = None
    textRoll: Optional[int] = None


class WantedModifier(_pydantic.BaseModel):
    modifierId: int
    position: int
    modifierLimitations: Optional[ModifierLimitations] = None


class PlotQuery(_pydantic.BaseModel):
    league: str
    itemSpecifications: ItemSpecs
    baseSpecifications: Optional[BaseSpecs] = None
    wantedModifiers: List[WantedModifier]
