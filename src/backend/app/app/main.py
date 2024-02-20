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


currencyCRUD = _crud.CRUDBase[
    _models.Currency,
    _schemas.Currency,
    _schemas.CurrencyCreate,
    _schemas.CurrencyUpdate,
](model=_models.Currency, schema=_schemas.Currency)


@app.post(
    "/api/currency/",
    response_model=Union[_schemas.CurrencyCreate, List[_schemas.CurrencyCreate]],
)
async def create_currency(
    currency: Union[_schemas.CurrencyCreate, List[_schemas.CurrencyCreate]],
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    return await currencyCRUD.create(db=db, obj_in=currency)


@app.get("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def get_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_mapped = {"currencyId": currencyId}
    currency = await currencyCRUD.get(db=db, filter=currency_mapped)
    return currency


@app.get("/api/currency/", response_model=List[_schemas.Currency])
async def get_all_currency(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_currency = await currencyCRUD.get_all(db=db)
    return all_currency


@app.delete("/api/currency/{currencyId}")
async def delete_currency(
    currencyId: int, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    currency_mapped = {"currencyId": currencyId}
    await currencyCRUD.remove(filter=currency_mapped, db=db)

    return f"Currency with id {currencyId} deleted successfully"


@app.put("/api/currency/{currencyId}", response_model=_schemas.Currency)
async def update_currency(
    currencyId: str,
    currency_update: _schemas.CurrencyUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    currency_map = {"currencyId": currencyId}
    currency = await currencyCRUD.get(
        db=db,
        filter=currency_map,
    )

    return await currencyCRUD.update(db_obj=currency, obj_in=currency_update, db=db)


accountCRUD = _crud.CRUDBase[
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
    return await accountCRUD.create(db=db, obj_in=account)


@app.get("/api/account/{accountName}", response_model=_schemas.Account)
async def get_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    account = await accountCRUD.get(db=db, filter=account_map)
    return account


@app.get("/api/account/", response_model=List[_schemas.Account])
async def get_all_accounts(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_accounts = await accountCRUD.get_all(db=db)
    return all_accounts


@app.delete("/api/account/{accountName}")
async def delete_account(
    accountName: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    account_map = {"accountName": accountName}
    await accountCRUD.remove(db=db, filter=account_map)

    return "Account deleted successfully"


@app.put("/api/account/{accountName}", response_model=_schemas.Account)
async def update_account(
    accountName: str,
    account_update: _schemas.AccountUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    account_mapped = {"accountName": accountName}
    account = await accountCRUD.get(
        db=db,
        filter=account_mapped,
    )

    return await accountCRUD.update(db_obj=account, obj_in=account_update, db=db)


itemBaseTypeCRUD = _crud.CRUDBase[
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
    return await itemBaseTypeCRUD.create(db=db, obj_in=itemBaseType)


@app.get("/api/itemBaseType/{baseType}", response_model=_schemas.ItemBaseType)
async def get_itemBaseType(
    baseType: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    itemBaseTypeMap = {"baseType": baseType}
    itemBaseType = await itemBaseTypeCRUD.get(db=db, filter=itemBaseTypeMap)
    return itemBaseType


@app.get("/api/itemBaseType/", response_model=List[_schemas.ItemBaseType])
async def get_all_itemBaseTypes(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    allItemBaseTypes = await itemBaseTypeCRUD.get_all(db=db)
    return allItemBaseTypes


@app.delete("/api/itemBaseType/{baseType}")
async def delete_itemBaseType(
    baseType: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    itemBaseTypeMap = {"baseType": baseType}
    await itemBaseTypeCRUD.remove(db=db, filter=itemBaseTypeMap)

    return "ItemBaseType deleted successfully"


@app.put("/api/itemBaseType/{baseType}", response_model=_schemas.ItemBaseType)
async def update_itemBaseType(
    baseType: str,
    itemBaseTypeUpdate: _schemas.ItemBaseTypeUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemBaseTypeMap = {"baseType": baseType}
    itemBaseType = await itemBaseTypeCRUD.get(
        db=db,
        filter=itemBaseTypeMap,
    )

    return await itemBaseTypeCRUD.update(
        db_obj=itemBaseType, obj_in=itemBaseTypeUpdate, db=db
    )


itemCRUD = _crud.CRUDBase[
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
    return await itemCRUD.create(db=db, obj_in=item)


@app.get("/api/item/{gameItemId}", response_model=_schemas.Item)
async def get_item(gameItemId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    item_map = {"gameItemId": gameItemId}
    item = await itemCRUD.get(db=db, filter=item_map)
    return item


@app.get("/api/item/", response_model=List[_schemas.Item])
async def get_all_items(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_items = await itemCRUD.get_all(db=db)
    return all_items


@app.delete("/api/item/{gameItemId}")
async def delete_item(
    gameItemId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    item_map = {"gameItemId": gameItemId}
    await itemCRUD.remove(db=db, filter=item_map)

    return "Item deleted successfully"


@app.put("/api/item/{gameItemId}", response_model=_schemas.Item)
async def update_item(
    gameItemId: str,
    item_update: _schemas.ItemUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    item_mapped = {"gameItemId": gameItemId}
    item = await itemCRUD.get(
        db=db,
        filter=item_mapped,
    )

    return await itemCRUD.update(db_obj=item, obj_in=item_update, db=db)


stashCRUD = _crud.CRUDBase[
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
    return await stashCRUD.create(db=db, obj_in=stash)


@app.get("/api/stash/{stashId}", response_model=_schemas.Stash)
async def get_stash(stashId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    stash_map = {"stashId": stashId}
    stash = await stashCRUD.get(db=db, filter=stash_map)
    return stash


@app.get("/api/stash/", response_model=List[_schemas.Stash])
async def get_all_stashes(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_stashes = await stashCRUD.get_all(db=db)
    return all_stashes


@app.delete("/api/stash/{stashId}")
async def delete_stash(stashId: str, db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    stash_map = {"stashId": stashId}
    await stashCRUD.remove(db=db, filter=stash_map)

    return "Stash deleted successfully"


@app.put("/api/stash/{stashId}", response_model=_schemas.Stash)
async def update_stash(
    stashId: str,
    stash_update: _schemas.StashUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    stash_mapped = {"stashId": stashId}
    stash = await stashCRUD.get(
        db=db,
        filter=stash_mapped,
    )

    return await stashCRUD.update(db_obj=stash, obj_in=stash_update, db=db)


modifierCRUD = _crud.CRUDBase[
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
    return await modifierCRUD.create(db=db, obj_in=modifier)


@app.get("/api/modifier/{modifierId}", response_model=Union[_schemas.Modifier, List[_schemas.Modifier]])
async def get_modifier(
    modifierId: int, position: Optional[int] = None, db: _orm.Session = _fastapi.Depends(_deps.get_db)
):
    modifier_map = {"modifierId": modifierId}
    if position is not None:
        modifier_map["position"] = position
    modifier = await modifierCRUD.get(db=db, filter=modifier_map)
    return modifier


@app.get("/api/modifier/", response_model=List[_schemas.Modifier])
async def get_all_modifiers(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_modifiers = await modifierCRUD.get_all(db=db)
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
    await modifierCRUD.remove(db=db, filter=modifier_map)

    return "Modifier deleted successfully"


@app.put("/api/modifier/{modifierId}", response_model=_schemas.Modifier)
async def update_modifier(
    modifierId: int,
    position: int,
    modifier_update: _schemas.ModifierUpdate,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    modifier_mapped = {"modifierId": modifierId, "position": position}
    modifier = await modifierCRUD.get(
        db=db,
        filter=modifier_mapped,
    )

    return await modifierCRUD.update(db_obj=modifier, obj_in=modifier_update, db=db)


itemModifierCRUD = _crud.CRUDBase[
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
    return await itemModifierCRUD.create(db=db, obj_in=itemModifier)


@app.get(
    "/api/itemModifier/{itemId}",
    response_model=_schemas.ItemModifier,
)
async def get_item_modifier(
    itemId: int,
    gameItemId: str,
    modifierId: int,
    position: int,
    db: _orm.Session = _fastapi.Depends(_deps.get_db),
):
    itemModifier_map = {
        "itemId": itemId,
        "gameItemId": gameItemId,
        "modifierId": modifierId,
        "position": position,
    }
    itemModifier = await itemModifierCRUD.get(db=db, filter=itemModifier_map)
    return itemModifier


@app.get("/api/itemModifier/", response_model=List[_schemas.ItemModifier])
async def get_all_item_modifiers(db: _orm.Session = _fastapi.Depends(_deps.get_db)):
    all_item_modifiers = await itemModifierCRUD.get_all(db=db)
    return all_item_modifiers


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

    await itemModifierCRUD.remove(db=db, filter=itemModifier_map)

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
    itemModifier_mapped = {
        "itemId": itemId,
        "gameItemId": gameItemId,
        "modifierId": modifierId,
        "position": position,
    }
    itemModifier = await itemModifierCRUD.get(
        db=db,
        filter=itemModifier_mapped,
    )

    return await itemModifierCRUD.update(
        db_obj=itemModifier, obj_in=itemModifier_update, db=db
    )
