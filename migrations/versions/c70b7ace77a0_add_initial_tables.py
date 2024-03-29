"""add initial tables

Revision ID: c70b7ace77a0
Revises: 5868b9203be2
Create Date: 2023-01-10 17:45:51.731419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c70b7ace77a0'
down_revision = '5868b9203be2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'job',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               schema='enterprise')
    op.alter_column('users', 'selected',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               schema='enterprise')
    op.alter_column('partners', 'selected',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               schema='partner')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('partners', 'selected',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               schema='partner')
    op.alter_column('users', 'selected',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               schema='enterprise')
    op.alter_column('users', 'job',
               existing_type=sa.VARCHAR(length=50),
               nullable=True,
               schema='enterprise')
    # ### end Alembic commands ###
