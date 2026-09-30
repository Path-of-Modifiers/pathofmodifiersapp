import pydantic as _pydantic


# Shared item modifier props
class ItemModifier(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    itemId: int
    modifierId: int
    position: int
    roll: float | None = None


class ItemModifierRoll(_pydantic.BaseModel):
    position: int
    roll: float | None = None


class ItemModifierCreate(_pydantic.BaseModel):
    modifierId: int

    rolls: list[ItemModifierRoll]
