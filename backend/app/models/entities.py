from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = 'admin'
    owner = 'owner'
    accountant = 'accountant'
    manager = 'manager'
    chef = 'chef'


class PeriodStatus(str, enum.Enum):
    in_progress = 'in_progress'
    review = 'review'
    issues = 'issues'
    closed = 'closed'


class TaskStatus(str, enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    done = 'done'
    canceled = 'canceled'


class Severity(str, enum.Enum):
    green = 'green'
    yellow = 'yellow'
    red = 'red'


class IssueStatus(str, enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    resolved = 'resolved'


class IssueType(str, enum.Enum):
    food_cost = 'food_cost'
    purchases = 'purchases'
    inventory = 'inventory'
    write_offs = 'write_offs'
    fot = 'fot'
    revenue = 'revenue'
    avg_check = 'avg_check'
    supplier_price = 'supplier_price'
    custom = 'custom'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False)


class RestaurantUser(Base):
    __tablename__ = 'restaurant_users'
    __table_args__ = (UniqueConstraint('user_id', 'restaurant_id', name='uq_restaurant_users'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'), nullable=False)


class Period(Base):
    __tablename__ = 'periods'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PeriodStatus] = mapped_column(Enum(PeriodStatus), default=PeriodStatus.in_progress, nullable=False)


class Block(Base):
    __tablename__ = 'blocks'
    __table_args__ = (UniqueConstraint('period_id', 'code', name='uq_period_block_code'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey('periods.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default='open')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.id'), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, default='')
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.open, nullable=False)
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    deadline: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)


class Issue(Base):
    __tablename__ = 'issues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey('periods.id'), nullable=False, index=True)
    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.id'), nullable=False)
    type: Mapped[IssueType] = mapped_column(Enum(IssueType), nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, default='')
    severity: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.yellow)
    status: Mapped[IssueStatus] = mapped_column(Enum(IssueStatus), default=IssueStatus.open)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class IssueAnalysis(Base):
    __tablename__ = 'issue_analyses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey('issues.id'), nullable=False, unique=True)
    reason: Mapped[str] = mapped_column(Text, default='')
    solution: Mapped[str] = mapped_column(Text, default='')
    result: Mapped[str] = mapped_column(Text, default='')
    assigned_user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    deadline: Mapped[date | None] = mapped_column(Date)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int | None] = mapped_column(ForeignKey('issues.id'))
    task_id: Mapped[int | None] = mapped_column(ForeignKey('tasks.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default='other')
    unit: Mapped[str] = mapped_column(String(20), default='kg')


class Supplier(Base):
    __tablename__ = 'suppliers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)


class ProductPrice(Base):
    __tablename__ = 'product_prices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Metric(Base):
    __tablename__ = 'metrics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey('periods.id'), unique=True, nullable=False, index=True)
    revenue: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    avg_check: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    guest_count: Mapped[int] = mapped_column(Integer, default=0)
    food_cost_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    food_cost_percent: Mapped[float] = mapped_column(Float, default=0)
    fot_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    fot_percent: Mapped[float] = mapped_column(Float, default=0)
    write_offs_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    inventory_diff_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    negative_stock_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    comments: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
