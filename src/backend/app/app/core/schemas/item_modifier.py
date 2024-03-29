from typing import Optional
import pydantic as _pydantic
import datetime as _dt


# Shared item modifier props
class _BaseItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    modifierId: int
    position: int
    roll: Optional[float] = None


# Properties to receive on item modifier creation
class ItemModifierCreate(_BaseItemModifier):
    pass


# Properties to receive on update
class ItemModifierUpdate(_BaseItemModifier):
    pass


# Properties shared by models stored in DB
class ItemModifierInDBBase(_BaseItemModifier):
    createdAt: _dt.datetime
    updatedAt: _dt.datetime


# Properties to return to client
class ItemModifier(ItemModifierInDBBase):
    pass


# Properties stored in DB
class ItemModifierInDB(ItemModifierInDBBase):
    pass
