"""Changed name of range to roll

Revision ID: 98edf7a48921
Revises: c1ff3b212b43
Create Date: 2024-03-25 11:37:33.348606

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98edf7a48921"
down_revision: Union[str, None] = "c1ff3b212b43"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("item_modifier", "range", new_column_name="roll")


def downgrade() -> None:
    op.alter_column("item_modifier", "roll", new_column_name="range")
