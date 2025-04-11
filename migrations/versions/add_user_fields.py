"""add user fields

Revision ID: add_user_fields
Revises: [previous_revision_id]
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add new columns to user table
    op.add_column('user', sa.Column('country', sa.String(64), nullable=True))
    op.add_column('user', sa.Column('governorate', sa.String(64), nullable=True))
    op.add_column('user', sa.Column('city', sa.String(64), nullable=True))
    op.add_column('user', sa.Column('education_level', sa.String(32), nullable=True))
    op.add_column('user', sa.Column('university', sa.String(128), nullable=True))

def downgrade():
    # Remove columns if needed to rollback
    op.drop_column('user', 'country')
    op.drop_column('user', 'governorate')
    op.drop_column('user', 'city')
    op.drop_column('user', 'education_level')
    op.drop_column('user', 'university')
