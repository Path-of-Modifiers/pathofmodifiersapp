import datetime as _dt
from typing import Optional
import pydantic as _pydantic


# Shared modifier props
class _BaseModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    modifierId: int
    position: int
    minRoll: Optional[float]
    maxRoll: Optional[float]
    textRoll: Optional[str]
    static: Optional[bool]
    effect: str
    regex: Optional[str]
    implicit: Optional[bool]
    explicit: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    corrupted: Optional[bool]
    enchanted: Optional[bool]
    veiled: Optional[bool]


# Properties to receive on modifier creation
class ModifierCreate(_BaseModifier):
    pass


# Properties to receive on update
class ModifierUpdate(_BaseModifier):
    pass


# Properties shared by models stored in DB
class ModifierInDBBase(_BaseModifier):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]


# Properties to return to client
class Modifier(ModifierInDBBase):
    pass


# Properties stored in DB
class ModifierInDB(ModifierInDBBase):
    pass
