from backend_api.app.core.schemas.modifier import GroupedModifier

from data_retrieval_app.utils import (
    get_grouped_modifiers_by_unique,
    get_item_base_types,
)


def get_uniques(modifiers_by_unique: dict[str, list[GroupedModifier]]) -> list[str]:
    if not modifiers_by_unique:
        raise ValueError("No unique items available")

    return list(modifiers_by_unique.keys())


def get_modifiers_by_unique(headers: dict):
    db_modifiers = get_grouped_modifiers_by_unique(headers)

    modifiers_by_unique = {
        unique: [{"description": modifier.effect} for modifier in modifiers]
        for unique, modifiers in db_modifiers.items()
    }
    return modifiers_by_unique


def get_bases(headers: dict) -> dict[str, str]:
    base_types = get_item_base_types(headers)

    base_type_by_name = dict[str, str]()

    for bt in base_types:
        if bt.relatedUniques is None:
            continue

        uniques = bt.relatedUniques.split("|")
        for unique in uniques:
            base_type_by_name[unique] = bt.baseType

    return base_type_by_name
