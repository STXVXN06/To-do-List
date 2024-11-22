# pylint: disable=import-error, no-member, function-redefined
"""first_migrations

Revision ID: 905731c6a76a
Revises: 
Create Date: 2024-11-06 18:26:01.991411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '905731c6a76a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Handles the database schema upgrade to the new version."""
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50),
               nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.CheckConstraint("name IN ('TO_DO', 'IN_PROGRESS', 'COMPLETED')", name='check_status_name'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_status_id'), 'status', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_of_creation', sa.Date(), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.CheckConstraint('expiration_date IS NULL OR expiration_date >= date_of_creation',
    name='check_expiration_date'),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_id'), 'task', ['id'], unique=False)
    op.create_table('change',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Date(), nullable=False),
    sa.Column('field_changed', sa.String(length=100), nullable=False),
    sa.Column('old_value', sa.Text(), nullable=True),
    sa.Column('new_value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_change_id'), 'change', ['id'], unique=False)
    # ### end Alembic commands ###
    op.execute("""
    INSERT INTO status (name) 
    VALUES ('TO_DO'), ('IN_PROGRESS'), ('COMPLETED');
    """)
    # Insertar los roles por defecto
    op.execute("""
    INSERT INTO role (name) 
    VALUES ('Administrator'), ('User');
    """)


def downgrade() -> None:
    """Reverts the database schema to the previous version."""
    op.execute("""
    DELETE FROM status WHERE name IN ('TO_DO', 'IN_PROGRESS', 'COMPLETED');
    """)

    op.execute("""
    DELETE FROM role WHERE name IN ('Administrator', 'User');
    """)



def downgrade() -> None:
    """Reverts the database schema to the previous version."""
    op.drop_index(op.f('ix_change_id'), table_name='change')
    op.drop_table('change')
    op.drop_index(op.f('ix_task_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_status_id'), table_name='status')
    op.drop_table('status')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###
