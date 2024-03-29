"""empty message

Revision ID: f0317f594eb7
Revises: 
Create Date: 2023-02-13 00:20:31.948373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0317f594eb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gpa', sa.Float(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('ranked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('faculty', sa.Boolean(), nullable=True),
    sa.Column('student', sa.Boolean(), nullable=True),
    sa.Column('leader', sa.Boolean(), nullable=True),
    sa.Column('sId', sa.Integer(), nullable=True),
    sa.Column('gpa', sa.Float(), nullable=True),
    sa.Column('member', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('proposal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('desc', sa.String(length=2064), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('owned', sa.Boolean(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('holder', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.ForeignKeyConstraint(['holder'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('proposal', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_proposal_desc'), ['desc'], unique=False)
        batch_op.create_index(batch_op.f('ix_proposal_title'), ['title'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proposal', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_proposal_title'))
        batch_op.drop_index(batch_op.f('ix_proposal_desc'))

    op.drop_table('proposal')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('group')
    # ### end Alembic commands ###
