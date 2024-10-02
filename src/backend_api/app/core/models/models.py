import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.database import Base


class Currency(Base):
    __tablename__ = "currency"

    currencyId: Mapped[int] = mapped_column(
        BigInteger, Identity(), primary_key=True, index=True, nullable=False
    )
    tradeName: Mapped[str] = mapped_column(String, index=True, nullable=False)
    valueInChaos: Mapped[float] = mapped_column(Float(), nullable=False)
    iconUrl: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )


class ItemBaseType(Base):
    __tablename__ = "item_base_type"

    baseType: Mapped[str] = mapped_column(
        String, nullable=False, primary_key=True, index=True
    )
    category: Mapped[str] = mapped_column(String, nullable=False)
    subCategory: Mapped[str | None] = mapped_column(String)


class Item(Base):
    __tablename__ = "item"

    itemId: Mapped[int] = mapped_column(
        BigInteger, Identity(), primary_key=True, index=True, nullable=False
    )
    gameItemId: Mapped[str] = mapped_column(String, index=True, nullable=False)
    stashId: Mapped[str] = mapped_column(
        String,
        ForeignKey("stash.stashId", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String)
    iconUrl: Mapped[str | None] = mapped_column(String)
    league: Mapped[str] = mapped_column(String, nullable=False)
    typeLine: Mapped[str] = mapped_column(String, nullable=False)
    baseType: Mapped[str] = mapped_column(
        String,
        ForeignKey("item_base_type.baseType", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    ilvl: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    rarity: Mapped[str] = mapped_column(String, nullable=False)
    identified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    forumNote: Mapped[str | None] = mapped_column(String)
    currencyAmount: Mapped[float | None] = mapped_column(Float(24))
    currencyId: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("currency.currencyId", ondelete="RESTRICT")
    )
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesized: Mapped[bool | None] = mapped_column(Boolean)
    replica: Mapped[bool | None] = mapped_column(Boolean)
    elder: Mapped[bool | None] = mapped_column(Boolean)
    shaper: Mapped[bool | None] = mapped_column(Boolean)
    influences: Mapped[dict | None] = mapped_column(JSONB)
    searing: Mapped[bool | None] = mapped_column(Boolean)
    tangled: Mapped[bool | None] = mapped_column(Boolean)
    isRelic: Mapped[bool | None] = mapped_column(Boolean)
    prefixes: Mapped[int | None] = mapped_column(SmallInteger)
    suffixes: Mapped[int | None] = mapped_column(SmallInteger)
    foilVariation: Mapped[int | None] = mapped_column(SmallInteger)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )


class Modifier(Base):
    __tablename__ = "modifier"

    modifierId: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1, cycle=True),
        nullable=False,
        index=True,
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    minRoll: Mapped[float | None] = mapped_column(Float(24))
    maxRoll: Mapped[float | None] = mapped_column(Float(24))
    textRolls: Mapped[str | None] = mapped_column(String)
    static: Mapped[bool | None] = mapped_column(Boolean)
    effect: Mapped[str] = mapped_column(String, nullable=False)
    regex: Mapped[str | None] = mapped_column(String)
    implicit: Mapped[bool | None] = mapped_column(Boolean)
    explicit: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesized: Mapped[bool | None] = mapped_column(Boolean)
    unique: Mapped[bool | None] = mapped_column(Boolean)
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    enchanted: Mapped[bool | None] = mapped_column(Boolean)
    veiled: Mapped[bool | None] = mapped_column(Boolean)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
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
        CheckConstraint(
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
        CheckConstraint(
            """ modifier."maxRoll" >= modifier."minRoll" """,
            name="check_modifier_maxRoll_greaterThan_minRoll",
        ),
        UniqueConstraint(modifierId, position),
    )


class ItemModifier(Base):
    __tablename__ = "item_modifier"

    itemId: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("item.itemId", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    modifierId: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    orderId: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    roll: Mapped[float | None] = mapped_column(Float(24))
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(),
        onupdate=func.now(),
    )

    __table_args__ = (
        PrimaryKeyConstraint(itemId, modifierId, orderId),
        ForeignKeyConstraint(
            [modifierId, position],
            ["modifier.modifierId", "modifier.position"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )


class Stash(Base):
    __tablename__ = "stash"

    stashId: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, nullable=False
    )
    accountName: Mapped[str] = mapped_column(
        String,
        ForeignKey("account.accountName", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    public: Mapped[bool] = mapped_column(Boolean, nullable=False)
    league: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(),
        onupdate=func.now(),
    )


class Account(Base):
    __tablename__ = "account"

    accountName: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, nullable=False
    )
    isBanned: Mapped[bool | None] = mapped_column(Boolean)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(),
        onupdate=func.now(),
    )


class User(Base):
    __tablename__ = "pom_user"

    userId: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    hashedPassword: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    isActive: Mapped[bool | None] = mapped_column(Boolean)
    isSuperuser: Mapped[bool | None] = mapped_column(Boolean)
    rateLimitTier: Mapped[int | None] = mapped_column(
        SmallInteger
    )  # 0 = basic limit usage
    isBanned: Mapped[bool | None] = mapped_column(Boolean)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(),
        onupdate=func.now(),
    )

    # Check contstraint where username can only hold letters and numbers with multiple languages
    __table_args__ = (
        CheckConstraint(
            "username ~* '^[[:alnum:]_]+$'",  # Allow letters, numbers, and underscore
            name="check_username_letters_numbers_and_underscores",
        ),
    )
