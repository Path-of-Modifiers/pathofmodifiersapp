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
    valueInChaos: Mapped[float] = mapped_column(Float(4), nullable=False)
    iconUrl: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )


class ItemBaseType(Base):
    __tablename__ = "item_base_type"

    baseType: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String, nullable=False)
    subCategory: Mapped[str | None] = mapped_column(String)
    relatedUniques: Mapped[str | None] = mapped_column(String)


class Item(Base):
    __tablename__ = "item"

    itemId: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1, cycle=True),
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String, index=True)
    league: Mapped[str] = mapped_column(
        String, nullable=False
    )  # TODO: Add index when we add more leagues
    baseType: Mapped[str] = mapped_column(
        String,
        ForeignKey("item_base_type.baseType", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    typeLine: Mapped[str] = mapped_column(String, nullable=False)
    ilvl: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    rarity: Mapped[str] = mapped_column(String, nullable=False)
    identified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    currencyAmount: Mapped[float | None] = mapped_column(Float(4))
    currencyId: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("currency.currencyId", ondelete="RESTRICT")
    )
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesised: Mapped[bool | None] = mapped_column(Boolean)
    replica: Mapped[bool | None] = mapped_column(Boolean)
    influences: Mapped[dict[str, str] | None] = mapped_column(
        JSONB
    )  # elder, shaper, warlord etc
    searing: Mapped[bool | None] = mapped_column(Boolean)
    tangled: Mapped[bool | None] = mapped_column(Boolean)
    isRelic: Mapped[bool | None] = mapped_column(Boolean)
    prefixes: Mapped[int | None] = mapped_column(SmallInteger)
    suffixes: Mapped[int | None] = mapped_column(SmallInteger)
    foilVariation: Mapped[int | None] = mapped_column(SmallInteger)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )


class Modifier(Base):
    # Timescale hypertable (see alembic revisions timescale definitions)
    # SQLAlchemy timescale dialect is limited and not regularily updated
    # We have baseTypeId a part of pkey, since the table segments on this attribute
    # TODO: Add dialect if the sqlalchemy timescale library gets updated
    __tablename__ = "modifier"

    modifierId: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1, cycle=True),
        nullable=False,
        index=True,
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False, index=True)
    relatedUniques: Mapped[str | None] = mapped_column(String)
    minRoll: Mapped[float | None] = mapped_column(Float(4))
    maxRoll: Mapped[float | None] = mapped_column(Float(4))
    textRolls: Mapped[str | None] = mapped_column(String)
    static: Mapped[bool | None] = mapped_column(Boolean)
    effect: Mapped[str] = mapped_column(String, nullable=False)
    regex: Mapped[str | None] = mapped_column(String)
    implicit: Mapped[bool | None] = mapped_column(Boolean)
    explicit: Mapped[bool | None] = mapped_column(Boolean)
    delve: Mapped[bool | None] = mapped_column(Boolean)
    fractured: Mapped[bool | None] = mapped_column(Boolean)
    synthesised: Mapped[bool | None] = mapped_column(Boolean)
    unique: Mapped[bool | None] = mapped_column(Boolean)
    corrupted: Mapped[bool | None] = mapped_column(Boolean)
    enchanted: Mapped[bool | None] = mapped_column(Boolean)
    veiled: Mapped[bool | None] = mapped_column(Boolean)
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
    # Segments by modifierId and createdAt
    __tablename__ = "item_modifier"

    itemId: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("item.itemId", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,  # Dummy pk since we removing the pks on hypertable creation
        index=True,
    )
    modifierId: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    roll: Mapped[float | None] = mapped_column(Float(4))
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [modifierId],
            ["modifier.modifierId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
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
