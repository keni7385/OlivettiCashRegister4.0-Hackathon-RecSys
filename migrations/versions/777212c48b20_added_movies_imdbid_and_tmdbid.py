"""Added Movies imdbId and tmdbId

Revision ID: 777212c48b20
Revises: 990567a763cc
Create Date: 2019-05-24 19:19:27.451987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '777212c48b20'
down_revision = '990567a763cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('imdb_id', sa.Integer(), nullable=True))
    op.add_column('movie', sa.Column('tmdb_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'tmdb_id')
    op.drop_column('movie', 'imdb_id')
    # ### end Alembic commands ###
