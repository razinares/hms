"""empty message

Revision ID: d10e4d0567fa
Revises: 
Create Date: 2022-10-22 09:42:27.611260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd10e4d0567fa'
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
    op.create_table('employee_data',
    sa.Column('eid', sa.Integer(), nullable=False),
    sa.Column('ename', sa.String(length=20), nullable=False),
    sa.Column('empid', sa.Integer(), nullable=True),
    sa.Column('edesignation', sa.String(length=20), nullable=True),
    sa.Column('ecnum', sa.Integer(), nullable=True),
    sa.Column('efname', sa.String(length=20), nullable=True),
    sa.Column('emname', sa.String(length=20), nullable=True),
    sa.Column('eenum', sa.String(length=20), nullable=True),
    sa.Column('enid', sa.Integer(), nullable=True),
    sa.Column('paddr', sa.String(), nullable=True),
    sa.Column('edob', sa.String(length=20), nullable=True),
    sa.Column('epaddress', sa.String(), nullable=True),
    sa.Column('eedu', sa.String(), nullable=True),
    sa.Column('ejobinfo', sa.String(), nullable=True),
    sa.Column('ephoto', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('eid')
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
    op.drop_table('employee_data')
    op.drop_table('diagnostics')
    # ### end Alembic commands ###
