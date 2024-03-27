"""Merged 13d and 98

Revision ID: 042066a4f2b8
Revises: 13da6f882eff, 98edf7a48921
Create Date: 2024-03-25 18:35:45.933740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '042066a4f2b8'
down_revision: Union[str, None] = ('13da6f882eff', '98edf7a48921')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
