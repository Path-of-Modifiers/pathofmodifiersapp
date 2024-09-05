from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import (
    Account,
    Currency,
    Item,
    ItemBaseType,
    ItemModifier,
    Modifier,
    Stash,
)
from app.core.schemas.item_modifier import ItemModifierCreate
from app.tests.utils.model_utils.item import generate_random_item
from app.tests.utils.model_utils.modifier import generate_random_modifier
from app.tests.utils.utils import random_float, random_int


async def create_random_item_modifier_dict(
    db: Session, retrieve_dependencies: bool | None = False
) -> (
    dict
    | tuple[
        dict,
        list[dict | Stash | Account | ItemBaseType | Currency | Item | Modifier] | None,
    ]
):
    """Create a random item modifier dictionary.

    Args:
        db (Session): DB session.
        retrieve_dependencies (bool | None): Whether to retrieve dependencies. Defaults to False.


    Returns:
        _type_: Random item modifier dictionary or tuple containing the dictionary and optional dependencies.
    """
    roll_value = random_float()

    # Set the dependencies
    if not retrieve_dependencies:
        item_dict, item = await generate_random_item(db)
    else:
        item_dict, item, deps = await generate_random_item(
            db, retrieve_dependencies=retrieve_dependencies
        )
    itemId = item.itemId
    modifier_dict, modifier = await generate_random_modifier(db)
    modifierId = modifier.modifierId
    position = modifier.position
    textRollId = random_int()

    item_modifier_dict = {
        "itemId": itemId,
        "modifierId": modifierId,
        "position": position,
        "roll": roll_value,
        "textRollId": textRollId,
    }
    if not retrieve_dependencies:
        return item_modifier_dict
    else:  # Gather dependencies and return
        deps += [item_dict, item, modifier_dict, modifier]
        return item_modifier_dict, deps


async def generate_random_item_modifier(
    db: Session, retrieve_dependencies: bool | None = False
) -> tuple[
    dict,
    ItemModifier,
    list[dict | Stash | Account | ItemBaseType | Currency | Item | Modifier] | None,
]:
    """Generate a random item modifier.

    Args:
        db (Session): DB session.
        retrieve_dependencies (bool, optional): Whether to retrieve dependencies. Defaults to False.

    Returns:
        Tuple[ Dict, ItemModifier, List[Union[Dict, Stash, Account, ItemBaseType, Currency, Item, Modifier]]], ]: \n
        Random item modifier dictionary, ItemModifier db object and optional dependencies.
    """
    output = await create_random_item_modifier_dict(db, retrieve_dependencies)
    if not retrieve_dependencies:
        item_modifier_dict = output
    else:
        item_modifier_dict, deps = output
    item_modifier_create = ItemModifierCreate(**item_modifier_dict)
    item_modifier = await crud.CRUD_itemModifier.create(db, obj_in=item_modifier_create)

    if not retrieve_dependencies:
        return item_modifier_dict, item_modifier
    else:
        return item_modifier_dict, item_modifier, deps
