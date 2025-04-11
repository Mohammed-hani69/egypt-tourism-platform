"""Initialize database

Revision ID: init_db
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create user table with all columns
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(64), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(128), nullable=False),
        sa.Column('is_guide', sa.Boolean(), default=False),
        sa.Column('is_student', sa.Boolean(), default=False),
        sa.Column('is_tourist', sa.Boolean(), default=False),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('country', sa.String(64)),
        sa.Column('governorate', sa.String(64)),
        sa.Column('city', sa.String(64)),
        sa.Column('profile_pic', sa.String(120)),
        sa.Column('education_level', sa.String(32)),
        sa.Column('university', sa.String(128)),
        sa.Column('languages', sa.String(200)),
        sa.Column('bio', sa.Text),
        sa.Column('date_joined', sa.DateTime),
        sa.Column('profile_completed', sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_email', 'user', ['email'], unique=True)
    op.create_index('idx_username', 'user', ['username'], unique=True)

def downgrade():
    op.drop_table('user')
