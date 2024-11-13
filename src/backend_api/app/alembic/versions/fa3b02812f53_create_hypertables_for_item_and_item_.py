"""Create hypertables for item and item_modifier

Revision ID: fa3b02812f53
Revises: 35736bccbe58
Create Date: 2024-11-13 11:50:03.745989

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fa3b02812f53"
down_revision: Union[str, None] = "35736bccbe58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    #    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""ALTER TABLE item_modifier ALTER COLUMN "itemId" DROP DEFAULT""")
    op.execute("""ALTER TABLE item DROP CONSTRAINT item_pkey""")
    op.execute("""ALTER TABLE item_modifier DROP CONSTRAINT item_modifier_pkey""")

    op.execute(
        "SELECT create_hypertable('item_modifier', by_range('createdHoursSinceLaunch'), migrate_data => TRUE);"  # 7 days interval
    )
    op.execute(
        "SELECT create_hypertable('item', 'createdHoursSinceLaunch', migrate_data => TRUE);"  # 7 days interval
    )
    op.execute(
        "SELECT add_dimension('item_modifier', by_hash('modifierId', 20));"
    )  # ~480 different modifierIds, so ~24 in each partition
    op.execute(
        "SELECT add_dimension('item', by_hash('name', 15));"
    )  # Currently have 31 different names, so get ~2 in each partition

    # I haven't gotten compress to work very well with our db. Here is a layout on how compress
    # may look like:


# op.execute(
#     """ALTER TABLE "item" SET (
#      timescaledb.compress,
#      timescaledb.compress_orderby = '"createdAt"',
#      timescaledb.compress_segmentby = '"name"'
#  );"""
# )
# op.execute(
#     "SELECT add_compression_policy('item', compress_after => INTERVAL '7 days');"
# )  # interval number is not optimized


#    # ### end Alembic commands ###
#
#
def downgrade() -> None:
    pass


#    # ### commands auto generated by Alembic - please adjust! ###
#
#    # Converts hypertable to normal table
#    op.execute(
#        """
#            CREATE TABLE item_modifier_normal (LIKE item_modifier INCLUDING ALL);
#            INSERT INTO item_modifier_normal (SELECT * FROM item_modifier);
#            DROP TABLE item_modifier;
#            ALTER TABLE item_modifier_normal RENAME TO item_modifier;
#        """
#    )
#
#    # ### end Alembic commands ###
