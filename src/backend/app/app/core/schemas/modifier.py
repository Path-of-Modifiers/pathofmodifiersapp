import datetime as _dt
from typing import Optional
import pydantic as _pydantic


# Shared modifier props
class _BaseModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    modifierId: Optional[int] = None
    position: int
    minRoll: Optional[float] = None
    maxRoll: Optional[float] = None
    textRoll: Optional[str] = None
    static: Optional[bool] = None
    effect: str
    regex: Optional[str] = None
    implicit: Optional[bool] = None
    explicit: Optional[bool] = None
    delve: Optional[bool] = None
    fractured: Optional[bool] = None
    synthesized: Optional[bool] = None
    corrupted: Optional[bool] = None
    enchanted: Optional[bool] = None
    veiled: Optional[bool] = None


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
