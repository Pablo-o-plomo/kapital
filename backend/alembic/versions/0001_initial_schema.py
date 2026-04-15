"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("format", sa.String(length=100), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False),
        sa.Column("monthly_revenue", sa.Float(), nullable=False),
        sa.Column("avg_check", sa.Float(), nullable=False),
        sa.Column("food_cost_percent", sa.Float(), nullable=False),
        sa.Column("labor_cost_percent", sa.Float(), nullable=False),
        sa.Column("write_offs", sa.Float(), nullable=False),
        sa.Column("net_profit", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
    )

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=140), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("contact_name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "supplier_prices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("product_name", sa.String(length=120), nullable=False),
        sa.Column("unit", sa.String(length=20), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("previous_price", sa.Float(), nullable=False),
        sa.Column("price_change_percent", sa.Float(), nullable=False),
        sa.Column("market_avg_price", sa.Float(), nullable=False),
        sa.Column("is_above_market", sa.Boolean(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
    )

    op.create_table(
        "inventory_losses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("category", sa.String(length=60), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
    )

    op.create_table(
        "prep_production",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("item_name", sa.String(length=120), nullable=False),
        sa.Column("shelf_life_hours", sa.Integer(), nullable=False),
        sa.Column("current_stock", sa.Float(), nullable=False),
        sa.Column("avg_sales_per_lifetime", sa.Float(), nullable=False),
        sa.Column("recommended_prep", sa.Float(), nullable=False),
        sa.Column("overproduction_risk", sa.Float(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
    )

    op.create_table(
        "kitchen_performance",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("station_name", sa.String(length=120), nullable=False),
        sa.Column("avg_cook_time", sa.Float(), nullable=False),
        sa.Column("orders_count", sa.Integer(), nullable=False),
        sa.Column("errors_count", sa.Integer(), nullable=False),
        sa.Column("load_percent", sa.Float(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("kitchen_performance")
    op.drop_table("prep_production")
    op.drop_table("inventory_losses")
    op.drop_table("supplier_prices")
    op.drop_table("suppliers")
    op.drop_table("restaurants")
