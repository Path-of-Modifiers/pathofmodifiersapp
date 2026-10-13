"""optimize item table

Revision ID: ee1239y6yfda
Revises: 965e766db0a0
Create Date: 2026-09-18 19:54:18.565656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ee1239y6yfda"
down_revision: Union[str, None] = "965e766db0a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "currency_type",
        sa.Column(
            "currencyId",
            sa.SmallInteger(),
            sa.Identity(always=False, start=1, increment=1),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("tradeName", sa.Text(), nullable=False),
    )

    op.execute("""
        INSERT INTO currency_type (name, "tradeName")
        SELECT DISTINCT 'TEMP_NAME', c."tradeName"
        FROM currency c;
    """)

    op.create_table(
        "currency_price",
        sa.Column(
            "currencyId",
            sa.SmallInteger(),
            nullable=False,
        ),
        sa.Column("leagueId", sa.SmallInteger(), nullable=False),
        sa.Column("createdHoursSinceLaunch", sa.SmallInteger(), nullable=False),
        sa.Column("valueInChaos", sa.Float(4), nullable=False),
        sa.PrimaryKeyConstraint("currencyId", "leagueId", "createdHoursSinceLaunch"),
        sa.ForeignKeyConstraint(
            ["currencyId"],
            ["currency_type.currencyId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["leagueId"], ["league.leagueId"], ondelete="CASCADE", onupdate="CASCADE"
        ),
    )

    op.execute("""
        INSERT INTO currency_price
        SELECT
            ct."currencyId",
            c."leagueId",
            c."createdHoursSinceLaunch",
            c."valueInChaos"
        FROM currency c
        JOIN currency_type ct
            ON c."tradeName" = ct."tradeName";
    """)

    op.drop_constraint("item_currencyId_fkey", "item", type_="foreignkey")
    op.drop_constraint("item_currencyId_fkey1", "item", type_="foreignkey")
    op.execute("""
        UPDATE item i
        SET "currencyId"=ct."currencyId"
        FROM currency c
        JOIN currency_type ct
            ON ct."tradeName" = c."tradeName"
        WHERE i."currencyId" = c."currencyId";
    """)

    op.drop_constraint(
        "unidentified_item_currencyId_fkey", "unidentified_item", type_="foreignkey"
    )
    op.execute("""
        UPDATE unidentified_item ui
        SET "currencyId"=ct."currencyId"
        FROM currency c
        JOIN currency_type ct
            ON ct."tradeName" = c."tradeName"
        WHERE ui."currencyId" = c."currencyId";
    """)

    op.drop_table("currency")

    op.alter_column(
        "item",
        "currencyId",
        existing_type=sa.Integer(),
        type_=sa.SmallInteger(),
    )
    op.create_foreign_key(
        None,
        "item",
        "currency_type",
        ["currencyId"],
        ["currencyId"],
    )

    op.alter_column(
        "unidentified_item",
        "currencyId",
        existing_type=sa.Integer(),
        type_=sa.SmallInteger(),
    )
    op.create_foreign_key(
        None,
        "unidentified_item",
        "currency_type",
        ["currencyId"],
        ["currencyId"],
    )


def downgrade() -> None:
    raise NotImplementedError("Downgrade is not supported for this migration")
