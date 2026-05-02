from __future__ import annotations
import enum
from datetime import date, datetime
from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ReportType(str, enum.Enum):
    sales = 'SALES'
    purchases = 'PURCHASES'
    osv = 'OSV'
    movement = 'MOVEMENT'

class ImportStatus(str, enum.Enum):
    pending='pending'; parsed='parsed'; failed='failed'; unknown='unknown'
class AlertSeverity(str, enum.Enum):
    green='green'; yellow='yellow'; red='red'

class IikoRestaurant(Base):
    __tablename__='iiko_restaurants'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String(200), nullable=False)
    code: Mapped[str]=mapped_column(String(120), unique=True, index=True)
    city: Mapped[str|None]=mapped_column(String(120))
    email_alias: Mapped[str|None]=mapped_column(String(255))
    subject_code: Mapped[str|None]=mapped_column(String(120))
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class RestaurantBot(Base):
    __tablename__='restaurant_bots'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id'), index=True)
    bot_token: Mapped[str]=mapped_column(String(255))
    telegram_chat_id: Mapped[str]=mapped_column(String(120))
    bot_username: Mapped[str|None]=mapped_column(String(120))
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class ReportImport(Base):
    __tablename__='report_imports'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int|None]=mapped_column(ForeignKey('iiko_restaurants.id'), index=True)
    report_type: Mapped[ReportType|None]=mapped_column(Enum(ReportType))
    report_date: Mapped[date|None]=mapped_column(Date)
    source: Mapped[str]=mapped_column(String(30), default='email')
    email_subject: Mapped[str|None]=mapped_column(String(500))
    email_from: Mapped[str|None]=mapped_column(String(255))
    email_message_id: Mapped[str|None]=mapped_column(String(255), index=True)
    original_filename: Mapped[str|None]=mapped_column(String(255))
    stored_file_path: Mapped[str|None]=mapped_column(String(500))
    status: Mapped[ImportStatus]=mapped_column(Enum(ImportStatus), default=ImportStatus.pending)
    error_message: Mapped[str|None]=mapped_column(Text)
    raw_metadata: Mapped[dict]=mapped_column(JSON, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime|None]=mapped_column(DateTime)

class SalesDaily(Base):
    __tablename__='sales_daily'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id')); business_date: Mapped[date]=mapped_column(Date)
    revenue_total: Mapped[float]=mapped_column(Numeric(14,2), default=0); orders_count: Mapped[int|None]=mapped_column(Integer); guests_count: Mapped[int|None]=mapped_column(Integer); average_check: Mapped[float|None]=mapped_column(Numeric(12,2))
    cash_revenue: Mapped[float|None]=mapped_column(Numeric(12,2)); card_revenue: Mapped[float|None]=mapped_column(Numeric(12,2)); delivery_revenue: Mapped[float|None]=mapped_column(Numeric(12,2)); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class PurchaseItem(Base):
    __tablename__='purchase_items'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id')); business_date: Mapped[date]=mapped_column(Date)
    supplier_name: Mapped[str|None]=mapped_column(String(200)); invoice_number: Mapped[str|None]=mapped_column(String(100)); product_name: Mapped[str]=mapped_column(String(250)); product_code: Mapped[str|None]=mapped_column(String(120)); category: Mapped[str|None]=mapped_column(String(120)); quantity: Mapped[float|None]=mapped_column(Numeric(12,3)); unit: Mapped[str|None]=mapped_column(String(50)); price: Mapped[float|None]=mapped_column(Numeric(12,2)); amount: Mapped[float|None]=mapped_column(Numeric(12,2)); vat: Mapped[float|None]=mapped_column(Numeric(12,2)); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class MovementItem(Base):
    __tablename__='movement_items'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id')); business_date: Mapped[date]=mapped_column(Date)
    warehouse: Mapped[str|None]=mapped_column(String(120)); product_name: Mapped[str]=mapped_column(String(250)); category: Mapped[str|None]=mapped_column(String(120)); operation_type: Mapped[str|None]=mapped_column(String(120)); document_type: Mapped[str|None]=mapped_column(String(120)); quantity: Mapped[float|None]=mapped_column(Numeric(12,3)); unit: Mapped[str|None]=mapped_column(String(50)); amount: Mapped[float|None]=mapped_column(Numeric(12,2)); is_writeoff: Mapped[bool]=mapped_column(Boolean, default=False); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class OsvItem(Base):
    __tablename__='osv_items'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id')); business_date: Mapped[date]=mapped_column(Date)
    warehouse: Mapped[str|None]=mapped_column(String(120)); product_name: Mapped[str]=mapped_column(String(250)); product_code: Mapped[str|None]=mapped_column(String(120)); category: Mapped[str|None]=mapped_column(String(120)); quantity: Mapped[float|None]=mapped_column(Numeric(12,3)); unit: Mapped[str|None]=mapped_column(String(50)); amount: Mapped[float|None]=mapped_column(Numeric(12,2)); is_negative: Mapped[bool]=mapped_column(Boolean, default=False); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__='alerts'
    id: Mapped[int]=mapped_column(Integer, primary_key=True); restaurant_id: Mapped[int|None]=mapped_column(ForeignKey('iiko_restaurants.id')); severity: Mapped[AlertSeverity]=mapped_column(Enum(AlertSeverity)); alert_type: Mapped[str]=mapped_column(String(80)); title: Mapped[str]=mapped_column(String(200)); message: Mapped[str]=mapped_column(Text); data: Mapped[dict]=mapped_column(JSON, default=dict); is_sent: Mapped[bool]=mapped_column(Boolean, default=False); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow); sent_at: Mapped[datetime|None]=mapped_column(DateTime)

