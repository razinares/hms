"""Initial Migration

Revision ID: d4ec6981315c
Revises: 
Create Date: 2022-10-18 03:40:38.781522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4ec6981315c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diagnostics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('tname', sa.String(length=20), nullable=True),
    sa.Column('tid', sa.Integer(), nullable=True),
    sa.Column('tcharge', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('mname', sa.String(length=20), nullable=True),
    sa.Column('mid', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.Column('qissued', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ssn_id', sa.Integer(), nullable=True),
    sa.Column('pname', sa.String(length=20), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('ldate', sa.DateTime(), nullable=True),
    sa.Column('tbed', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=20), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userstore',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uname', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnosticsmaster',
    sa.Column('tid', sa.Integer(), nullable=False),
    sa.Column('tname', sa.String(length=20), nullable=True),
    sa.Column('tcharge', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tid'], ['diagnostics.tid'], ),
    sa.PrimaryKeyConstraint('tid')
    )
    op.create_table('medicinemaster',
    sa.Column('mid', sa.Integer(), nullable=False),
    sa.Column('mname', sa.String(length=20), nullable=True),
    sa.Column('qavailable', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mid'], ['medicines.mid'], ),
    sa.PrimaryKeyConstraint('mid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medicinemaster')
    op.drop_table('diagnosticsmaster')
    op.drop_table('userstore')
    op.drop_table('patients')
    op.drop_table('medicines')
    op.drop_table('diagnostics')
    # ### end Alembic commands ###
