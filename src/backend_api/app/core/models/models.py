import sqlalchemy as _sql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func

from app.core.models.database import Base


def update(self, **new_data):
    for field, value in new_data.items():
        setattr(self, field, value)


Base.update = update


class Currency(Base):

    __tablename__ = "currency"

    currencyId = _sql.Column(
        _sql.BigInteger,
        _sql.Identity(start=1, increment=1, cycle=True),
        primary_key=True,
        index=True,
        nullable=False,
    )
    tradeName = _sql.Column(_sql.String(), index=True, nullable=False)
    valueInChaos = _sql.Column(_sql.Float(), nullable=False)
    iconUrl = _sql.Column(_sql.String(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)


class ItemBaseType(Base):

    __tablename__ = "item_base_type"

    baseType = _sql.Column(_sql.String(), nullable=False, primary_key=True, index=True)
    category = _sql.Column(_sql.String(), nullable=False)
    subCategory = _sql.Column(_sql.String())
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)
    updatedAt = _sql.Column(
        _sql.DateTime(),
        onupdate=func.now(),
    )


class Item(Base):

    __tablename__ = "item"

    itemId = _sql.Column(
        _sql.BigInteger,
        _sql.Identity(start=1, increment=1, cycle=True),
        primary_key=True,
        index=True,
        nullable=False,
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
        _sql.ForeignKey(
            "item_base_type.baseType", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    ilvl = _sql.Column(_sql.SmallInteger(), nullable=False)
    rarity = _sql.Column(_sql.String(), nullable=False)
    identified = _sql.Column(_sql.Boolean(), nullable=False)
    forumNote = _sql.Column(_sql.String())
    currencyAmount = _sql.Column(_sql.Float(24))
    currencyId = _sql.Column(
        _sql.BigInteger(), _sql.ForeignKey("currency.currencyId", ondelete="RESTRICT")
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
    foilVariation = _sql.Column(_sql.SmallInteger())
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)


class Modifier(Base):

    __tablename__ = "modifier"

    modifierId = _sql.Column(
        _sql.BigInteger,
        _sql.Identity(start=1, increment=1, cycle=True),
        nullable=False,
        index=True,
        primary_key=True,
    )
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    minRoll = _sql.Column(_sql.Float(24))
    maxRoll = _sql.Column(_sql.Float(24))
    textRolls = _sql.Column(_sql.String())
    static = _sql.Column(_sql.Boolean())
    effect = _sql.Column(_sql.String(), nullable=False)
    regex = _sql.Column(_sql.String())
    implicit = _sql.Column(_sql.Boolean())
    explicit = _sql.Column(_sql.Boolean())
    delve = _sql.Column(_sql.Boolean())
    fractured = _sql.Column(_sql.Boolean())
    synthesized = _sql.Column(_sql.Boolean())
    unique = _sql.Column(_sql.Boolean())
    corrupted = _sql.Column(_sql.Boolean())
    enchanted = _sql.Column(_sql.Boolean())
    veiled = _sql.Column(_sql.Boolean())
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)
    updatedAt = _sql.Column(
        _sql.DateTime(),
        onupdate=func.now(),
    )

    __table_args__ = (
        _sql.CheckConstraint(
            """
            CASE 
                WHEN (modifier.static = TRUE) 
                THEN (
                        (modifier."minRoll" IS NULL AND modifier."maxRoll" IS NULL)
                        AND modifier."textRolls" IS NULL 
                        AND modifier.regex IS NULL
                    )
                ELSE (
                        (
                            (
                                (modifier."minRoll" IS NOT NULL AND modifier."maxRoll" IS NOT NULL)
                                AND modifier."textRolls" IS NULL
                            )
                            OR
                            (
                                (modifier."minRoll" IS  NULL AND modifier."maxRoll" IS  NULL)
                                AND modifier."textRolls" IS NOT NULL
                            )
                        )
                        AND modifier.regex IS NOT NULL
                    )
            END
            """,
            name="check_modifier_if_static_else_check_rolls_and_regex",
        ),
        _sql.CheckConstraint(
            """
            CASE
                WHEN modifier.static = TRUE
                THEN (
                    modifier.effect NOT LIKE '%#%'
                    )
                ELSE (
                    modifier.effect LIKE '%#%'
                )
            END
            """,
            name="check_modifier_if_not_static_then_modifier_contains_hashtag",
        ),
        _sql.CheckConstraint(
            """ modifier."maxRoll" >= modifier."minRoll" """,
            name="check_modifier_maxRoll_greaterThan_minRoll",
        ),
        _sql.UniqueConstraint(modifierId, position),
    )


class ItemModifier(Base):

    __tablename__ = "item_modifier"

    itemId = _sql.Column(
        _sql.BigInteger(),
        _sql.ForeignKey("item.itemId", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    modifierId = _sql.Column(_sql.BigInteger(), nullable=False, index=True)
    position = _sql.Column(_sql.SmallInteger(), nullable=False, index=True)
    roll = _sql.Column(_sql.Float(24))
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)
    updatedAt = _sql.Column(
        _sql.DateTime(),
        onupdate=func.now(),
    )

    __table_args__ = (
        _sql.PrimaryKeyConstraint(itemId, modifierId),
        _sql.ForeignKeyConstraint(
            [modifierId, position],
            ["modifier.modifierId", "modifier.position"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )


class Stash(Base):

    __tablename__ = "stash"

    stashId = _sql.Column(_sql.String(), primary_key=True, index=True, nullable=False)
    accountName = _sql.Column(
        _sql.String(),
        _sql.ForeignKey("account.accountName", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    public = _sql.Column(_sql.Boolean(), nullable=False)
    league = _sql.Column(_sql.String(), nullable=False)
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)
    updatedAt = _sql.Column(
        _sql.DateTime(),
        onupdate=func.now(),
    )


class Account(Base):

    __tablename__ = "account"

    accountName = _sql.Column(
        _sql.String(), primary_key=True, index=True, nullable=False
    )
    isBanned = _sql.Column(_sql.Boolean())
    createdAt = _sql.Column(_sql.DateTime(), default=func.now(), nullable=False)
    updatedAt = _sql.Column(
        _sql.DateTime(),
        onupdate=func.now(),
    )
