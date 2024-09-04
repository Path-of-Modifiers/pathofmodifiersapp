import datetime as _dt

import pydantic as _pydantic


# Shared modifier props
class _BaseModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    position: int
    relatedUniques: str
    minRoll: float | None = None
    maxRoll: float | None = None
    textRolls: str | None = None
    static: bool | None = None
    effect: str
    regex: str | None = None
    implicit: bool | None = None
    explicit: bool | None = None
    delve: bool | None = None
    fractured: bool | None = None
    synthesized: bool | None = None
    unique: bool | None = None
    corrupted: bool | None = None
    enchanted: bool | None = None
    veiled: bool | None = None


class GroupedModifierByEffect(_pydantic.BaseModel):
    modifierId: list[int]
    position: list[int]
    minRoll: list[float | None]
    maxRoll: list[float | None]
    textRolls: list[str | None]
    effect: str
    static: list[bool | None]


# Properties to receive on modifier creation
class ModifierCreate(_BaseModifier):
    modifierId: int | None = None


# Properties to receive on update
class ModifierUpdate(_BaseModifier):
    pass


# Properties shared by models stored in DB
class ModifierInDBBase(_BaseModifier):
    modifierId: int
    createdAt: _dt.datetime
    updatedAt: _dt.datetime | None = None


# Properties to return to client
class Modifier(ModifierInDBBase):
    pass


# Properties stored in DB
class ModifierInDB(ModifierInDBBase):
    pass
