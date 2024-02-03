from typing import TYPE_CHECKING, List

import pydantic as _pydantic
import database as _database
import schemas as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_commit_refresh(field: _pydantic.BaseModel, db: "Session"):
    db.add(field)
    db.commit()
    db.refresh(field)

async def create_currency(currency: _schemas.CreateCurrency, db: "Session"
) -> _schemas.Currency:
    currency = _models.Currency(**currency.model_dump())
    add_commit_refresh(currency, db)
    return _schemas.Currency.model_validate(currency)

async def get_all_currencys(db: "Session") -> List[_schemas.Currency]:
    currencys = db.query(_models.Currency).all()
    return list(map(_schemas.Currency.model_validate, currencys))

async def get_currency(currency_id: int, db: "Session"):
    currency = db.query(_models.Currency).filter(_models.Currency.currencyName == currency_id).first()
    return currency

async def delete_currency(currency: _models.Currency, db: "Session"):
    db.delete(currency)
    db.commit()

async def update_currency(currency_data: _schemas.CreateCurrency, currency: _models.Currency, db: "Session"
) -> _schemas.Currency:
    currency.currencyName = currency_data.currencyName
    currency.valueInChaos = currency_data.valueInChaos
    currency.iconUrl = currency_data.iconUrl
    currency.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(currency)

    return _schemas.Currency.model_validate(currency)

async def create_item(item: _schemas.CreateItem, db: "Session"
) -> _schemas.Item:
    item = _models.Item(**item.model_dump())
    add_commit_refresh(item, db)

async def get_all_items(db: "Session") -> List[_schemas.Item]:
    items = db.query(_models.Item).all()
    return list(map(_schemas.Item.model_validate, items))

async def get_item(item_id: int, db: "Session"):
    item = db.query(_models.Item).filter(_models.Item.itemId == item_id).first()
    return item

async def delete_item(item: _models.Item, db: "Session"):
    db.delete(item)
    db.commit()

async def update_item(item_data: _schemas.CreateItem, item: _models.Item, db: "Session"
) -> _schemas.Item:
    item.stashId = item_data.stashId
    item.name = item_data.name
    item.iconUrl = item_data.iconUrl
    item.league = item_data.league
    item.typeLine = item_data.typeLine
    item.baseType = item_data.baseType
    item.rarity = item_data.rarity
    item.identified = item_data.identified
    item.itemLevel = item_data.itemLevel
    item.forumNote = item_data.forumNote
    item.currencyAmount = item_data.currencyAmount
    item.currencyName = item_data.currencyName
    item.corrupted = item_data.corrupted
    item.delve = item_data.delve
    item.fractured = item_data.fractured
    item.synthesized = item_data.synthesized
    item.replica = item_data.replica
    item.elder = item_data.elder
    item.shaper = item_data.shaper
    item.influences = item_data.influences
    item.searing = item_data.searing
    item.tangled = item_data.tangled
    item.isrelic = item_data.isrelic
    item.prefixes = item_data.prefixes
    item.suffixes = item_data.suffixes
    item.foilVariation = item_data.foilVariation
    item.inventoryId = item_data.inventoryId
    item.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(item)

    return _schemas.Item.model_validate(item)

async def create_transaction(transaction: _schemas.CreateTransaction, db: "Session"
) -> _schemas.Transaction:
    transaction = _models.Transaction(**transaction.model_dump())
    add_commit_refresh(transaction, db)
    return _schemas.Transaction.model_validate(transaction)

async def get_all_transactions(db: "Session") -> List[_schemas.Transaction]:
    transactions = db.query(_models.Transaction).all()
    return list(map(_schemas.Transaction.model_validate, transactions))

async def get_transaction(transaction_id: int, db: "Session"):
    transaction = db.query(_models.Transaction).filter(_models.Transaction.transactionId == transaction_id).first()
    return transaction

async def delete_transaction(transaction: _models.Transaction, db: "Session"):
    db.delete(transaction)
    db.commit()

async def update_transaction(transaction_data: _schemas.CreateTransaction, transaction: _models.Transaction, db: "Session"
) -> _schemas.Transaction:
    transaction.itemId = transaction_data.itemId
    transaction.accountName = transaction_data.accountName
    transaction.currencyAmount = transaction_data.currencyAmount
    transaction.currencyName = transaction_data.currencyName
    transaction.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(transaction)

    return _schemas.Transaction.model_validate(transaction)

async def create_item_base_type(item_base_type: _schemas.CreateItemBaseType, db: "Session"
) -> _schemas.ItemBaseType:
    item_base_type = _models.ItemBaseType(**item_base_type.model_dump())
    add_commit_refresh(item_base_type, db)
    return _schemas.ItemBaseType.model_validate(item_base_type)

