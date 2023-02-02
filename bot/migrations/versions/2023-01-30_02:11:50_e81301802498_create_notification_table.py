"""
create_notification_table

Revision ID:e81301802498
Revises:275f4df1dc0b
Create Date:2023-01-30 02:11:50.759482
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e81301802498'
down_revision = '275f4df1dc0b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('currency_char_code', sa.String(), nullable=False),
        sa.Column('value', sa.Numeric(precision=9, scale=4), nullable=False),
        sa.Column('comparison_sign', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=True)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
