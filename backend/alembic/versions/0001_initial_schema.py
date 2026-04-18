"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-18
"""

from alembic import op
import sqlalchemy as sa


revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('companies', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(150), nullable=False, unique=True))

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(150), nullable=False),
        sa.Column('email', sa.String(200), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'owner', 'accountant', 'manager', 'chef', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'restaurants',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=False),
    )

    op.create_table(
        'restaurant_users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.UniqueConstraint('user_id', 'restaurant_id', name='uq_restaurant_users'),
    )

    op.create_table(
        'periods',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', sa.Enum('in_progress', 'review', 'issues', 'closed', name='periodstatus'), nullable=False),
    )

    op.create_table(
        'blocks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('period_id', sa.Integer(), sa.ForeignKey('periods.id'), nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('code', sa.String(60), nullable=False),
        sa.Column('status', sa.String(40), nullable=False),
        sa.UniqueConstraint('period_id', 'code', name='uq_period_block_code'),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('block_id', sa.Integer(), sa.ForeignKey('blocks.id'), nullable=False),
        sa.Column('title', sa.String(220), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('open', 'in_progress', 'done', 'canceled', name='taskstatus'), nullable=False),
        sa.Column('assigned_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('deadline', sa.Date()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime()),
    )

    op.create_table(
        'issues',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('period_id', sa.Integer(), sa.ForeignKey('periods.id'), nullable=False),
        sa.Column('block_id', sa.Integer(), sa.ForeignKey('blocks.id'), nullable=False),
        sa.Column('type', sa.Enum('food_cost', 'purchases', 'inventory', 'write_offs', 'fot', 'revenue', 'avg_check', 'supplier_price', 'custom', name='issuetype'), nullable=False),
        sa.Column('title', sa.String(220), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('severity', sa.Enum('green', 'yellow', 'red', name='severity'), nullable=False),
        sa.Column('status', sa.Enum('open', 'in_progress', 'resolved', name='issuestatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'issue_analyses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('issue_id', sa.Integer(), sa.ForeignKey('issues.id'), nullable=False, unique=True),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('solution', sa.Text(), nullable=False),
        sa.Column('result', sa.Text(), nullable=False),
        sa.Column('assigned_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('deadline', sa.Date()),
        sa.Column('resolved_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('issue_id', sa.Integer(), sa.ForeignKey('issues.id')),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table('products', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(180), nullable=False), sa.Column('category', sa.String(100), nullable=False), sa.Column('unit', sa.String(20), nullable=False))
    op.create_table('suppliers', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(180), nullable=False, unique=True))

    op.create_table(
        'product_prices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id'), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False),
        sa.Column('price', sa.Numeric(12, 2), nullable=False),
        sa.Column('price_date', sa.Date(), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    )

    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('period_id', sa.Integer(), sa.ForeignKey('periods.id'), nullable=False, unique=True),
        sa.Column('revenue', sa.Numeric(14, 2), nullable=False),
        sa.Column('avg_check', sa.Numeric(12, 2), nullable=False),
        sa.Column('guest_count', sa.Integer(), nullable=False),
        sa.Column('food_cost_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('food_cost_percent', sa.Float(), nullable=False),
        sa.Column('fot_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('fot_percent', sa.Float(), nullable=False),
        sa.Column('write_offs_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('inventory_diff_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('negative_stock_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('comments', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('metrics')
    op.drop_table('product_prices')
    op.drop_table('suppliers')
    op.drop_table('products')
    op.drop_table('comments')
    op.drop_table('issue_analyses')
    op.drop_table('issues')
    op.drop_table('tasks')
    op.drop_table('blocks')
    op.drop_table('periods')
    op.drop_table('restaurant_users')
    op.drop_table('restaurants')
    op.drop_table('users')
    op.drop_table('companies')
    sa.Enum(name='issuestatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='severity').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='issuetype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='taskstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='periodstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