async def get_all_item_base_types(db: "Session") -> List[_schemas.ItemBaseType]:
    item_base_types = db.query(_models.ItemBaseType).all()
    return list(map(_schemas.ItemBaseType.model_validate, item_base_types))

async def get_item_base_type(item_base_type_id: int, db: "Session"):
    item_base_type = db.query(_models.ItemBaseType).filter(_models.ItemBaseType.id == item_base_type_id).first()
    return item_base_type

async def delete_item_base_type(item_base_type: _models.ItemBaseType, db: "Session"):
    db.delete(item_base_type)
    db.commit()

async def update_item_base_type(item_base_type_data: _schemas.CreateItemBaseType, item_base_type: _models.ItemBaseType, db: "Session"
) -> _schemas.ItemBaseType:
    item_base_type.baseType = item_base_type_data.baseType
    item_base_type.category = item_base_type_data.category
    item_base_type.subCategory = item_base_type_data.subCategory
    item_base_type.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(item_base_type)

    return _schemas.ItemBaseType.model_validate(item_base_type)

async def create_item_modifiers(item_modifiers: _schemas.CreateItemModifiers, db: "Session"
) -> _schemas.ItemModifiers:
    item_modifiers = _models.ItemModifiers(**item_modifiers.model_dump())
    add_commit_refresh(item_modifiers, db)
    return _schemas.ItemModifiers.model_validate(item_modifiers)

async def get_all_item_modifierss(db: "Session") -> List[_schemas.ItemModifiers]:
    item_modifierss = db.query(_models.ItemModifiers).all()
    return list(map(_schemas.ItemModifiers.model_validate, item_modifierss))

async def get_item_modifiers(item_modifiers_id: int, db: "Session"):
    item_modifiers = db.query(_models.ItemModifiers).filter(_models.ItemModifiers.id == item_modifiers_id).first()
    return item_modifiers

async def delete_item_modifiers(item_modifiers: _models.ItemModifiers, db: "Session"):
    db.delete(item_modifiers)
    db.commit()

async def update_item_modifiers(item_modifiers_data: _schemas.CreateItemModifiers, item_modifiers: _models.ItemModifiers, db: "Session"
) -> _schemas.ItemModifiers:
    item_modifiers_data.modifierId = item_modifiers_data.modifierId
    item_modifiers_data.itemId = item_modifiers_data.itemId
    db.commit()
    db.refresh(item_modifiers)

    return _schemas.ItemModifiers.model_validate(item_modifiers)

async def create_modifier(modifier: _schemas.CreateModifier, db: "Session"
) -> _schemas.Modifier:
    modifier = _models.Modifier(**modifier.model_dump())
    add_commit_refresh(modifier, db)
    return _schemas.Modifier.model_validate(modifier)

async def get_all_modifiers(db: "Session") -> List[_schemas.Modifier]:
    modifiers = db.query(_models.Modifier).all()
    return list(map(_schemas.Modifier.model_validate, modifiers))

async def get_modifier(modifier_id: int, db: "Session"):
    modifier = db.query(_models.Modifier).filter(_models.Modifier.id == modifier_id).first()
    return modifier

async def delete_modifier(modifier: _models.Modifier, db: "Session"):
    db.delete(modifier)
    db.commit()

async def update_modifier(modifier_data: _schemas.CreateModifier, modifier: _models.Modifier, db: "Session"
) -> _schemas.Modifier:
    modifier.modifierId = modifier_data.modifierId
    modifier.effect = modifier_data.effect
    modifier.implicit = modifier_data.implicit
    modifier.explicit = modifier_data.explicit
    modifier.delve = modifier_data.delve
    modifier.fractured = modifier_data.fractured
    modifier.synthesized = modifier_data.synthesized
    modifier.corrupted = modifier_data.corrupted
    modifier.enchanted = modifier_data.enchanted
    modifier.veiled = modifier_data.veiled
    modifier.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(modifier)

    return _schemas.Modifier.model_validate(modifier)

async def create_modifier_stats(modifier_stats: _schemas.CreateModifierStats, db: "Session"
) -> _schemas.ModifierStats:
    modifier_stats = _models.ModifierStats(**modifier_stats.model_dump())
    add_commit_refresh(modifier_stats, db)
    return _schemas.ModifierStats.model_validate(modifier_stats)

async def get_all_modifier_stats(db: "Session") -> List[_schemas.ModifierStats]:
    modifier_statss = db.query(_models.ModifierStats).all()
    return list(map(_schemas.ModifierStats.model_validate, modifier_statss))

async def get_modifier_stats(modifier_stats_id: int, db: "Session"):
    modifier_stats = db.query(_models.ModifierStats).filter(_models.ModifierStats.id == modifier_stats_id).first()
    return modifier_stats

