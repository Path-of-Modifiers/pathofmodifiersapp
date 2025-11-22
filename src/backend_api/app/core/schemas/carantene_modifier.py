import datetime as _dt

import pydantic as _pydantic


# Shared modifier props
class _BaseCaranteneModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    effect: str
    relatedUnique: str
    implicit: bool | None = None
    explicit: bool | None = None
    delve: bool | None = None
    fractured: bool | None = None
    synthesised: bool | None = None
    unique: bool | None = None
    corrupted: bool | None = None
    enchanted: bool | None = None
    veiled: bool | None = None
    mutated: bool | None = None


# Properties to receive on modifier creation
class CaranteneModifierCreate(_BaseCaranteneModifier):
    pass


# Properties to receive on update
class CaranteneModifierUpdate(_BaseCaranteneModifier):
    pass


# Properties shared by models stored in DB
class CaranteneModifierInDBBase(_BaseCaranteneModifier):
    caranteneModifierId: int
    createdAt: _dt.datetime
    updatedAt: _dt.datetime | None = None


# Properties to return to client
class CaranteneModifier(CaranteneModifierInDBBase):
    pass


# Properties stored in DB
class CaranteneModifierInDB(CaranteneModifierInDBBase):
    pass


class CaranteneModifiersPK(_pydantic.BaseModel):
    caranteneModifierId: int
