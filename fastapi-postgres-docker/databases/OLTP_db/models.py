import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import JSONB

import database as _database


class Currency(_database.Base):

    __tablename__ = "currency"

    currencyName = _sql.Column(
        _sql.String(), primary_key=True, index=True, nullable=False
    )
    valueInChaos = _sql.Column(_sql.Float(), nullable=False)
    iconUrl = _sql.Column(_sql.String(), nullable=False, unique=True)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class ItemBaseType(_database.Base):

    __tablename__ = "item_basetype"

    baseType = _sql.Column(_sql.String(), nullable=False, primary_key=True, index=True)
    category = _sql.Column(_sql.String(), nullable=False, unique=True)
    subCategory = _sql.Column(JSONB(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class Item(_database.Base):

    __tablename__ = "item"

    itemId = _sql.Column(_sql.String(), primary_key=True, index=True, nullable=False)
    stashId = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Stash.stashId", ondelete="CASCADE"),
        nullable=False,
    )
    name = _sql.Column(_sql.String())
    iconUrl = _sql.Column(_sql.String())
    league = _sql.Column(_sql.String(), nullable=False)
    typeLine = _sql.Column(_sql.String(), nullable=False)
    baseType = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("ItemBaseType.baseType", ondelete="RESTRICT"),
        nullable=False,
    )
    rarity = _sql.Column(_sql.String(), nullable=False)
    identified = _sql.Column(_sql.Boolean(), nullable=False)
    itemLevel = _sql.Column(_sql.SmallInteger(), nullable=False)
    forumNote = _sql.Column(_sql.String())
    currencyAmount = _sql.Column(_sql.Float(24))
    currencyName = _sql.Column(
        _sql.String(), _sql.ForeignKey("Currency.currencyName", ondelete="RESTRICT")
    )
    corrupted = _sql.Column(_sql.Boolean())
    delve = _sql.Column(_sql.Boolean())
    fractured = _sql.Column(_sql.Boolean())
    synthesized = _sql.Column(_sql.Boolean())
    replica = _sql.Column(_sql.Boolean())
    elder = _sql.Column(_sql.Boolean())
    shaper = _sql.Column(_sql.Boolean())
    influences = _sql.Column(JSONB())
    searing = _sql.Column(_sql.Boolean())
    tangled = _sql.Column(_sql.Boolean())
    isRelic = _sql.Column(_sql.Boolean())
    prefixes = _sql.Column(_sql.SmallInteger())
    suffixes = _sql.Column(_sql.SmallInteger())
    foilVariation = _sql.Column(_sql.Integer())
    inventoryId = _sql.Column(_sql.String())
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class Modifier(_database.Base):

    __tablename__ = "modifier"

    modifierId = _sql.Column(_sql.String(), nullable=False, index=True)
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    minRoll = _sql.Column(_sql.Float(24))
    maxRoll = _sql.Column(_sql.Float(24))
    textRoll = _sql.Column(_sql.String())
    effect = _sql.Column(_sql.String(), nullable=False)
    implicit = _sql.Column(_sql.Boolean())
    explicit = _sql.Column(_sql.Boolean())
    delve = _sql.Column(_sql.Boolean())
    fractured = _sql.Column(_sql.Boolean())
    synthesized = _sql.Column(_sql.Boolean())
    corrupted = _sql.Column(_sql.Boolean())
    enchanted = _sql.Column(_sql.Boolean())
    veiled = _sql.Column(_sql.Boolean())
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)

    __table_args__ = (_sql.PrimaryKeyConstraint(modifierId, position),)


class Transaction(_database.Base):

    __tablename__ = "transaction"

    transactionId = _sql.Column(
        _sql.Integer(), autoincrement=True, primary_key=True, index=True, nullable=False
    )
    itemId = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Item.itemId", ondelete="CASCADE"),
        nullable=False,
    )
    accountName = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Account.accountName", ondelete="CASCADE"),
        nullable=False,
    )
    currencyAmount = _sql.Column(_sql.Float(24), nullable=False)
    currencyName = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Currency.currencyName", ondelete="RESTRICT"),
        nullable=False,
    )
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class ItemModifier(_database.Base):

    __tablename__ = "item_modifier"

    itemId = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Item.itemId", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    modifierId = _sql.Column(_sql.String(), nullable=False, index=True)
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    range = _sql.Column(_sql.Float(24))

    __table_args__ = (
        _sql.PrimaryKeyConstraint(itemId, modifierId, position),
        _sql.ForeignKeyConstraint(
            [modifierId, position],
            ["Modifier.modifierId", "Modifier.position"],
            ondelete="CASCADE",
        ),
    )


class Stash(_database.Base):

    __tablename__ = "stash"

    stashId = _sql.Column(_sql.String(), primary_key=True, index=True, nullable=False)
    accountName = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("Account.accountName", ondelete="CASCADE"),
        nullable=False,
    )
    public = _sql.Column(_sql.Boolean(), nullable=False)
    league = _sql.Column(_sql.String(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class Account(_database.Base):

    __tablename__ = "account"

    accountName = _sql.Column(
        _sql.String(), primary_key=True, index=True, nullable=False
    )
    isBanned = _sql.Column(_sql.Boolean())
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
