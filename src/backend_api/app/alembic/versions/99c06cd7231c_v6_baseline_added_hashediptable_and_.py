"""v6 Baseline Added Eventlistener for deleting the rows every 24 hours

Revision ID: 99c06cd7231c
Revises: 
Create Date: 2024-08-09 21:05:43.164175

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "99c06cd7231c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("accountName", sa.String(), nullable=False),
        sa.Column("isBanned", sa.Boolean(), nullable=True),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("accountName"),
    )
    op.create_index(
        op.f("ix_account_accountName"), "account", ["accountName"], unique=False
    )
    op.create_table(
        "currency",
        sa.Column(
            "currencyId",
            sa.BigInteger(),
            sa.Identity(always=False, start=1, increment=1, cycle=True),
            nullable=False,
        ),
        sa.Column("tradeName", sa.String(), nullable=False),
        sa.Column("valueInChaos", sa.Float(), nullable=False),
        sa.Column("iconUrl", sa.String(), nullable=False),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("currencyId"),
    )
    op.create_index(
        op.f("ix_currency_currencyId"), "currency", ["currencyId"], unique=False
    )
    op.create_index(
        op.f("ix_currency_tradeName"), "currency", ["tradeName"], unique=False
    )
    op.create_table(
        "item_base_type",
        sa.Column("baseType", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("subCategory", sa.String(), nullable=True),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("baseType"),
    )
    op.create_index(
        op.f("ix_item_base_type_baseType"), "item_base_type", ["baseType"], unique=False
    )
    op.create_table(
        "modifier",
        sa.Column(
            "modifierId",
            sa.BigInteger(),
            sa.Identity(always=False, start=1, increment=1, cycle=True),
            nullable=False,
        ),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("minRoll", sa.Float(precision=24), nullable=True),
        sa.Column("maxRoll", sa.Float(precision=24), nullable=True),
        sa.Column("textRolls", sa.String(), nullable=True),
        sa.Column("static", sa.Boolean(), nullable=True),
        sa.Column("effect", sa.String(), nullable=False),
        sa.Column("regex", sa.String(), nullable=True),
        sa.Column("implicit", sa.Boolean(), nullable=True),
        sa.Column("explicit", sa.Boolean(), nullable=True),
        sa.Column("delve", sa.Boolean(), nullable=True),
        sa.Column("fractured", sa.Boolean(), nullable=True),
        sa.Column("synthesized", sa.Boolean(), nullable=True),
        sa.Column("unique", sa.Boolean(), nullable=True),
        sa.Column("corrupted", sa.Boolean(), nullable=True),
        sa.Column("enchanted", sa.Boolean(), nullable=True),
        sa.Column("veiled", sa.Boolean(), nullable=True),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "\n            CASE\n                WHEN modifier.static = TRUE\n                THEN (\n                    modifier.effect NOT LIKE '%%#%%'\n                    )\n                ELSE (\n                    modifier.effect LIKE '%%#%%'\n                )\n            END\n            ",
            name="check_modifier_if_not_static_then_modifier_contains_hashtag",
        ),
        sa.CheckConstraint(
            ' modifier."maxRoll" >= modifier."minRoll" ',
            name="check_modifier_maxRoll_greaterThan_minRoll",
        ),
        sa.CheckConstraint(
            '\n            CASE \n                WHEN (modifier.static = TRUE) \n                THEN (\n                        (modifier."minRoll" IS NULL AND modifier."maxRoll" IS NULL)\n                        AND modifier."textRolls" IS NULL \n                        AND modifier.regex IS NULL\n                    )\n                ELSE (\n                        (\n                            (\n                                (modifier."minRoll" IS NOT NULL AND modifier."maxRoll" IS NOT NULL)\n                                AND modifier."textRolls" IS NULL\n                            )\n                            OR\n                            (\n                                (modifier."minRoll" IS  NULL AND modifier."maxRoll" IS  NULL)\n                                AND modifier."textRolls" IS NOT NULL\n                            )\n                        )\n                        AND modifier.regex IS NOT NULL\n                    )\n            END\n            ',
            name="check_modifier_if_static_else_check_rolls_and_regex",
        ),
        sa.PrimaryKeyConstraint("modifierId"),
        sa.UniqueConstraint("modifierId", "position"),
    )
    op.create_index(
        op.f("ix_modifier_modifierId"), "modifier", ["modifierId"], unique=False
    )
    op.create_index(
        op.f("ix_modifier_position"), "modifier", ["position"], unique=False
    )
    op.create_table(
        "stash",
        sa.Column("stashId", sa.String(), nullable=False),
        sa.Column("accountName", sa.String(), nullable=False),
        sa.Column("public", sa.Boolean(), nullable=False),
        sa.Column("league", sa.String(), nullable=False),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["accountName"],
            ["account.accountName"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("stashId"),
    )
    op.create_index(op.f("ix_stash_stashId"), "stash", ["stashId"], unique=False)
    op.create_table(
        "item",
        sa.Column(
            "itemId",
            sa.BigInteger(),
            sa.Identity(always=False, start=1, increment=1, cycle=True),
            nullable=False,
        ),
        sa.Column("gameItemId", sa.String(), nullable=False),
        sa.Column("stashId", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("iconUrl", sa.String(), nullable=True),
        sa.Column("league", sa.String(), nullable=False),
        sa.Column("typeLine", sa.String(), nullable=False),
        sa.Column("baseType", sa.String(), nullable=False),
        sa.Column("ilvl", sa.SmallInteger(), nullable=False),
        sa.Column("rarity", sa.String(), nullable=False),
        sa.Column("identified", sa.Boolean(), nullable=False),
        sa.Column("forumNote", sa.String(), nullable=True),
        sa.Column("currencyAmount", sa.Float(precision=24), nullable=True),
        sa.Column("currencyId", sa.BigInteger(), nullable=True),
        sa.Column("corrupted", sa.Boolean(), nullable=True),
        sa.Column("delve", sa.Boolean(), nullable=True),
        sa.Column("fractured", sa.Boolean(), nullable=True),
        sa.Column("synthesized", sa.Boolean(), nullable=True),
        sa.Column("replica", sa.Boolean(), nullable=True),
        sa.Column("elder", sa.Boolean(), nullable=True),
        sa.Column("shaper", sa.Boolean(), nullable=True),
        sa.Column("influences", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("searing", sa.Boolean(), nullable=True),
        sa.Column("tangled", sa.Boolean(), nullable=True),
        sa.Column("isRelic", sa.Boolean(), nullable=True),
        sa.Column("prefixes", sa.SmallInteger(), nullable=True),
        sa.Column("suffixes", sa.SmallInteger(), nullable=True),
        sa.Column("foilVariation", sa.SmallInteger(), nullable=True),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["baseType"],
            ["item_base_type.baseType"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["currencyId"], ["currency.currencyId"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["stashId"], ["stash.stashId"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("itemId"),
    )
    op.create_index(op.f("ix_item_gameItemId"), "item", ["gameItemId"], unique=False)
    op.create_index(op.f("ix_item_itemId"), "item", ["itemId"], unique=False)
    op.create_table(
        "item_modifier",
        sa.Column("itemId", sa.BigInteger(), nullable=False),
        sa.Column("modifierId", sa.BigInteger(), nullable=False),
        sa.Column("orderId", sa.SmallInteger(), nullable=False),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("roll", sa.Float(precision=24), nullable=True),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["itemId"], ["item.itemId"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["modifierId", "position"],
            ["modifier.modifierId", "modifier.position"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("itemId", "modifierId", "orderId"),
    )
    op.create_index(
        op.f("ix_item_modifier_itemId"), "item_modifier", ["itemId"], unique=False
    )
    op.create_index(
        op.f("ix_item_modifier_modifierId"),
        "item_modifier",
        ["modifierId"],
        unique=False,
    )
    op.create_index(
        op.f("ix_item_modifier_position"), "item_modifier", ["position"], unique=False
    )
    op.create_index(
        op.f("ix_item_modifier_orderId"),
        "item_modifier",
        ["orderId"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_item_modifier_position"), table_name="item_modifier")
    op.drop_index(op.f("ix_item_modifier_modifierId"), table_name="item_modifier")
    op.drop_index(op.f("ix_item_modifier_itemId"), table_name="item_modifier")
    op.drop_table("item_modifier")
    op.drop_index(op.f("ix_item_itemId"), table_name="item")
    op.drop_index(op.f("ix_item_gameItemId"), table_name="item")
    op.drop_table("item")
    op.drop_index(op.f("ix_stash_stashId"), table_name="stash")
    op.drop_table("stash")
    op.drop_index(op.f("ix_item_modifier_orderId"), table_name="modifier")
    op.drop_index(op.f("ix_modifier_position"), table_name="modifier")
    op.drop_index(op.f("ix_modifier_modifierId"), table_name="modifier")
    op.drop_table("modifier")
    op.drop_index(op.f("ix_item_base_type_baseType"), table_name="item_base_type")
    op.drop_table("item_base_type")
    op.drop_index(op.f("ix_currency_tradeName"), table_name="currency")
    op.drop_index(op.f("ix_currency_currencyId"), table_name="currency")
    op.drop_table("currency")
    op.drop_index(op.f("ix_account_accountName"), table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###
