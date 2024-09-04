"""Added related unique tracking for modifiers

Revision ID: 3d51a9d54735
Revises: 59a1d9f18849
Create Date: 2024-09-04 14:02:23.900216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d51a9d54735'
down_revision: Union[str, None] = '59a1d9f18849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('modifier', sa.Column('relatedUnique', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('modifier', 'relatedUnique')
    # ### end Alembic commands ###
