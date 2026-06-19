from pydantic import BaseModel


class ModifierSchema(BaseModel):
    modifierId: int
    position: int
    minRoll: int
    maxRoll: int
    implicit: bool
    explicit: bool
    delve: bool
    fractured: bool
    synthesised: bool
    unique: bool
    corrupted: bool
    enchanted: bool
    veiled: bool
    static: bool
    effect: str
    relatedUniques: str
    textRolls: str
    regex: str
    dynamicallyCreated: bool


class CaranteneModifierSchema(BaseModel):
    effect: str
    relatedUnique: str
    implicit: str
    explicit: str
    delve: str
    fractured: str
    synthesised: str
    unique: str
    corrupted: str
    enchanted: str
    veiled: str
    mutated: str
