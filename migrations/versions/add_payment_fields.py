"""add payment fields

Revision ID: add_payment_fields
Create Date: 2024-04-16 17:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_payment_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('tour_booking') as batch_op:
        batch_op.add_column(sa.Column('payment_status', sa.String(20), nullable=False, server_default='pending'))
        batch_op.add_column(sa.Column('total_cost', sa.Float(), nullable=True))

def downgrade():
    with op.batch_alter_table('tour_booking') as batch_op:
        batch_op.drop_column('payment_status')
        batch_op.drop_column('total_cost')
