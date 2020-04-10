"""added fund owner relationship

Revision ID: fd83433ae308
Revises: 1310a3935ffe
Create Date: 2020-04-08 22:34:46.223162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd83433ae308'
down_revision = '1310a3935ffe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('funds', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_funds_owner_id_users'), 'users', ['owner_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('funds', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_funds_owner_id_users'), type_='foreignkey')
        batch_op.drop_column('owner_id')

    # ### end Alembic commands ###