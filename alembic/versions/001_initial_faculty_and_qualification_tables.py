"""Initial migration: Create faculty_members and faculty_qualifications tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-08-08 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'faculty_members',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=False),
        sa.Column('designation', sa.String(length=100), nullable=False),
        sa.Column('years_of_experience', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('joining_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculty_members_department'), 'faculty_members', ['department'], unique=False)
    op.create_index(op.f('ix_faculty_members_designation'), 'faculty_members', ['designation'], unique=False)
    op.create_index(op.f('ix_faculty_members_email'), 'faculty_members', ['email'], unique=True)
    op.create_index(op.f('ix_faculty_members_id'), 'faculty_members', ['id'], unique=False)

    op.create_table(
        'faculty_qualifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('faculty_id', sa.Integer(), nullable=False),
        sa.Column('degree', sa.String(length=50), nullable=False),
        sa.Column('field_of_study', sa.String(length=100), nullable=True),
        sa.Column('institution', sa.String(length=150), nullable=True),
        sa.Column('passing_year', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['faculty_id'], ['faculty_members.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculty_qualifications_degree'), 'faculty_qualifications', ['degree'], unique=False)
    op.create_index(op.f('ix_faculty_qualifications_faculty_id'), 'faculty_qualifications', ['faculty_id'], unique=False)
    op.create_index(op.f('ix_faculty_qualifications_id'), 'faculty_qualifications', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_faculty_qualifications_id'), table_name='faculty_qualifications')
    op.drop_index(op.f('ix_faculty_qualifications_faculty_id'), table_name='faculty_qualifications')
    op.drop_index(op.f('ix_faculty_qualifications_degree'), table_name='faculty_qualifications')
    op.drop_table('faculty_qualifications')
    op.drop_index(op.f('ix_faculty_members_id'), table_name='faculty_members')
    op.drop_index(op.f('ix_faculty_members_email'), table_name='faculty_members')
    op.drop_index(op.f('ix_faculty_members_designation'), table_name='faculty_members')
    op.drop_index(op.f('ix_faculty_members_department'), table_name='faculty_members')
    op.drop_table('faculty_members')
