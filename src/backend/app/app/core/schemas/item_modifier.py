from typing import Optional
import pydantic as _pydantic


# Shared item modifier props
class _BaseItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    gameItemId: str
    modifierId: int
    position: int
    range: Optional[float] = None


# Properties to receive on item modifier creation
class ItemModifierCreate(_BaseItemModifier):
    pass


# Properties to receive on update
class ItemModifierUpdate(_BaseItemModifier):
    pass


# Properties shared by models stored in DB
class ItemModifierInDBBase(_BaseItemModifier):
    createdAt: _pydantic.datetime.datetime
    updatedAt: _pydantic.datetime.datetime


# Properties to return to client
class ItemModifier(ItemModifierInDBBase):
    pass


# Properties stored in DB
class ItemModifierInDB(ItemModifierInDBBase):
    pass
