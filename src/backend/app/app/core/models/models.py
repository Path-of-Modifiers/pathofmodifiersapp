import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import JSONB

from app.core.models.database import Base


def update(self, **new_data):
    for field, value in new_data.items():
        setattr(self, field, value)


Base.update = update


class Currency(Base):

    __tablename__ = "currency"

    currency_field_seq = _sql.Sequence(
        "currency_id_seq",
        start=1,
        increment=1,
        minvalue=1,
        cycle=False,
        cache=1,
        schema=None,
    )
    currencyId = _sql.Column(
        _sql.BigInteger(),
        currency_field_seq,
        server_default=currency_field_seq.next_value(),
        primary_key=True,
        index=True,
        nullable=False,
    )
    currencyName = _sql.Column(_sql.String(), index=True, nullable=False)
    valueInChaos = _sql.Column(_sql.Float(), nullable=False)
    iconUrl = _sql.Column(_sql.String(), nullable=False, unique=True)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class ItemBaseType(Base):

    __tablename__ = "item_base_type"

    baseType = _sql.Column(_sql.String(), nullable=False, primary_key=True, index=True)
    category = _sql.Column(_sql.String(), nullable=False, unique=True)
    subCategory = _sql.Column(JSONB(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class Item(Base):

    __tablename__ = "item"

    item_field_seq = _sql.Sequence(
        "item_id_seq",
        start=1,
        increment=1,
        minvalue=1,
        cycle=False,
        cache=1,
        schema=None,
    )
    itemId = _sql.Column(
        _sql.BigInteger(),
        item_field_seq,
        index=True,
        nullable=False,
        server_default=item_field_seq.next_value(),
    )
    gameItemId = _sql.Column(_sql.String(), index=True, nullable=False)
    stashId = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("stash.stashId", ondelete="CASCADE"),
        nullable=False,
    )
    name = _sql.Column(_sql.String())
    iconUrl = _sql.Column(_sql.String())
    league = _sql.Column(_sql.String(), nullable=False)
    typeLine = _sql.Column(_sql.String(), nullable=False)
    baseType = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("item_base_type.baseType", ondelete="RESTRICT"),
        nullable=False,
    )
    rarity = _sql.Column(_sql.String(), nullable=False)
    identified = _sql.Column(_sql.Boolean(), nullable=False)
    itemLevel = _sql.Column(_sql.SmallInteger(), nullable=False)
    forumNote = _sql.Column(_sql.String())
    currencyAmount = _sql.Column(_sql.Float(24))
    currencyId = _sql.Column(
        _sql.Integer(), _sql.ForeignKey("currency.currencyId", ondelete="RESTRICT")
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

    __table_args__ = (_sql.PrimaryKeyConstraint(itemId, gameItemId),)


class Modifier(Base):

    __tablename__ = "modifier"

    modifier_field_seq = _sql.Sequence(
        "modifier_id_seq",
        start=1,
        increment=1,
        minvalue=1,
        cycle=False,
        cache=1,
        schema=None,
    )
    modifierId = _sql.Column(
        _sql.BigInteger(),
        modifier_field_seq,
        index=True,
        nullable=False,
        server_default=modifier_field_seq.next_value(),
    )
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    minRoll = _sql.Column(_sql.Float(24))
    maxRoll = _sql.Column(_sql.Float(24))
    textRoll = _sql.Column(_sql.String())
    static = _sql.Column(_sql.Boolean())
    effect = _sql.Column(_sql.String(), nullable=False)
    regex = _sql.Column(_sql.String())
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


class ItemModifier(Base):

    __tablename__ = "item_modifier"

    itemId = _sql.Column(
        _sql.BigInteger(),
        nullable=False,
        index=True,
    )
    gameItemId = _sql.Column(
        _sql.String(),
        nullable=False,
        index=True,
    )
    modifierId = _sql.Column(_sql.BigInteger(), nullable=False, index=True)
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    range = _sql.Column(_sql.Float(24))

    __table_args__ = (
        _sql.PrimaryKeyConstraint(itemId, gameItemId, modifierId, position),
        _sql.ForeignKeyConstraint(
            [itemId, gameItemId],
            ["item.itemId", "item.gameItemId"],
            ondelete="CASCADE",
        ),
        _sql.ForeignKeyConstraint(
            [modifierId, position],
            ["modifier.modifierId", "modifier.position"],
            ondelete="CASCADE",
        ),
    )


class Stash(Base):

    __tablename__ = "stash"

    stashId = _sql.Column(_sql.String(), primary_key=True, index=True, nullable=False)
    accountName = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("account.accountName", ondelete="CASCADE"),
        nullable=False,
    )
    public = _sql.Column(_sql.Boolean(), nullable=False)
    league = _sql.Column(_sql.String(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)


class Account(Base):

    __tablename__ = "account"

    accountName = _sql.Column(
        _sql.String(), primary_key=True, index=True, nullable=False
    )
    isBanned = _sql.Column(_sql.Boolean())
    createdAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
    updatedAt = _sql.Column(_sql.DateTime(), default=_dt.datetime.utcnow)
