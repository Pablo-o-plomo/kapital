from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.entities import (
    InventoryLoss,
    KitchenPerformance,
    PrepProduction,
    Restaurant,
    Supplier,
    SupplierPrice,
)


def get_summary(db: Session):
    restaurants = db.query(Restaurant).all()
    total_revenue = sum(r.monthly_revenue for r in restaurants)
    total_write_offs = sum(r.write_offs for r in restaurants)
    total_net_profit = sum(r.net_profit for r in restaurants)
    count = len(restaurants) or 1
    problem_count = len([r for r in restaurants if r.status != "stable"])
    critical_alerts = len([r for r in restaurants if r.food_cost_percent > 36 or r.labor_cost_percent > 31])

    return {
        "total_revenue": round(total_revenue, 2),
        "avg_food_cost": round(sum(r.food_cost_percent for r in restaurants) / count, 2),
        "avg_labor_cost": round(sum(r.labor_cost_percent for r in restaurants) / count, 2),
        "total_write_offs": round(total_write_offs, 2),
        "total_net_profit": round(total_net_profit, 2),
        "restaurants_count": len(restaurants),
        "problem_restaurants_count": problem_count,
        "critical_alerts_count": critical_alerts,
    }


def get_losses(db: Session):
    losses = db.query(InventoryLoss).all()
    restaurants = {r.id: r.name for r in db.query(Restaurant).all()}
    by_cat, by_rest = defaultdict(float), defaultdict(float)

    for item in losses:
        by_cat[item.category] += item.amount
        by_rest[restaurants.get(item.restaurant_id, "Unknown")] += item.amount

    top = sorted(by_rest.items(), key=lambda x: x[1], reverse=True)[:3]
    return {
        "losses_by_category": [{"category": k, "amount": round(v, 2)} for k, v in by_cat.items()],
        "losses_by_restaurant": [{"restaurant": k, "amount": round(v, 2)} for k, v in by_rest.items()],
        "top_loss_restaurants": [{"restaurant": k, "amount": round(v, 2)} for k, v in top],
        "total_losses": round(sum(l.amount for l in losses), 2),
    }


def get_suppliers(db: Session):
    prices = db.query(SupplierPrice).all()
    suppliers = {s.id: s.name for s in db.query(Supplier).all()}
    comparison = [
        {
            "supplier": suppliers.get(p.supplier_id, "Unknown"),
            "restaurant_id": p.restaurant_id,
            "product_name": p.product_name,
            "price": p.price,
            "market_avg_price": p.market_avg_price,
            "is_above_market": p.is_above_market,
        }
        for p in prices
    ]
    risky = sorted(
        [c for c in comparison if c["is_above_market"]], key=lambda x: x["price"] - x["market_avg_price"], reverse=True
    )[:5]
    above_market = len([p for p in prices if p.is_above_market])
    largest_changes = sorted(
        [
            {
                "supplier": suppliers.get(p.supplier_id, "Unknown"),
                "product_name": p.product_name,
                "price_change_percent": p.price_change_percent,
            }
            for p in prices
        ],
        key=lambda x: abs(x["price_change_percent"]),
        reverse=True,
    )[:7]

    return {
        "supplier_price_comparison": comparison,
        "risky_suppliers": risky,
        "products_above_market": above_market,
        "largest_price_changes": largest_changes,
    }


def get_prep(db: Session):
    items = db.query(PrepProduction).all()
    high_risk = [i for i in items if i.overproduction_risk >= 65]
    avg_risk = sum(i.overproduction_risk for i in items) / (len(items) or 1)

    return {
        "prep_items": [
            {
                "id": i.id,
                "restaurant_id": i.restaurant_id,
                "item_name": i.item_name,
                "shelf_life_hours": i.shelf_life_hours,
                "current_stock": i.current_stock,
                "avg_sales_per_lifetime": i.avg_sales_per_lifetime,
                "recommended_prep": i.recommended_prep,
                "overproduction_risk": i.overproduction_risk,
            }
            for i in items
        ],
        "high_risk_items": [
            {"item_name": i.item_name, "restaurant_id": i.restaurant_id, "overproduction_risk": i.overproduction_risk}
            for i in high_risk
        ],
        "average_overproduction_risk": round(avg_risk, 2),
    }


def get_kitchen(db: Session):
    rows = db.query(KitchenPerformance).all()
    bottlenecks = [r for r in rows if r.avg_cook_time > 15 or r.load_percent > 85]

    return {
        "station_performance": [
            {
                "id": r.id,
                "restaurant_id": r.restaurant_id,
                "station_name": r.station_name,
                "avg_cook_time": r.avg_cook_time,
                "orders_count": r.orders_count,
                "errors_count": r.errors_count,
                "load_percent": r.load_percent,
            }
            for r in rows
        ],
        "bottlenecks": [
            {
                "station_name": r.station_name,
                "restaurant_id": r.restaurant_id,
                "avg_cook_time": r.avg_cook_time,
                "load_percent": r.load_percent,
            }
            for r in bottlenecks
        ],
        "average_cook_time": round(sum(r.avg_cook_time for r in rows) / (len(rows) or 1), 2),
        "overloaded_stations": len([r for r in rows if r.load_percent > 85]),
    }


def get_profitability(db: Session):
    restaurants = db.query(Restaurant).all()
    table = [
        {
            "id": r.id,
            "name": r.name,
            "city": r.city,
            "monthly_revenue": r.monthly_revenue,
            "net_profit": r.net_profit,
            "margin_percent": round((r.net_profit / r.monthly_revenue * 100) if r.monthly_revenue else 0, 2),
            "food_cost_percent": r.food_cost_percent,
            "labor_cost_percent": r.labor_cost_percent,
            "status": r.status,
        }
        for r in restaurants
    ]
    sorted_table = sorted(table, key=lambda x: x["margin_percent"], reverse=True)
    return {
        "restaurant_profitability_table": table,
        "top_performers": sorted_table[:3],
        "worst_performers": sorted_table[-3:],
    }
