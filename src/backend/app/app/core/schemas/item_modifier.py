from typing import Optional
import pydantic as _pydantic


# Shared item modifier props
class _BaseItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    gameItemId: str
    modifierId: int
    position: int
    range: Optional[float]


# Properties to receive on item modifier creation
class CreateItemModifier(_BaseItemModifier):
    pass


# Properties to receive on update
class UpdateItemModifier(_BaseItemModifier):
    pass


# Properties shared by models stored in DB
class ItemModifierInDBBase(_BaseItemModifier):
    id: int


# Properties to return to client
class ItemModifier(ItemModifierInDBBase):
    pass


# Properties stored in DB
class ItemModifierInDB(ItemModifierInDBBase):
    pass
