from typing import List

from sqlalchemy import func
from app import crud

from sqlalchemy.orm import Session

from app import crud
from app.core.models.models import Item
from app.core.schemas.item import ItemCreate
from backend.app.app.tests.utils.utils import random_lower_string
from backend.app.app.tests.utils.utils import random_int
from backend.app.app.tests.utils.utils import random_bool
from backend.app.app.tests.utils.utils import random_float
from backend.app.app.tests.utils.utils import random_json
from backend.app.app.tests.utils.utils import random_url


async def create_random_item(db: Session) -> Item:
    gameItemId =random_lower_string()
    stashId =random_lower_string()
    name =random_lower_string()
    iconUrl =random_url()
    league = random_lower_string()
    typeLine = random_lower_string()
    baseType = random_lower_string()
    rarity = random_lower_string()
    identified = random_bool()
    itemLevel = random_int(small_int=True)
    forumNote = random_lower_string()
    currencyAmount = random_float()
    currencyId = random_int()
    corrupted = random_bool()
    delve = random_bool()
    fractured = random_bool()
    synthesized = random_bool()
    replica = random_bool()
    elder = random_bool()
    shaper = random_bool()
    influences = random_json()
    searing = random_bool()
    tangled = random_bool()
    isRelic = random_bool()
    prefixes = random_int(small_int=True)
    suffixes = random_int(small_int=True)
    foilVariation = random_int()
    inventoryId = random_lower_string()
    
    item_in = ItemCreate(
        gameItemId=gameItemId,
        stashId=stashId,
        name=name,
        iconUrl=iconUrl,
        league=league,
        typeLine=typeLine,
        baseType=baseType,
        rarity=rarity,
        identified=identified,
        itemLevel=itemLevel,
        forumNote=forumNote,
        currencyAmount=currencyAmount,
        currencyId=currencyId,
        corrupted=corrupted,
        delve=delve,
        fractured=fractured,
        synthesized=synthesized,
        replica=replica,
        elder=elder,
        shaper=shaper,
        influences=influences,
        searing=searing,
        tangled=tangled,
        isRelic=isRelic,
        prefixes=prefixes,
        suffixes=suffixes,
        foilVariation=foilVariation,
        inventoryId=inventoryId,
    )
    return await crud.CRUD_item.create(db=db, obj_in=item_in)


def create_random_item_list(db: Session, count: int = 10) -> List[Item]:
    return [create_random_item(db) for _ in range(count)]


async def get_random_item(session: Session) -> Item:
    random_item = session.query(Item).order_by(func.random()).first()

    if random_item:
        print(
            f"Found already existing item. random_item.gameItemId: {random_item.gameItemId}"
        )
    else:
        random_item = create_random_item(session)
    return random_item