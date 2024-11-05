import datetime as _dt

import pydantic as _pydantic


# Shared item modifier props
class _BaseItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    modifierId: int
    orderId: int
    position: int
    roll: float | None = None


# Properties to receive on item modifier creation
class ItemModifierCreate(_BaseItemModifier):
    createdAt: _dt.datetime | None = None


# Properties to receive on update
class ItemModifierUpdate(_BaseItemModifier):
    pass


# Properties shared by models stored in DB
class ItemModifierInDBBase(_BaseItemModifier):
    createdAt: _dt.datetime
    updatedAt: _dt.datetime | None = None


# Properties to return to client
class ItemModifier(ItemModifierInDBBase):
    pass


# Properties stored in DB
class ItemModifierInDB(ItemModifierInDBBase):
    pass
