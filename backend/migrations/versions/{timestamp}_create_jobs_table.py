from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=5000), nullable=False),
        sa.Column('requirements', sa.String(length=5000), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('salary_range', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.Enum('draft', 'open', 'closed', name='jobstatus'), 
                 nullable=False, server_default='draft'),
        sa.Column('hiring_manager_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                 server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), 
                 server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['hiring_manager_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_hiring_manager_id'), 'jobs', ['hiring_manager_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_jobs_hiring_manager_id'), table_name='jobs')
    op.drop_table('jobs')
    op.execute('DROP TYPE jobstatus')
