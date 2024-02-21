from __future__ import annotations
import fastapi as _fastapi
from typing import List, Union, Optional

import app.core.models.models as _models
import app.api.deps as _deps

import app.crud.base as _crud

import app.core.schemas as _schemas


import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Welcome to Path of Modifiers API!"}


CRUD_currency = _crud.CRUDBase[
    _models.Currency,
    _schemas.Currency,
    _schemas.CurrencyCreate,
    _schemas.CurrencyUpdate,
](model=_models.Currency, schema=_schemas.Currency)


@app.post(
    "/api/currency/",
    response_model=Union[_schemas.Currency, List[_schemas.Currency]],
)
async def create_currency(
    currency: Union[_schemas.CurrencyCreate, List[_schemas.CurrencyCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_currency.create(db=db, obj_in=currency)


@app.get(
    "/api/currency/{currencyId}",
    response_model=Union[_schemas.Currency, List[_schemas.Currency]],
)
async def get_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(db=db, filter=currency_map)
    return currency


@app.get(
    "/api/currency/", response_model=Union[_schemas.Currency, List[_schemas.Currency]]
)
async def get_all_currency(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_currency = await CRUD_currency.get(db=db)
    return all_currency


@app.delete("/api/currency/{currencyId}")
async def delete_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_map = {"currencyId": currencyId}
    await CRUD_currency.remove(filter=currency_map, db=db)

    return f"Currency with id {currencyId} deleted successfully"


@app.put("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def update_currency(
    currencyId: int,
    currency_update: _schemas.CurrencyUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    currency_map = {"currencyId": currencyId}
    currency = await CRUD_currency.get(
        db=db,
        filter=currency_map,
    )

    return await CRUD_currency.update(db_obj=currency, obj_in=currency_update, db=db)


CRUD_account = _crud.CRUDBase[
    _models.Account,
    _schemas.Account,
    _schemas.AccountCreate,
    _schemas.AccountUpdate,
](model=_models.Account, schema=_schemas.Account)


@app.post(
    "/api/account/",
    response_model=Union[_schemas.AccountCreate, List[_schemas.AccountCreate]],
)
async def create_account(
    account: Union[_schemas.AccountCreate, List[_schemas.AccountCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_account.create(db=db, obj_in=account)


@app.get(
    "/api/account/{accountName}",
    response_model=Union[_schemas.Account, List[_schemas.Account]],
)
async def get_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    account = await CRUD_account.get(db=db, filter=account_map)
    return account


@app.get(
    "/api/account/", response_model=Union[_schemas.Account, List[_schemas.Account]]
)
async def get_all_accounts(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_accounts = await CRUD_account.get(db=db)
    return all_accounts


@app.delete("/api/account/{accountName}")
async def delete_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    await CRUD_account.remove(db=db, filter=account_map)

    return "Account deleted successfully"


@app.put("/api/account/{accountName}", response_model=_schemas.Account)
async def update_account(
    accountName: str,
    account_update: _schemas.AccountUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    account_map = {"accountName": accountName}
    account = await CRUD_account.get(
        db=db,
        filter=account_map,
    )

    return await CRUD_account.update(db_obj=account, obj_in=account_update, db=db)


CRUD_itemBaseType = _crud.CRUDBase[
    _models.ItemBaseType,
    _schemas.ItemBaseType,
    _schemas.ItemBaseTypeCreate,
    _schemas.ItemBaseTypeUpdate,
](model=_models.ItemBaseType, schema=_schemas.ItemBaseType)


@app.post(
    "/api/itemBaseType/",
    response_model=Union[
        _schemas.ItemBaseTypeCreate, List[_schemas.ItemBaseTypeCreate]
    ],
)
async def create_itemBaseType(
    itemBaseType: Union[_schemas.ItemBaseTypeCreate, List[_schemas.ItemBaseTypeCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_itemBaseType.create(db=db, obj_in=itemBaseType)


@app.get(
    "/api/itemBaseType/{baseType}",
    response_model=Union[_schemas.ItemBaseType, List[_schemas.ItemBaseType]],
)
async def get_itemBaseType(
    baseType: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    itemBaseType_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(db=db, filter=itemBaseType_map)
    return itemBaseType


@app.get(
    "/api/itemBaseType/",
    response_model=Union[_schemas.ItemBaseType, List[_schemas.ItemBaseType]],
)
async def get_all_itemBaseTypes(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_ItemBaseTypes = await CRUD_itemBaseType.get(db=db)
    return all_ItemBaseTypes


@app.delete("/api/itemBaseType/{baseType}")
async def delete_itemBaseType(
    baseType: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    itemBaseType_map = {"baseType": baseType}
    await CRUD_itemBaseType.remove(db=db, filter=itemBaseType_map)

    return "ItemBaseType deleted successfully"


@app.put("/api/itemBaseType/{baseType}", response_model=_schemas.ItemBaseType)
async def update_itemBaseType(
    baseType: str,
    itemBaseType_update: _schemas.ItemBaseTypeUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemBaseType_map = {"baseType": baseType}
    itemBaseType = await CRUD_itemBaseType.get(
        db=db,
        filter=itemBaseType_map,
    )

    return await CRUD_itemBaseType.update(
        db_obj=itemBaseType, obj_in=itemBaseType_update, db=db
    )


CRUD_item = _crud.CRUDBase[
    _models.Item,
    _schemas.Item,
    _schemas.ItemCreate,
    _schemas.ItemUpdate,
](model=_models.Item, schema=_schemas.Item)


@app.post(
    "/api/item/",
    response_model=Union[_schemas.Item, List[_schemas.Item]],
)
async def create_item(
    item: Union[_schemas.ItemCreate, List[_schemas.ItemCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_item.create(db=db, obj_in=item)


@app.get("/api/item/{itemId}", response_model=Union[_schemas.Item, List[_schemas.Item]])
async def get_item(itemId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    item_map = {"itemId": itemId}
    item = await CRUD_item.get(db=db, filter=item_map)
    return item


@app.get("/api/item/", response_model=Union[_schemas.Item, List[_schemas.Item]])
async def get_all_items(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_items = await CRUD_item.get(db=db)
    return all_items


@app.delete("/api/item/{itemId}")
async def delete_item(itemId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    item_map = {"itemId": itemId}
    await CRUD_item.remove(db=db, filter=item_map)

    return "Item deleted successfully"


@app.put("/api/item/{itemId}", response_model=_schemas.Item)
async def update_item(
    itemId: str,
    item_update: _schemas.ItemUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    item_map = {"itemId": itemId}
    item = await CRUD_item.get(
        db=db,
        filter=item_map,
    )

    return await CRUD_item.update(db_obj=item, obj_in=item_update, db=db)


CRUD_stash = _crud.CRUDBase[
    _models.Stash,
    _schemas.Stash,
    _schemas.StashCreate,
    _schemas.StashUpdate,
](model=_models.Stash, schema=_schemas.Stash)


@app.post(
    "/api/stash/",
    response_model=Union[_schemas.StashCreate, List[_schemas.StashCreate]],
)
async def create_stash(
    stash: Union[_schemas.StashCreate, List[_schemas.StashCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_stash.create(db=db, obj_in=stash)


@app.get(
    "/api/stash/{stashId}", response_model=Union[_schemas.Stash, List[_schemas.Stash]]
)
async def get_stash(stashId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(db=db, filter=stash_map)
    return stash


@app.get("/api/stash/", response_model=Union[_schemas.Stash, List[_schemas.Stash]])
async def get_all_stashes(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_stashes = await CRUD_stash.get(db=db)
    return all_stashes


@app.delete("/api/stash/{stashId}")
async def delete_stash(stashId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    stash_map = {"stashId": stashId}
    await CRUD_stash.remove(db=db, filter=stash_map)

    return "Stash deleted successfully"


@app.put("/api/stash/{stashId}", response_model=_schemas.Stash)
async def update_stash(
    stashId: str,
    stash_update: _schemas.StashUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    stash_map = {"stashId": stashId}
    stash = await CRUD_stash.get(
        db=db,
        filter=stash_map,
    )

    return await CRUD_stash.update(db_obj=stash, obj_in=stash_update, db=db)


CRUD_modifier = _crud.CRUDBase[
    _models.Modifier,
    _schemas.Modifier,
    _schemas.ModifierCreate,
    _schemas.ModifierUpdate,
](model=_models.Modifier, schema=_schemas.Modifier)


@app.post(
    "/api/modifier/",
    response_model=Union[_schemas.ModifierCreate, List[_schemas.ModifierCreate]],
)
async def create_modifier(
    modifier: Union[_schemas.ModifierCreate, List[_schemas.ModifierCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_modifier.create(db=db, obj_in=modifier)


@app.get(
    "/api/modifier/{modifierId}",
    response_model=Union[_schemas.Modifier, List[_schemas.Modifier]],
)
async def get_modifier(
    modifierId: int,
    position: Optional[int] = None,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    modifier = await CRUD_modifier.get(db=db, filter=modifier_map)
    return modifier


@app.get(
    "/api/modifier/", response_model=Union[_schemas.Modifier, List[_schemas.Modifier]]
)
async def get_all_modifiers(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_modifiers = await CRUD_modifier.get(db=db)
    return all_modifiers


@app.delete("/api/modifier/{modifierId}")
async def delete_modifier(
    modifierId: int,
    position: Optional[int] = None,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    await CRUD_modifier.remove(db=db, filter=modifier_map)

    return "Modifier deleted successfully"


@app.put("/api/modifier/{modifierId}", response_model=_schemas.Modifier)
async def update_modifier(
    modifierId: int,
    position: int,
    modifier_update: _schemas.ModifierUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    modifier_map = {"modifierId": modifierId, "position": position}
    modifier = await CRUD_modifier.get(
        db=db,
        filter=modifier_map,
    )

    return await CRUD_modifier.update(db_obj=modifier, obj_in=modifier_update, db=db)


CRUD_itemModifier = _crud.CRUDBase[
    _models.ItemModifier,
    _schemas.ItemModifier,
    _schemas.ItemModifierCreate,
    _schemas.ItemModifierUpdate,
](model=_models.ItemModifier, schema=_schemas.ItemModifier)


@app.post(
    "/api/itemModifier/",
    response_model=Union[_schemas.ItemModifier, List[_schemas.ItemModifier]],
)
async def create_item_modifier(
    itemModifier: Union[_schemas.ItemModifierCreate, List[_schemas.ItemModifierCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await CRUD_itemModifier.create(db=db, obj_in=itemModifier)


@app.get(
    "/api/itemModifier/{itemId}",
    response_model=Union[_schemas.ItemModifier, List[_schemas.ItemModifier]],
)
async def get_item_modifier(
    itemId: int,
    gameItemId: Optional[str] = None,
    modifierId: Optional[int] = None,
    position: Optional[int] = None,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemModifier_map = {"itemId": itemId}
    if gameItemId is not None:
        itemModifier_map["gameItemId"] = gameItemId
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if position is not None:
        itemModifier_map["position"] = position

    itemModifier = await CRUD_itemModifier.get(db=db, filter=itemModifier_map)
    return itemModifier


@app.get(
    "/api/itemModifier/",
    response_model=Union[_schemas.ItemModifier, List[_schemas.ItemModifier]],
)
async def get_all_item_modifiers(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_itemModifiers = await CRUD_itemModifier.get(db=db)
    return all_itemModifiers


@app.delete("/api/itemModifier/{itemId}")
async def delete_item_modifier(
    itemId: int,
    gameItemId: Optional[str] = None,
    modifierId: Optional[int] = None,
    position: Optional[int] = None,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemModifier_map = {"itemId": itemId}
    if gameItemId is not None:
        itemModifier_map["gameItemId"] = gameItemId
    if modifierId is not None:
        itemModifier_map["modifierId"] = modifierId
    if position is not None:
        itemModifier_map["position"] = position

    await CRUD_itemModifier.remove(db=db, filter=itemModifier_map)

    return "ItemModifier deleted successfully"


@app.put(
    "/api/itemModifier/{itemId}",
    response_model=_schemas.ItemModifier,
)
async def update_item_modifier(
    itemId: int,
    gameItemId: str,
    modifierId: int,
    position: int,
    itemModifier_update: _schemas.ItemModifierUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemModifier_map = {
        "itemId": itemId,
        "gameItemId": gameItemId,
        "modifierId": modifierId,
        "position": position,
    }
    itemModifier = await CRUD_itemModifier.get(
        db=db,
        filter=itemModifier_map,
    )

    return await CRUD_itemModifier.update(
        db_obj=itemModifier, obj_in=itemModifier_update, db=db
    )
