from sqlalchemy.orm import Session

from app import crud
from app.core.schemas.item_base_type import ItemBaseTypeUpdate, ItemBaseTypeCreate
from backend.app.app.tests.utils.model_utils.item_base_type import (
    create_random_itemBaseType,
    create_random_itemBaseType_list,
)
from backend.app.app.tests.utils.utils import (
    random_float,
    random_lower_string,
    random_url,
)


async def test_create_itemBaseType(db: Session) -> None:
    itemBaseType = await create_random_itemBaseType(db)
    stored_created_itemBaseType = await crud.CRUD_itemBaseType.create(
        db, obj_in=itemBaseType
    )
    assert stored_created_itemBaseType
    assert stored_created_itemBaseType.baseType == itemBaseType.baseType
    assert stored_created_itemBaseType.category == itemBaseType.category
    assert stored_created_itemBaseType.subCategory == itemBaseType.subCategory


async def test_create_multiple_itemBaseTypes(db: Session) -> None:
    # Get the initial count of stored itemBaseTypes
    initial_itemBaseType_count = len(await crud.CRUD_itemBaseType.get(db))

    # Create random itemBaseTypes
    itemBaseTypes = await create_random_itemBaseType_list(db=db, count=5)

    # Get the final count of stored itemBaseTypes
    stored_itemBaseTypes = await crud.CRUD_itemBaseType.get(db)
    final_itemBaseType_count = len(stored_itemBaseTypes)

    # Ensure the total count matches the expected count
    assert final_itemBaseType_count == initial_itemBaseType_count + 5

    # Check that the newly created itemBaseTypes are in the stored itemBaseTypes
    for stored_itemBaseType in stored_itemBaseTypes:
        if stored_itemBaseType not in itemBaseTypes:
            assert stored_itemBaseType
            assert stored_itemBaseType in await crud.CRUD_itemBaseType.get(db)


async def get_all_itemBaseType(db: Session) -> None:
    itemBaseType = await create_random_itemBaseType(db)
    itemBaseType_map = {"baseType": itemBaseType.baseType}
    stored_itemBaseType = await crud.CRUD_itemBaseType.get(db, filter=itemBaseType_map)
    assert stored_itemBaseType
    all_itemBaseTypes = await crud.CRUD_itemBaseType.get(db)
    assert stored_itemBaseType in all_itemBaseTypes