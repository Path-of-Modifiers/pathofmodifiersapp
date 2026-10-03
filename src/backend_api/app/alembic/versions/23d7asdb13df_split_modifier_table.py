"""optimize item table

Revision ID: 23d7asdb13df
Revises: dd4abb2b6541
Create Date: 2026-07-23 15:20:18.565656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from backend_api.app.alembic.replaceable_objects.main import ReplaceableTrigger

# revision identifiers, used by Alembic.
revision: str = "23d7asdb13df"
down_revision: Union[str, None] = "dd4abb2b6541"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

modifier_id_trigger = ReplaceableTrigger(
    "increment_modifier_id",
    "modifier",
    """
    RETURNS trigger AS ${name}$
    DECLARE
        exists boolean;
    BEGIN
        exists := EXISTS(SELECT 1 FROM modifier WHERE "effect" = NEW.effect);
        IF NOT exists THEN
            NEW."modifierId" := nextval('modifier_id_seq');

        ELSIF exists THEN
            NEW."modifierId" := (SELECT "modifierId" FROM modifier WHERE "effect" = NEW.effect LIMIT 1);
        END IF;

        RETURN NEW;
    END;
    ${name}$ LANGUAGE plpgsql;
    """,
    """
    BEFORE INSERT ON {table}
	FOR EACH ROW
	EXECUTE FUNCTION {name}();
    """,
)


def upgrade() -> None:
    op.drop_trigger(modifier_id_trigger)

    op.execute("""
        DROP SEQUENCE modifier_id_seq;
    """)

    op.create_table(
        "modifier_roll",
        sa.Column("modifierId", sa.SmallInteger(), nullable=False),
        sa.Column("position", sa.SmallInteger(), nullable=False),
        sa.Column("minRoll", sa.Float(4)),
        sa.Column("maxRoll", sa.Float(4)),
        sa.Column("textRolls", sa.ARRAY(sa.Text())),
        sa.PrimaryKeyConstraint("modifierId", "position"),
        sa.CheckConstraint(
            """ modifier_roll."maxRoll" >= modifier_roll."minRoll" """,
            name="check_modifier_maxRoll_greaterThan_minRoll",
        ),
    )

    op.execute("""
        INSERT INTO modifier_roll
        SELECT
            m."modifierId",
            m.position,
            m."minRoll",
            m."maxRoll",
            string_to_array(m."textRolls", '|')
        FROM modifier m
    """)

    with op.batch_alter_table("item_modifier") as batch_op:
        batch_op.drop_constraint("fk_item_modifier_modifier", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_item_modifier_modifier_roll",
            "modifier_roll",
            ["modifierId", "position"],
            ["modifierId", "position"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )

    with op.batch_alter_table("modifier") as batch_op:
        batch_op.drop_constraint("modifier_pkey", type_="primary")
        batch_op.execute("""
            DELETE FROM modifier m
            WHERE m.position > 0
        """)
        batch_op.drop_column("position")
        batch_op.drop_column("minRoll")
        batch_op.drop_column("maxRoll")
        batch_op.drop_column("textRolls")
        batch_op.create_primary_key("pk_modifier", ["modifierId"])
        batch_op.create_unique_constraint("uq_effect", ["effect"])

    with op.batch_alter_table("modifier_roll") as batch_op:
        batch_op.create_foreign_key(
            "fk_modifier_roll_modifier",
            "modifier",
            ["modifierId"],
            ["modifierId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        )


def downgrade() -> None:
    # Remove the FK from modifier_roll -> modifier first.
    with op.batch_alter_table("modifier_roll") as batch_op:
        batch_op.drop_constraint(
            "fk_modifier_roll_modifier",
            type_="foreignkey",
        )

    with op.batch_alter_table("modifier") as batch_op:
        batch_op.drop_constraint("uq_effect")
        batch_op.add_column(sa.Column("position", sa.SmallInteger()))
        batch_op.add_column(sa.Column("minRoll", sa.Float(4)))
        batch_op.add_column(sa.Column("maxRoll", sa.Float(4)))
        batch_op.add_column(sa.Column("textRolls", sa.Text()))

        batch_op.create_primary_key(
            "modifier_pkey",
            ["modifierId", "position"],
        )

        # Restore the rows that were deleted during upgrade and populate
        # the position 0 rows with the data from modifier_roll.
        op.execute("""
            INSERT INTO modifier (
                "modifierId",
                position,
                "minRoll",
                "maxRoll",
                "textRolls"
            )
            SELECT
                mr."modifierId",
                mr.position,
                mr."minRoll",
                mr."maxRoll",
                array_to_string(mr."textRolls", '|')
            FROM modifier_roll mr
        """)

    # Restore the original FK from item_modifier -> modifier.
    with op.batch_alter_table("item_modifier") as batch_op:
        batch_op.drop_constraint(
            "fk_item_modifier_modifier_roll",
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            "fk_item_modifier_modifier",
            "modifier",
            ["modifierId"],
            ["modifierId"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )

    # modifier_roll is no longer needed.
    op.drop_table("modifier_roll")

    op.execute("CREATE SEQUENCE modifier_id_seq;")
    op.execute(
        """SELECT setval('modifier_id_seq', (SELECT MAX("modifierId") FROM modifier));"""
    )
    op.create_trigger(modifier_id_trigger)
