"""add contacts table

Revision ID: e8e95db6a8c8
Revises: a7eb018101b0
Create Date: 2022-11-25 08:03:47.183712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8e95db6a8c8'
down_revision = 'a7eb018101b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
   # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('clientes_excel', schema='partner')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clientes_excel',
    sa.Column('numero', sa.VARCHAR(length=400), autoincrement=False, nullable=False),
    sa.Column('nombre', sa.VARCHAR(length=400), autoincrement=False, nullable=False),
    sa.Column('reup', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('tipocliente', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=400), autoincrement=False, nullable=True),
    sa.Column('telefono', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('movil', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('user_add', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('date_add', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('numero', name='clienteexcel_pkey'),
    schema='partner'
    )
    # ### end Alembic commands ###