async def delete_modifier_stats(modifier_stats: _models.ModifierStats, db: "Session"):
    db.delete(modifier_stats)
    db.commit()

async def update_modifier_stats(modifier_stats_data: _schemas.CreateModifierStats, modifier_stats: _models.ModifierStats, db: "Session"
) -> _schemas.CreateModifierStats:
    modifier_stats.modifierId = modifier_stats_data.modifierId
    modifier_stats.statId = modifier_stats_data.statId
    db.commit()
    db.refresh(modifier_stats)

    return _schemas.CreateModifierStats.model_validate(modifier_stats)

async def create_stat(stat: _schemas.Stat, db: "Session"
) -> _schemas.Stat:
    stat = _models.Stat(**stat.model_dump())
    add_commit_refresh(stat, db)
    return _schemas.Stat.model_validate(stat)

async def get_all_stats(db: "Session") -> List[_schemas.Stat]:
    stats = db.query(_models.Stat).all()
    return list(map(_schemas.Stat.model_validate, stats))

async def get_stat(stat_id: int, db: "Session"):
    stat = db.query(_models.Stat).filter(_models.Stat.id == stat_id).first()
    return stat

async def delete_stat(stat: _models.Stat, db: "Session"):
    db.delete(stat)
    db.commit()

async def update_stat(stat_data: _schemas.CreateStat, stat: _models.Stat, db: "Session"
) -> _schemas.Stat:
    stat.statId = stat_data.statId
    stat.position = stat_data.position
    stat.statValue = stat_data.statValue
    stat.mininumValue = stat_data.mininumValue
    stat.maximumValue = stat_data.maximumValue
    stat.statTier = stat_data.statTier
    stat.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(stat)

    return _schemas.Stat.model_validate(stat)

async def create_stash(stash: _schemas.CreateStash, db: "Session"
) -> _schemas.Stash:
    stash = _models.Stash(**stash.model_dump())
    add_commit_refresh(stash, db)
    return _schemas.Stash.model_validate(stash)

async def get_all_stashs(db: "Session") -> List[_schemas.Stash]:
    stashs = db.query(_models.Stash).all()
    return list(map(_schemas.Stash.model_validate, stashs))

async def get_stash(stash_id: int, db: "Session"):
    stash = db.query(_models.Stash).filter(_models.Stash.id == stash_id).first()
    return stash

async def delete_stash(stash: _models.Stash, db: "Session"):
    db.delete(stash)
    db.commit()

async def update_stash(stash_data: _schemas.CreateStash, stash: _models.Stash, db: "Session"
) -> _schemas.Stash:
    stash.stashId = stash_data.stashId
    stash.accountName = stash_data.accountName
    stash.public = stash_data.public
    stash.league = stash_data.league
    stash.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(stash)

    return _schemas.Stash.model_validate(stash)

async def create_account(account: _schemas.CreateAccount, db: "Session"
) -> _schemas.Account:
    account = _models.Account(**account.model_dump())
    add_commit_refresh(account, db)
    return _schemas.Account.model_validate(account)

async def get_all_accounts(db: "Session") -> List[_schemas.Account]:
    accounts = db.query(_models.Account).all()
    return list(map(_schemas.Account.model_validate, accounts))

async def get_account(account_id: int, db: "Session"):
    account = db.query(_models.Account).filter(_models.Account.id == account_id).first()
    return account

async def delete_account(account: _models.Account, db: "Session"):
    db.delete(account)
    db.commit()

async def update_account(account_data: _schemas.CreateAccount, account: _models.Account, db: "Session"
) -> _schemas.Account:
    account.accountName = account_data.accountName
    account.isBanned = account_data.isBanned
    account.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(account)

    return _schemas.Account.model_validate(account)

# Format for adding new services
""" async def create_X(X: _schemas.CreateX, db: "Session"
) -> _schemas.X:
    X = _models.X(**X.model_dump())
    add_commit_refresh(X, db)
    return _schemas.X.model_validate(X)

async def get_all_Xs(db: "Session") -> List[_schemas.X]:
    Xs = db.query(_models.X).all()
    return list(map(_schemas.X.model_validate, Xs))

async def get_X(X_id: int, db: "Session"):
    X = db.query(_models.X).filter(_models.X.id == X_id).first()
    return X

async def delete_X(X: _models.X, db: "Session"):
    db.delete(X)
    db.commit()

async def update_X(X_data: _schemas.CreateX, X: _models.X, db: "Session"
) -> _schemas.X:
    X.name = X_data.name
    # add more fields here
    X.updatedAt = _schemas._dt.datetime.now()
    db.commit()
    db.refresh(X)

    return _schemas.X.model_validate(X) """



