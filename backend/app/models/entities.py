from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    format: Mapped[str] = mapped_column(String(100), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    avg_check: Mapped[float] = mapped_column(Float, nullable=False)
    food_cost_percent: Mapped[float] = mapped_column(Float, nullable=False)
    labor_cost_percent: Mapped[float] = mapped_column(Float, nullable=False)
    write_offs: Mapped[float] = mapped_column(Float, nullable=False)
    net_profit: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)

    supplier_prices: Mapped[list["SupplierPrice"]] = relationship(back_populates="restaurant")
    inventory_losses: Mapped[list["InventoryLoss"]] = relationship(back_populates="restaurant")
    prep_production: Mapped[list["PrepProduction"]] = relationship(back_populates="restaurant")
    kitchen_performance: Mapped[list["KitchenPerformance"]] = relationship(back_populates="restaurant")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    supplier_prices: Mapped[list["SupplierPrice"]] = relationship(back_populates="supplier")


class SupplierPrice(Base):
    __tablename__ = "supplier_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(String(120), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    previous_price: Mapped[float] = mapped_column(Float, nullable=False)
    price_change_percent: Mapped[float] = mapped_column(Float, nullable=False)
    market_avg_price: Mapped[float] = mapped_column(Float, nullable=False)
    is_above_market: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    supplier: Mapped[Supplier] = relationship(back_populates="supplier_prices")
    restaurant: Mapped[Restaurant] = relationship(back_populates="supplier_prices")


class InventoryLoss(Base):
    __tablename__ = "inventory_losses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)

    restaurant: Mapped[Restaurant] = relationship(back_populates="inventory_losses")


class PrepProduction(Base):
    __tablename__ = "prep_production"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(120), nullable=False)
    shelf_life_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    current_stock: Mapped[float] = mapped_column(Float, nullable=False)
    avg_sales_per_lifetime: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_prep: Mapped[float] = mapped_column(Float, nullable=False)
    overproduction_risk: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    restaurant: Mapped[Restaurant] = relationship(back_populates="prep_production")


class KitchenPerformance(Base):
    __tablename__ = "kitchen_performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    station_name: Mapped[str] = mapped_column(String(120), nullable=False)
    avg_cook_time: Mapped[float] = mapped_column(Float, nullable=False)
    orders_count: Mapped[int] = mapped_column(Integer, nullable=False)
    errors_count: Mapped[int] = mapped_column(Integer, nullable=False)
    load_percent: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    restaurant: Mapped[Restaurant] = relationship(back_populates="kitchen_performance")
