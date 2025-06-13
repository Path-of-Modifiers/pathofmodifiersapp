import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Identity,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.database import Base


class Currency(Base):
    __tablename__ = "currency"

    currencyId: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    createdHoursSinceLaunch: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    valueInChaos: Mapped[float] = mapped_column(Float(4), nullable=False)
    tradeName: Mapped[str] = mapped_column(Text, nullable=False)


class ItemBaseType(Base):
    __tablename__ = "item_base_type"

    itemBaseTypeId: Mapped[int] = mapped_column(
        SmallInteger,
        Identity(start=1, increment=1),
        primary_key=True,
    )
    baseType: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )
    category: Mapped[str] = mapped_column(Text, nullable=False)
    subCategory: Mapped[str | None] = mapped_column(Text)
    relatedUniques: Mapped[str | None] = mapped_column(Text)


class _ItemBase:
    name: Mapped[str | None] = mapped_column(Text, nullable=False)
    itemBaseTypeId: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "item_base_type.itemBaseTypeId", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        nullable=False,
    )
    createdHoursSinceLaunch: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    league: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    itemId: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1, always=True),
        primary_key=True,  # Primary key constraint gets removed on hypertable creation
    )
    currencyId: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("currency.currencyId", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    ilvl: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    currencyAmount: Mapped[float] = mapped_column(Float(4), nullable=False)
    rarity: Mapped[str] = mapped_column(Text, nullable=False)


class Item(_ItemBase, Base):
    # Hypertable
    # For hypertable specs, see alembic revision `cc29b89156db'
    __tablename__ = "item"

    itemId: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1),
        primary_key=True,  # Primary key constraint gets removed on hypertable creation
    )
    prefixes: Mapped[int | None] = mapped_column(SmallInteger)
    suffixes: Mapped[int | None] = mapped_column(SmallInteger)
    foilVariation: Mapped[int | None] = mapped_column(SmallInteger)
    identified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesised: Mapped[bool | None] = mapped_column(Boolean)
    replica: Mapped[bool | None] = mapped_column(Boolean)
    searing: Mapped[bool | None] = mapped_column(Boolean)
    tangled: Mapped[bool | None] = mapped_column(Boolean)
    influences: Mapped[dict[str, str] | None] = mapped_column(
        JSONB
    )  # elder, shaper, warlord etc

    __table_args__ = (
        Index(
            "ix_item_name_itemBaseTypeId_createdHoursSinceLaunch_league",
            "name",
            "itemBaseTypeId",
            "createdHoursSinceLaunch",
            "league",
        ),
    )


class UnidentifiedItem(_ItemBase, Base):
    """
    IS-A item relation, couldn't be bothered finding the actual way to implement it.
    However, it is missing `suffixes` and `prefixes` attributes, and identified must be false.
    """

    __tablename__ = "unidentified_item"

    nItems: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    identified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    aggregated: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index(
            "ix_unid_item_name_itemBaseTypeId_createdHoursSinceLaunch_league",
            "name",
            "itemBaseTypeId",
            "createdHoursSinceLaunch",
            "league",
        ),
        CheckConstraint(
            """
            identified IS NOT TRUE
            """,
            "identified_is_false",
        ),
    )


class Modifier(Base):
    __tablename__ = "modifier"

    modifierId: Mapped[int] = mapped_column(
        SmallInteger,
        Identity(start=1, increment=1, cycle=True),
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    minRoll: Mapped[float | None] = mapped_column(Float(4))
    maxRoll: Mapped[float | None] = mapped_column(Float(4))
    implicit: Mapped[bool | None] = mapped_column(Boolean)
    explicit: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesised: Mapped[bool | None] = mapped_column(Boolean)
    unique: Mapped[bool | None] = mapped_column(Boolean)
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    enchanted: Mapped[bool | None] = mapped_column(Boolean)
    veiled: Mapped[bool | None] = mapped_column(Boolean)
    static: Mapped[bool | None] = mapped_column(Boolean)
    effect: Mapped[str] = mapped_column(Text, nullable=False)
    relatedUniques: Mapped[str | None] = mapped_column(Text)
    textRolls: Mapped[str | None] = mapped_column(Text)
    regex: Mapped[str | None] = mapped_column(Text)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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
    # Hypertable
    # For hypertable specs, see alembic revision `cc29b89156db'

    __tablename__ = "item_modifier"

    modifierId: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "modifier.modifierId",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    createdHoursSinceLaunch: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    itemId: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        primary_key=True,  # Primary key constraint gets removed on hypertable creation
    )
    roll: Mapped[float | None] = mapped_column(
        Float(4),
    )
    __table_args__ = (
        Index(
            "ix_item_modifierId_createdHoursSinceLaunch_roll_itemId",
            "modifierId",
            "createdHoursSinceLaunch",
            "roll",
            "itemId",
        ),
    )


class User(Base):
    __tablename__ = "pom_user"

    userId: Mapped[UUID] = mapped_column(  # type: ignore
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    rateLimitTier: Mapped[int | None] = mapped_column(
        SmallInteger
    )  # 0 = basic limit usage
    isActive: Mapped[bool | None] = mapped_column(Boolean)
    isSuperuser: Mapped[bool | None] = mapped_column(Boolean)
    isBanned: Mapped[bool | None] = mapped_column(Boolean)
    hashedPassword: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    # Check contstraint where username can only hold letters and numbers with multiple languages
    __table_args__ = (
        CheckConstraint(
            "username ~* '^[[:alnum:]_]+$'",  # Allow letters, numbers, and underscore
            name="check_username_letters_numbers_and_underscores",
        ),
    )
