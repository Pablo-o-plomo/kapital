from datetime import date
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import InventoryLoss, KitchenPerformance, PrepProduction, Restaurant, Supplier, SupplierPrice


RESTAURANTS = [
    {"name": "Москва / Авиапарк", "city": "Москва", "format": "Флагман Food Hall", "seats": 180, "monthly_revenue": 14200000, "avg_check": 1680, "food_cost_percent": 31.5, "labor_cost_percent": 27.8, "write_offs": 420000, "net_profit": 2960000, "status": "stable"},
    {"name": "Ростов-на-Дону", "city": "Ростов-на-Дону", "format": "Street Casual", "seats": 120, "monthly_revenue": 8600000, "avg_check": 1180, "food_cost_percent": 35.9, "labor_cost_percent": 29.5, "write_offs": 510000, "net_profit": 980000, "status": "attention"},
    {"name": "Южно-Сахалинск", "city": "Южно-Сахалинск", "format": "Premium Seafood", "seats": 90, "monthly_revenue": 12300000, "avg_check": 2140, "food_cost_percent": 38.4, "labor_cost_percent": 30.6, "write_offs": 760000, "net_profit": 1040000, "status": "critical"},
    {"name": "Сочи", "city": "Сочи", "format": "Resort Family", "seats": 150, "monthly_revenue": 9700000, "avg_check": 1430, "food_cost_percent": 33.2, "labor_cost_percent": 28.6, "write_offs": 390000, "net_profit": 1670000, "status": "stable"},
    {"name": "Санкт-Петербург", "city": "Санкт-Петербург", "format": "Urban Bistro", "seats": 130, "monthly_revenue": 11100000, "avg_check": 1520, "food_cost_percent": 34.7, "labor_cost_percent": 31.2, "write_offs": 640000, "net_profit": 1210000, "status": "attention"},
]


SUPPLIERS = [
    {"name": "FreshNorth", "category": "Овощи и зелень", "contact_name": "Ирина Павлова", "phone": "+7 900 100 11 22", "email": "irina@freshnorth.ru", "is_active": True},
    {"name": "ProteinHub", "category": "Мясо и птица", "contact_name": "Антон Лебедев", "phone": "+7 900 200 22 33", "email": "anton@proteinhub.ru", "is_active": True},
    {"name": "OceanLine", "category": "Рыба и морепродукты", "contact_name": "Марина Седова", "phone": "+7 900 300 33 44", "email": "marina@oceanline.ru", "is_active": True},
    {"name": "DairyPro", "category": "Молочная продукция", "contact_name": "Сергей Никитин", "phone": "+7 900 400 44 55", "email": "sergey@dairypro.ru", "is_active": True},
    {"name": "BakeryOne", "category": "Хлеб и выпечка", "contact_name": "Ольга Бондарь", "phone": "+7 900 500 55 66", "email": "olga@bakeryone.ru", "is_active": True},
]


def reset_and_seed_data(db: Session):
    for model in [SupplierPrice, InventoryLoss, PrepProduction, KitchenPerformance, Supplier, Restaurant]:
        db.query(model).delete()

    restaurants = [Restaurant(**item) for item in RESTAURANTS]
    suppliers = [Supplier(**item) for item in SUPPLIERS]
    db.add_all(restaurants + suppliers)
    db.flush()

    today = date.today()
    losses_categories = ["порча", "брак", "персонал", "комплименты", "инвентаризация минус", "инвентаризация плюс"]
    products = ["Лосось охлажденный", "Куриное филе", "Томаты", "Моцарелла", "Хлеб ремесленный"]
    stations = ["Гриль", "Холодный цех", "Пицца", "Горячий цех", "Экспедиция"]

    for r in restaurants:
        for idx, category in enumerate(losses_categories):
            amount = (idx + 1) * 15000 + (r.id * 7000)
            db.add(InventoryLoss(restaurant_id=r.id, category=category, amount=amount, date=today, comment=f"{category} — контрольная запись"))

        for i, item in enumerate(["Соус демиглас", "Бульон куриный", "Салат микс", "Тесто для пиццы", "Крем-суп основа"]):
            avg_sales = 80 + i * 12 + r.id * 3
            stock = avg_sales + (15 if r.status != "stable" else 4)
            risk = min(95, round((stock / max(avg_sales, 1)) * 55, 1))
            db.add(PrepProduction(restaurant_id=r.id, item_name=item, shelf_life_hours=24 + i * 8, current_stock=stock, avg_sales_per_lifetime=avg_sales, recommended_prep=round(avg_sales * 0.9, 1), overproduction_risk=risk, date=today))

        for i, station in enumerate(stations):
            base_time = 9 + i * 1.4 + (2.5 if r.status == "critical" else 0)
            load = 62 + i * 6 + (10 if r.status != "stable" else 0)
            errors = 2 + i + (3 if load > 85 else 0)
            db.add(KitchenPerformance(restaurant_id=r.id, station_name=station, avg_cook_time=round(base_time, 1), orders_count=220 + i * 40, errors_count=errors, load_percent=min(99, load), date=today))

    for s in suppliers:
        for idx, r in enumerate(restaurants):
            price = 100 + (s.id * 16) + (idx * 8)
            previous = round(price * 0.9, 2)
            change = round((price - previous) / previous * 100, 2)
            market = round(price * (0.92 if idx % 2 == 0 else 1.03), 2)
            db.add(SupplierPrice(supplier_id=s.id, restaurant_id=r.id, product_name=products[(s.id + idx) % len(products)], unit="кг", price=round(price, 2), previous_price=previous, price_change_percent=change, market_avg_price=market, is_above_market=price > market, date=today))

    db.commit()


def main():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        reset_and_seed_data(session)


if __name__ == "__main__":
    main()
