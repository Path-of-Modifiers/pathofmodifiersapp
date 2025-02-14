from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.schemas.item_base_type import ItemBaseTypeCreate
from app.tests.utils.utils import random_int, random_lower_string


def create_random_item_base_type_dict() -> dict:
    """Create a random item base type dictionary.

    Returns:
        Dict: Item base type dictionary with random values.
    """
    baseType = random_lower_string()
    category = random_lower_string()
    subCategory = random_lower_string()
    relatedUniques = "|".join(
        [random_lower_string() for _ in range(random_int(max_value=3))]
    )

    item_base_type = {
        "baseType": baseType,
        "category": category,
        "subCategory": subCategory,
        "relatedUniques": relatedUniques,
    }

    return item_base_type


async def generate_random_item_base_type(
    db: Session,
) -> tuple[dict, model_ItemBaseType]:
    """Generate a random item base type.

    Args:
        db (Session): DB session.

    Returns:
        Tuple[Dict, ItemBaseType]: Random item base type dict and ItemBaseType db object.
    """
    item_base_type_dict = create_random_item_base_type_dict()
    item_base_type_create = ItemBaseTypeCreate(**item_base_type_dict)
    item_base_type = await crud.CRUD_itemBaseType.create(
        db, obj_in=item_base_type_create
    )

    return item_base_type_dict, item_base_type
