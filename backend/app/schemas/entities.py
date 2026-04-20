from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.entities import IssueStatus, IssueType, PeriodStatus, Severity, TaskStatus, UserRole


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.manager


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class CompanyCreate(BaseModel):
    name: str


class RestaurantCreate(BaseModel):
    name: str
    company_id: int


class RestaurantOut(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True


class PeriodCreate(BaseModel):
    restaurant_id: int
    start_date: date
    end_date: date


class PeriodUpdate(BaseModel):
    status: PeriodStatus


class PeriodOut(BaseModel):
    id: int
    restaurant_id: int
    start_date: date
    end_date: date
    status: PeriodStatus

    class Config:
        from_attributes = True


class BlockOut(BaseModel):
    id: int
    period_id: int
    name: str
    code: str
    status: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    block_id: int
    title: str
    description: str = ''
    assigned_user_id: Optional[int] = None
    deadline: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_user_id: Optional[int] = None
    deadline: Optional[date] = None


class TaskOut(BaseModel):
    id: int
    block_id: int
    title: str
    description: str
    status: TaskStatus
    assigned_user_id: Optional[int]
    deadline: Optional[date]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class IssueCreate(BaseModel):
    period_id: int
    block_id: int
    type: IssueType
    title: str
    description: str = ''
    severity: Severity = Severity.yellow


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[IssueStatus] = None


class IssueOut(BaseModel):
    id: int
    period_id: int
    block_id: int
    type: IssueType
    title: str
    description: str
    severity: Severity
    status: IssueStatus
    created_at: datetime

    class Config:
        from_attributes = True


class IssueAnalysisIn(BaseModel):
    reason: str = ''
    solution: str = ''
    result: str = ''
    assigned_user_id: Optional[int] = None
    deadline: Optional[date] = None


class IssueAnalysisOut(BaseModel):
    id: int
    issue_id: int
    reason: str
    solution: str
    result: str
    assigned_user_id: Optional[int]
    deadline: Optional[date]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    issue_id: Optional[int] = None
    task_id: Optional[int] = None
    text: str = Field(min_length=1)


class CommentOut(BaseModel):
    id: int
    issue_id: Optional[int]
    task_id: Optional[int]
    user_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class MetricCreate(BaseModel):
    period_id: int
    revenue: float = 0
    avg_check: float = 0
    guest_count: int = 0
    food_cost_value: float = 0
    food_cost_percent: float = 0
    fot_value: float = 0
    fot_percent: float = 0
    write_offs_value: float = 0
    inventory_diff_value: float = 0
    negative_stock_value: float = 0
    comments: str = ''


class MetricUpdate(BaseModel):
    revenue: Optional[float] = None
    avg_check: Optional[float] = None
    guest_count: Optional[int] = None
    food_cost_value: Optional[float] = None
    food_cost_percent: Optional[float] = None
    fot_value: Optional[float] = None
    fot_percent: Optional[float] = None
    write_offs_value: Optional[float] = None
    inventory_diff_value: Optional[float] = None
    negative_stock_value: Optional[float] = None
    comments: Optional[str] = None


class MetricOut(BaseModel):
    id: int
    period_id: int
    revenue: float
    avg_check: float
    guest_count: int
    food_cost_value: float
    food_cost_percent: float
    fot_value: float
    fot_percent: float
    write_offs_value: float
    inventory_diff_value: float
    negative_stock_value: float
    comments: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    category: str
    unit: str


class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    unit: str

    class Config:
        from_attributes = True


class SupplierCreate(BaseModel):
    name: str


class SupplierOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductPriceCreate(BaseModel):
    product_id: int
    supplier_id: int
    restaurant_id: int
    price: float
    price_date: date


class ProductPriceOut(BaseModel):
    id: int
    product_id: int
    supplier_id: int
    restaurant_id: int
    price: float
    price_date: date
    created_by_user_id: int

    class Config:
        from_attributes = True
