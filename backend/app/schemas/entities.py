from datetime import date
from pydantic import BaseModel


class RestaurantOut(BaseModel):
    id: int
    name: str
    city: str
    format: str
    seats: int
    monthly_revenue: float
    avg_check: float
    food_cost_percent: float
    labor_cost_percent: float
    write_offs: float
    net_profit: float
    status: str

    class Config:
        from_attributes = True


class SupplierOut(BaseModel):
    id: int
    name: str
    category: str
    contact_name: str
    phone: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class SupplierPriceOut(BaseModel):
    id: int
    supplier_id: int
    restaurant_id: int
    product_name: str
    unit: str
    price: float
    previous_price: float
    price_change_percent: float
    market_avg_price: float
    is_above_market: bool
    date: date

    class Config:
        from_attributes = True


class InventoryLossOut(BaseModel):
    id: int
    restaurant_id: int
    category: str
    amount: float
    date: date
    comment: str

    class Config:
        from_attributes = True


class PrepProductionOut(BaseModel):
    id: int
    restaurant_id: int
    item_name: str
    shelf_life_hours: int
    current_stock: float
    avg_sales_per_lifetime: float
    recommended_prep: float
    overproduction_risk: float
    date: date

    class Config:
        from_attributes = True


class KitchenPerformanceOut(BaseModel):
    id: int
    restaurant_id: int
    station_name: str
    avg_cook_time: float
    orders_count: int
    errors_count: int
    load_percent: float
    date: date

    class Config:
        from_attributes = True
