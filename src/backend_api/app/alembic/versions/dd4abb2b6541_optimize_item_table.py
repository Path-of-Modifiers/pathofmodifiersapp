"""optimize item table

Revision ID: dd4abb2b6541
Revises: 965e766db0a0
Create Date: 2026-07-23 15:20:18.565656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "dd4abb2b6541"
down_revision: Union[str, None] = "965e766db0a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "_temp_item_availability",
        sa.Column("temp_game_item_id", sa.Text(), nullable=False),  # Temporary column
        sa.Column(
            "temp_league_id", sa.SmallInteger(), nullable=False
        ),  # Temporary column
        # sa.Column("itemId", sa.Integer(), nullable=False), # Will be added later
        sa.Column("currencyId", sa.Integer(), nullable=False),
        sa.Column("currencyAmount", sa.Float(4), nullable=False),
        sa.Column("isAsync", sa.Boolean()),
        sa.Column("validFrom", sa.SmallInteger(), nullable=False),
        sa.Column("validTo", sa.SmallInteger()),
        sa.ForeignKeyConstraint(
            ["currencyId"],
            ["currency.currencyId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
    )

    op.execute("""
        INSERT INTO _temp_item_availability (
            temp_game_item_id,
            temp_league_id,
            "currencyId",
            "currencyAmount",
            "validFrom",
            "validTo"
        )
        WITH ordered AS (
            SELECT
                i.*,
                LAG(i."createdHoursSinceLaunch") OVER w AS prev_hour,
                LAG(i."leagueId")             OVER w AS prev_league,
                LAG(i."currencyId")           OVER w AS prev_currency,
                LAG(i."currencyAmount")       OVER w AS prev_amount
            FROM item i
            WINDOW w AS (
                PARTITION BY i."gameItemId"
                ORDER BY i."createdHoursSinceLaunch"
            )
        ),
        marked AS (
            SELECT
                *,
                CASE
                    WHEN 
                    prev_hour IS NULL
                    OR o."createdHoursSinceLaunch" > prev_hour + 1
                    OR o."leagueId" IS DISTINCT FROM prev_league
                    OR o."currencyId" IS DISTINCT FROM prev_currency
                    OR o."currencyAmount" IS DISTINCT FROM prev_amount
                    THEN 1
                    ELSE 0
                END AS new_listing
            FROM ordered o
        ),
        grouped AS (
            SELECT
                *,
                SUM(new_listing) OVER (
                    PARTITION BY m."gameItemId"
                    ORDER BY m."createdHoursSinceLaunch"
                ) AS grp
            FROM marked m
        ),
        collapsed AS (
            SELECT
                g."gameItemId",
                g."leagueId",
                g."currencyId",
                g."currencyAmount",
                grp,
                MIN(g."createdHoursSinceLaunch") AS "validFrom",
                MAX(g."createdHoursSinceLaunch") + 1 AS observedValidTo
            FROM grouped g
            GROUP BY
                g."gameItemId",
                g."leagueId",
                g."currencyId",
                g."currencyAmount",
                grp
        )
        SELECT
            c."gameItemId",
            c."leagueId",
            c."currencyId",
            c."currencyAmount",
            c."validFrom",
            CASE
                WHEN LEAD(grp) OVER (
                    PARTITION BY c."gameItemId"
                    ORDER BY grp
                ) IS NULL
                THEN c."validFrom" + 1
                ELSE observedValidTo
            END AS "validTo"
            
        FROM collapsed c;
    """)
    # TODO optimize when writing the plotting query
    # sa.Index("ix_item_availability_itemId_validFrom", "itemId", "validFrom"),

    with op.batch_alter_table("item") as batch_op:
        batch_op.drop_column("prefixes")
        batch_op.drop_column("suffixes")
        batch_op.drop_column("currencyAmount")
        batch_op.drop_column("currencyId")
        batch_op.execute("""
            DELETE FROM item i
            WHERE i."itemId" NOT IN (
                SELECT MIN(i2."itemId")
                FROM item i2
                GROUP BY i2."gameItemId", i2."leagueId"
            )
            """)
        batch_op.execute("""
            DELETE FROM item i
            WHERE i."itemId" NOT IN (
                SELECT im."itemId"
                FROM item_modifier im
            )
            """)
        batch_op.alter_column("itemId", new_column_name="old_item_id")

    # Rebuilds the item table to remove the hypertable.
    op.execute("""
        CREATE TABLE _item_temp AS
        SELECT DISTINCT ON ("gameItemId", "leagueId")
            ROW_NUMBER() OVER (ORDER BY "gameItemId", "leagueId") AS "itemId",
            *
        FROM item i
        ORDER BY
            "gameItemId",
            "leagueId";

        DROP TABLE item;
        ALTER TABLE _item_temp
            ALTER COLUMN "itemId" SET NOT NULL;
        ALTER TABLE _item_temp
            ALTER COLUMN "itemId" ADD GENERATED ALWAYS AS IDENTITY;
        SELECT setval(
            pg_get_serial_sequence('_item_temp', 'itemId'),
            COALESCE((SELECT MAX("itemId") FROM _item_temp), 1),
            TRUE
        );

        ALTER TABLE _item_temp RENAME TO item;
    """)

    with op.batch_alter_table("item") as batch_op:
        batch_op.drop_column("delve")
        batch_op.drop_column("foilVariation")
        batch_op.create_primary_key("item_pkey", ["itemId"])
        batch_op.create_foreign_key(
            "fk_item_league",
            "league",
            ["leagueId"],
            ["leagueId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )
        batch_op.create_foreign_key(
            "fk_item_item_base_type",
            "item_base_type",
            ["itemBaseTypeId"],
            ["itemBaseTypeId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )
        batch_op.alter_column("gameItemId", nullable=False)
        batch_op.alter_column("leagueId", nullable=False)
        batch_op.alter_column(
            "createdHoursSinceLaunch", new_column_name="firstObserved", nullable=False
        )
        batch_op.alter_column("name", nullable=False)
        batch_op.alter_column("itemBaseTypeId", nullable=False)
        batch_op.alter_column("rarity", nullable=False)
        batch_op.alter_column("ilvl", nullable=False)
        batch_op.alter_column("identified", nullable=False)

        # TODO update when writing the plotting query
        batch_op.create_index(
            "ix_item_leagueId_itemBaseTypeId",
            ["leagueId", "itemBaseTypeId", "firstObserved"],
        )

    op.create_table(
        "item_availability",
        sa.Column(
            "availabilityId",
            sa.Integer(),
            sa.Identity(always=False, start=1, increment=1),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("itemId", sa.Integer(), nullable=False),
        sa.Column("currencyId", sa.Integer(), nullable=False),
        sa.Column("currencyAmount", sa.Float(4), nullable=False),
        sa.Column("isAsync", sa.Boolean()),
        sa.Column("validFrom", sa.SmallInteger(), nullable=False),
        sa.Column("validTo", sa.SmallInteger()),
        sa.ForeignKeyConstraint(
            ["currencyId"],
            ["currency.currencyId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["itemId"],
            ["item.itemId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        # TODO optimize when writing the plotting query
        sa.Index("ix_item_availability_itemId_validFrom", "itemId", "validFrom"),
    )
    op.execute("""
    INSERT INTO item_availability (
        "itemId",
        "currencyId",
        "currencyAmount",
        "validFrom",
        "validTo"
        )
    SELECT 
        i."itemId",
        ia."currencyId",
        ia."currencyAmount",
        ia."validFrom",
        ia."validTo"
    FROM item i
    LEFT JOIN _temp_item_availability ia
        ON i."gameItemId" = ia.temp_game_item_id AND i."leagueId" = ia.temp_league_id;
    """)

    op.drop_table("_temp_item_availability")

    # Rebuilds the item_modifier table to use the new itemId, and to remove the hypertable.
    op.execute("""
        CREATE TABLE _item_modifier_temp AS
        SELECT 
            i."itemId"::INT,
            im."modifierId",
            im.position,
            im.roll
        FROM item i
        LEFT JOIN item_modifier im
            ON i.old_item_id = im."itemId";
        
        DROP TABLE item_modifier;

        ALTER TABLE _item_modifier_temp RENAME TO item_modifier;
    """)
    op.drop_column("item", "old_item_id")

    with op.batch_alter_table("item_modifier") as batch_op:
        batch_op.alter_column("itemId", nullable=False)
        batch_op.alter_column("modifierId", nullable=False)
        batch_op.alter_column("position", nullable=False)
        batch_op.alter_column(
            "roll", existing_type=sa.Float(), type_=sa.Float(4), nullable=True
        )
        batch_op.create_primary_key(
            "item_modifier_pkey", ["itemId", "modifierId", "position"]
        )
        batch_op.create_foreign_key(
            "fk_item_modifier_item",
            "item",
            ["itemId"],
            ["itemId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
        batch_op.create_foreign_key(
            "fk_item_modifier_modifier",
            "modifier",
            ["modifierId", "position"],
            ["modifierId", "position"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )


def downgrade() -> None:
    raise NotImplementedError("Downgrade is not supported for this migration")
    # Remove the FK before restoring the old item schema.
    # op.drop_constraint(
    #     "fk_item_availability_item",
    #     "item_availability",
    #     type_="foreignkey",
    # )
    # # Restore the columns that were removed by upgrade().
    # with op.batch_alter_table("item") as batch_op:
    #     batch_op.drop_constraint(
    #         "item_pkey",
    #         type_="primary",
    #     )

    #     batch_op.alter_column(
    #         "itemId",
    #         new_column_name="gameItemId",
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "itemId",
    #             sa.Integer(),
    #             sa.Identity(always=False, start=1, increment=1),
    #             nullable=False,
    #         )
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "prefixes",
    #             sa.Integer(),
    #             nullable=False,
    #             server_default="0",
    #         )
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "suffixes",
    #             sa.Integer(),
    #             nullable=False,
    #             server_default="0",
    #         )
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "currencyId",
    #             sa.Integer(),
    #             nullable=True,
    #         )
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "currencyAmount",
    #             sa.Float(4),
    #             nullable=True,
    #         )
    #     )

    #     batch_op.add_column(
    #         sa.Column(
    #             "createdHoursSinceLaunch",
    #             sa.Integer(),
    #             nullable=True,
    #         )
    #     )  # Build the complete historical item set from item_availability.
    # #
    # # The upgraded table still contains one representative item row for
    # # every (gameItemId, leagueId). We use that row as the template for
    # # all of the columns that were not part of item_availability.
    # #
    # # validFrom is inclusive and validTo is exclusive.
    # op.execute("""
    #     CREATE TEMP TABLE _item_template
    #     ON COMMIT DROP
    #     AS
    #     SELECT DISTINCT ON ("gameItemId", "leagueId")
    #         "gameItemId",
    #         "foilVariation",
    #         "identified",
    #         "corrupted",
    #         "delve",
    #         "fractured",
    #         "synthesised",
    #         "replica",
    #         "searing",
    #         "tangled",
    #         "influences",
    #         "name",
    #         "itemBaseTypeId",
    #         "ilvl",
    #         "rarity",
    #         "leagueId"
    #     FROM item
    #     ORDER BY
    #         "gameItemId",
    #         "leagueId",
    #         "itemId";
    # """)

    # # Remove the representative rows created by the upgrade. They are
    # # replaced by the reconstructed hourly history below.
    # #
    # # No metadata is lost because it has already been copied into the
    # # temporary template table.
    # op.execute("""
    #     DELETE FROM item;
    # """)

    # # Reconstruct one row per hour.
    # #
    # # item_availability contains intervals:
    # #
    # #   [validFrom, validTo)
    # #
    # # so generate_series(validFrom, validTo - 1) gives exactly the
    # # original hourly rows represented by each interval.
    # #
    # # A new itemId is generated by the identity column.
    # op.execute("""
    #     INSERT INTO item (
    #         "gameItemId",
    #         "prefixes",
    #         "suffixes",
    #         "foilVariation",
    #         "identified",
    #         "corrupted",
    #         "delve",
    #         "fractured",
    #         "synthesised",
    #         "replica",
    #         "searing",
    #         "tangled",
    #         "influences",
    #         "name",
    #         "itemBaseTypeId",
    #         "createdHoursSinceLaunch",
    #         "leagueId",
    #         "currencyId",
    #         "ilvl",
    #         "currencyAmount",
    #         "rarity"
    #     )
    #     SELECT
    #         ia."itemId" AS "gameItemId",
    #         0 AS "prefixes",
    #         0 AS "suffixes",
    #         t."foilVariation",
    #         t."identified",
    #         t."corrupted",
    #         t."delve",
    #         t."fractured",
    #         t."synthesised",
    #         t."replica",
    #         t."searing",
    #         t."tangled",
    #         t."influences",
    #         t."name",
    #         t."itemBaseTypeId",
    #         h."createdHoursSinceLaunch",
    #         ia."leagueId",
    #         ia."currencyId",
    #         t."ilvl",
    #         ia."currencyAmount",
    #         t."rarity"
    #     FROM item_availability ia
    #     JOIN _item_template t
    #         ON t."gameItemId" = ia."itemId"
    #         AND t."leagueId" = ia."leagueId"
    #     CROSS JOIN LATERAL generate_series(
    #         ia."validFrom",
    #         ia."validTo" - 1
    #     ) AS h("createdHoursSinceLaunch")
    #     ORDER BY
    #         ia."itemId",
    #         ia."leagueId",
    #         h."createdHoursSinceLaunch";
    # """)

    # # Restore the original identity primary key.
    # with op.batch_alter_table("item") as batch_op:
    #     batch_op.create_primary_key(
    #         "item_pkey",
    #         ["itemId"],
    #     )
    # op.drop_table("item_availability")
