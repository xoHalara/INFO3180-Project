"""Add photo column to profiles

Revision ID: 99e69821dc0d
Revises: 24ccac1313e0
Create Date: 2025-05-03 16:30:48.417787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99e69821dc0d'
down_revision = '24ccac1313e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id_fk', sa.Integer(), nullable=False),
    sa.Column('fav_user_id_fk', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fav_user_id_fk'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id_fk'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='unique_favorite')
    )
    op.drop_table('favourites')
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_column('photo')

    op.create_table('favourites',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id_fk', sa.INTEGER(), nullable=False),
    sa.Column('fav_user_id_fk', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['fav_user_id_fk'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id_fk'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='unique_favorite')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###
