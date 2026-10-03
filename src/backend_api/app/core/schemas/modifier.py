import re

import pydantic as _pydantic


# Shared modifier props
class ModifierBase(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True, extra="ignore")

    relatedUniques: str | None = None

    static: bool | None = None
    effect: str
    regex: re.Pattern | None = None

    implicit: bool | None = None
    explicit: bool | None = None
    delve: bool | None = None
    fractured: bool | None = None
    synthesised: bool | None = None
    unique: bool | None = None
    corrupted: bool | None = None
    enchanted: bool | None = None
    veiled: bool | None = None

    @_pydantic.field_validator("regex", mode="before")
    @classmethod
    def compile_regex(cls, value: str | None) -> re.Pattern:
        if value is None:
            return None
        elif isinstance(value, str):
            return re.compile(value)

        return value

    @_pydantic.field_serializer("regex")
    def serialize_regex(self, regex: re.Pattern | None) -> str | None:
        if regex is None:
            return None
        elif isinstance(regex, str):
            return regex
        else:
            return regex.pattern


class ModifierRoll(_pydantic.BaseModel):
    position: int
    minRoll: float | None = None
    maxRoll: float | None = None
    textRolls: list[str] | None = None


# Properties to receive on modifier creation
class ModifierCreate(ModifierBase):
    rolls: list[ModifierRoll] = _pydantic.Field(default_factory=list)


# Properties to return to client
class Modifier(ModifierBase):
    modifierId: int


class GroupedModifier(Modifier):
    rolls: list[ModifierRoll]


class ModifierUpdate(Modifier):
    rolls: list[ModifierRoll] | None = None
    effect: str | None = None
