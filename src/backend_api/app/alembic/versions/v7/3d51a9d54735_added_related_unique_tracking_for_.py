"""Added related unique tracking for modifiers and item base types

Revision ID: 3d51a9d54735
Revises: 6d9ebe48cb1e
Create Date: 2024-09-04 14:02:23.900216

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3d51a9d54735"
down_revision: Union[str, None] = "874158ad90c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("modifier", sa.Column("relatedUniques", sa.String()))
    op.add_column("item_base_type", sa.Column("relatedUniques", sa.String()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("modifier", "relatedUniques")
    op.drop_column("item_base_type", "relatedUniques")
    # ### end Alembic commands ###