class DashboardSnapshot(Base):
    __tablename__='dashboard_snapshots'
    __table_args__ = (UniqueConstraint('restaurant_id', 'business_date', name='uq_dashboard_rest_date'),)
    id: Mapped[int]=mapped_column(Integer, primary_key=True); restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); business_date: Mapped[date]=mapped_column(Date, index=True)
    revenue_total: Mapped[float]=mapped_column(Numeric(14,2), default=0); purchases_total: Mapped[float]=mapped_column(Numeric(14,2), default=0); writeoffs_total: Mapped[float]=mapped_column(Numeric(14,2), default=0); writeoffs_percent: Mapped[float]=mapped_column(Numeric(8,2), default=0); negative_stock_count: Mapped[int]=mapped_column(Integer, default=0); purchase_price_risks_count: Mapped[int]=mapped_column(Integer, default=0); status: Mapped[AlertSeverity]=mapped_column(Enum(AlertSeverity), default=AlertSeverity.green); data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)


class ReportTypeRef(Base):
    __tablename__='report_types'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    report_code: Mapped[str]=mapped_column(String(10), unique=True)
    report_name_ru: Mapped[str]=mapped_column(String(200))
    iiko_report_name: Mapped[str|None]=mapped_column(String(255))
    frequency: Mapped[str|None]=mapped_column(String(50))
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)

class PurchasePriceEvent(Base):
    __tablename__='purchase_price_events'
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int]=mapped_column(ForeignKey('iiko_restaurants.id')); report_import_id: Mapped[int]=mapped_column(ForeignKey('report_imports.id'))
    product_name: Mapped[str|None]=mapped_column(String(250)); product_code: Mapped[str|None]=mapped_column(String(120)); arrival_datetime: Mapped[datetime|None]=mapped_column(DateTime)
    supplier_name: Mapped[str|None]=mapped_column(String(250)); invoice_number: Mapped[str|None]=mapped_column(String(120)); supplier_product_name: Mapped[str|None]=mapped_column(String(250)); unit: Mapped[str|None]=mapped_column(String(50))
    price_with_vat: Mapped[float|None]=mapped_column(Numeric(12,2)); unit_price_with_vat: Mapped[float|None]=mapped_column(Numeric(12,2)); pricelist_price: Mapped[float|None]=mapped_column(Numeric(12,2)); price_deviation_rub: Mapped[float|None]=mapped_column(Numeric(12,2)); price_deviation_percent: Mapped[float|None]=mapped_column(Numeric(8,2)); raw_data: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
