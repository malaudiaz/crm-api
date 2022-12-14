"""add contracts table

Revision ID: 296bdc06e03a
Revises: e21bd7b93238
Create Date: 2022-11-26 23:56:03.855998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '296bdc06e03a'
down_revision = 'e21bd7b93238'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contracts',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('number', sa.String(length=100), nullable=False),
    sa.Column('id_partner', sa.String(), nullable=False),
    sa.Column('id_contact', sa.String(), nullable=False),
    sa.Column('sign_by', sa.String(length=400), nullable=True),
    sa.Column('sign_date', sa.Date(), nullable=True),
    sa.Column('initial_aproved_import', sa.Float(), nullable=True),
    sa.Column('real_aproved_import', sa.Float(), nullable=True),
    sa.Column('real_import', sa.Float(), nullable=True),
    sa.Column('is_supplement', sa.Boolean(), nullable=False),
    sa.Column('contract_id', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(length=50), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.contracts.id'], ),
    sa.ForeignKeyConstraint(['id_contact'], ['partner.contacts.id'], ),
    sa.ForeignKeyConstraint(['id_partner'], ['partner.partners.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='contract'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contracts', schema='contract')
    # ### end Alembic commands ###
