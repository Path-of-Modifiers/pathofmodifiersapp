from typing import TYPE_CHECKING, List

import datetime as _dt
import pydantic as _pydantic
import database as Database
import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return Database.Base.metadata.create_all(bind=Database.engine)


def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_commit_refresh(field: _pydantic.BaseModel, db: "Session"):
    db.add(field)
    db.commit()
    db.refresh(field)


async def create_currency(
    currency: _schemas.CreateCurrency, db: "Session"
) -> _schemas.Currency:
    currency = _models.Currency(**currency.model_dump())
    add_commit_refresh(currency, db)
    return _schemas.Currency.model_validate(currency)


async def get_all_currency(db: "Session") -> List[_schemas.Currency]:
    currencies = db.query(_models.Currency).all()
    return list(map(_schemas.Currency.model_validate, currencies))


async def get_currency(currencyName: int, db: "Session"):
    currency = (
        db.query(_models.Currency)
        .filter(_models.Currency.currencyName == currencyName)
        .first()
    )
    return currency


async def delete_currency(currency: _models.Currency, db: "Session"):
    db.delete(currency)
    db.commit()


async def update_currency(
    currencyData: _schemas.CreateCurrency, currency: _models.Currency, db: "Session"
) -> _schemas.Currency:
    currency.update(
        **currencyData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow()
    )
    db.commit()
    db.refresh(currency)

    return _schemas.Currency.model_validate(currency)


async def create_item(item: _schemas.CreateItem, db: "Session") -> _schemas.Item:
    item = _models.Item(**item.model_dump())
    add_commit_refresh(item, db)


async def get_all_item(db: "Session") -> List[_schemas.Item]:
    items = db.query(_models.Item).all()
    return list(map(_schemas.Item.model_validate, items))


async def get_item(itemId: int, db: "Session"):
    item = db.query(_models.Item).filter(_models.Item.itemId == itemId).first()
    return item


async def delete_item(item: _models.Item, db: "Session"):
    db.delete(item)
    db.commit()


async def update_item(
    itemData: _schemas.CreateItem, item: _models.Item, db: "Session"
) -> _schemas.Item:
    item.update(**itemData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow())
    db.commit()
    db.refresh(item)

    return _schemas.Item.model_validate(item)


async def create_transaction(
    transaction: _schemas.CreateTransaction, db: "Session"
) -> _schemas.Transaction:
    transaction = _models.Transaction(**transaction.model_dump())
    add_commit_refresh(transaction, db)
    return _schemas.Transaction.model_validate(transaction)


async def get_all_transaction(db: "Session") -> List[_schemas.Transaction]:
    transactions = db.query(_models.Transaction).all()
    return list(map(_schemas.Transaction.model_validate, transactions))


async def get_transaction(transactionId: int, db: "Session"):
    transaction = (
        db.query(_models.Transaction)
        .filter(_models.Transaction.transactionId == transactionId)
        .first()
    )
    return transaction


async def delete_transaction(transaction: _models.Transaction, db: "Session"):
    db.delete(transaction)
    db.commit()


async def update_transaction(
    transactionData: _schemas.CreateTransaction,
    transaction: _models.Transaction,
    db: "Session",
) -> _schemas.Transaction:
    transaction.update(
        **transactionData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow()
    )
    db.commit()
    db.refresh(transaction)

    return _schemas.Transaction.model_validate(transaction)


async def create_item_base_type(
    itemBaseType: _schemas.CreateItemBaseType, db: "Session"
) -> _schemas.ItemBaseType:
    itemBaseType = _models.ItemBaseType(**itemBaseType.model_dump())
    add_commit_refresh(itemBaseType, db)
    return _schemas.ItemBaseType.model_validate(itemBaseType)


async def get_all_item_base_type(db: "Session") -> List[_schemas.ItemBaseType]:
    item_base_types = db.query(_models.ItemBaseType).all()
    return list(map(_schemas.ItemBaseType.model_validate, item_base_types))


async def get_item_base_type(itemBaseTypeId: int, db: "Session"):
    itemBaseType = (
        db.query(_models.ItemBaseType)
        .filter(_models.ItemBaseType.baseType == itemBaseTypeId)
        .first()
    )
    return itemBaseType


async def delete_item_base_type(item_base_type: _models.ItemBaseType, db: "Session"):
    db.delete(item_base_type)
    db.commit()


async def update_item_base_type(
    itemBaseTypeData: _schemas.CreateItemBaseType,
    itemBaseType: _models.ItemBaseType,
    db: "Session",
) -> _schemas.ItemBaseType:
    itemBaseType.update(
        **itemBaseTypeData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow()
    )
    db.commit()
    db.refresh(itemBaseType)

    return _schemas.ItemBaseType.model_validate(itemBaseType)


