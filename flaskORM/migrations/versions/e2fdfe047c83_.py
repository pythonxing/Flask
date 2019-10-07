"""empty message

Revision ID: e2fdfe047c83
Revises: 
Create Date: 2019-10-07 23:07:38.042830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2fdfe047c83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('curriculum',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('c_id', sa.String(length=32), nullable=True),
    sa.Column('c_name', sa.String(length=32), nullable=True),
    sa.Column('c_time', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('picture',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=32), nullable=True),
    sa.Column('picture', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacationTip',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vacation_id', sa.Integer(), nullable=True),
    sa.Column('vacation_name', sa.String(length=32), nullable=True),
    sa.Column('vacation_type', sa.String(length=32), nullable=True),
    sa.Column('vacation_start', sa.String(length=32), nullable=True),
    sa.Column('vacation_deadline', sa.String(length=32), nullable=True),
    sa.Column('vacation_description', sa.Text(), nullable=True),
    sa.Column('vacation_phone', sa.String(length=32), nullable=True),
    sa.Column('vacation_status', sa.Integer(), nullable=True),
    sa.Column('vacation_day', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacationTip')
    op.drop_table('user')
    op.drop_table('picture')
    op.drop_table('curriculum')
    # ### end Alembic commands ###