async def create_item_modifier(
    itemModifier: _schemas.CreateItemModifier, db: "Session"
) -> _schemas.ItemModifier:
    itemModifier = _models.ItemModifier(**itemModifier.model_dump())
    add_commit_refresh(itemModifier, db)
    return _schemas.ItemModifier.model_validate(itemModifier)


async def get_all_item_modifier(db: "Session") -> List[_schemas.ItemModifier]:
    itemModifiers = db.query(_models.ItemModifier).all()
    return list(map(_schemas.ItemModifier.model_validate, itemModifiers))


async def get_item_modifier(itemModifierId: int, db: "Session"):
    itemModifier = (
        db.query(_models.ItemModifier)
        .filter(
            _models.ItemModifier.itemModifierId == itemModifierId,
        )
        .first()
    )
    return itemModifier


async def delete_item_modifier(itemModifier: _models.ItemModifier, db: "Session"):
    db.delete(itemModifier)
    db.commit()


async def update_item_modifier(
    itemModifierData: _schemas.CreateItemModifier,
    itemModifier: _models.ItemModifier,
    db: "Session",
) -> _schemas.ItemModifier:
    itemModifier.update(
        **itemModifierData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow()
    )
    db.commit()
    db.refresh(itemModifier)

    return _schemas.ItemModifier.model_validate(itemModifier)


async def create_modifier(
    modifier: _schemas.CreateModifier, db: "Session"
) -> _schemas.Modifier:
    modifier = _models.Modifier(**modifier.model_dump())
    add_commit_refresh(modifier, db)
    return _schemas.Modifier.model_validate(modifier)


async def get_all_modifier(db: "Session") -> List[_schemas.Modifier]:
    modifiers = db.query(_models.Modifier).all()
    return list(map(_schemas.Modifier.model_validate, modifiers))


async def get_modifier(modifierId: int, position: int, db: "Session"):
    modifier = (
        db.query(_models.Modifier)
        .filter(
            _models.Modifier.id == modifierId, _models.Modifier.position == position
        )
        .first()
    )
    return modifier


async def delete_modifier(modifier: _models.Modifier, db: "Session"):
    db.delete(modifier)
    db.commit()


async def update_modifier(
    modifierData: _schemas.CreateModifier, modifier: _models.Modifier, db: "Session"
) -> _schemas.Modifier:
    modifier.update(
        **modifierData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow()
    )
    db.commit()
    db.refresh(modifier)

    return _schemas.Modifier.model_validate(modifier)


async def create_stash(stash: _schemas.CreateStash, db: "Session") -> _schemas.Stash:
    stash = _models.Stash(**stash.model_dump())
    add_commit_refresh(stash, db)
    return _schemas.Stash.model_validate(stash)


async def get_all_stash(db: "Session") -> List[_schemas.Stash]:
    stashs = db.query(_models.Stash).all()
    return list(map(_schemas.Stash.model_validate, stashs))


async def get_stash(stash_id: int, db: "Session"):
    stash = db.query(_models.Stash).filter(_models.Stash.id == stash_id).first()
    return stash


async def delete_stash(stash: _models.Stash, db: "Session"):
    db.delete(stash)
    db.commit()


async def update_stash(
    stashData: _schemas.CreateStash, stash: _models.Stash, db: "Session"
) -> _schemas.Stash:
    stash.update(**stashData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow())
    db.commit()
    db.refresh(stash)

    return _schemas.Stash.model_validate(stash)


async def create_account(
    account: _schemas.CreateAccount, db: "Session"
) -> _schemas.Account:
    account = _models.Account(**account.model_dump())
    add_commit_refresh(account, db)
    return _schemas.Account.model_validate(account)


async def get_all_account(db: "Session") -> List[_schemas.Account]:
    accounts = db.query(_models.Account).all()
    return list(map(_schemas.Account.model_validate, accounts))


async def get_account(account_id: int, db: "Session"):
    account = db.query(_models.Account).filter(_models.Account.id == account_id).first()
    return account


async def delete_account(account: _models.Account, db: "Session"):
    db.delete(account)
    db.commit()


async def update_account(
    accountData: _schemas.CreateAccount, account: _models.Account, db: "Session"
) -> _schemas.Account:
    account.update(**accountData.model_dump(), updatedAt=_schemas._dt.datetime.utcnow())
    db.commit()
    db.refresh(account)

    return _schemas.Account.model_validate(account)
