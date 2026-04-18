from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import (
    Block,
    Comment,
    Company,
    Issue,
    IssueAnalysis,
    IssueType,
    Metric,
    Period,
    Product,
    ProductPrice,
    Restaurant,
    RestaurantUser,
    Severity,
    Supplier,
    Task,
    User,
    UserRole,
)
from app.services.auth import hash_password
from app.services.rules import create_metric_issues, create_standard_blocks, create_supplier_price_issue


def seed(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    users = [
        User(full_name='Admin User', email='admin@example.com', hashed_password=hash_password('password123'), role=UserRole.admin),
        User(full_name='Owner User', email='owner@example.com', hashed_password=hash_password('password123'), role=UserRole.owner),
        User(full_name='Accountant User', email='accountant@example.com', hashed_password=hash_password('password123'), role=UserRole.accountant),
        User(full_name='Manager User', email='manager@example.com', hashed_password=hash_password('password123'), role=UserRole.manager),
        User(full_name='Chef User', email='chef@example.com', hashed_password=hash_password('password123'), role=UserRole.chef),
    ]
    db.add_all(users)
    db.flush()

    company = Company(name='KLEVO Group')
    db.add(company)
    db.flush()

    restaurants = [
        Restaurant(name='Клёво Ростов', company_id=company.id),
        Restaurant(name='Клёво Сочи', company_id=company.id),
        Restaurant(name='Клёво Авиапарк', company_id=company.id),
    ]
    db.add_all(restaurants)
    db.flush()

    for user in users[1:]:
        for restaurant in restaurants:
            db.add(RestaurantUser(user_id=user.id, restaurant_id=restaurant.id))

    products = [
        Product(name='Лосось', category='рыба', unit='кг'),
        Product(name='Тунец', category='рыба', unit='кг'),
        Product(name='Креветка', category='морепродукты', unit='кг'),
        Product(name='Томаты', category='овощи', unit='кг'),
        Product(name='Авокадо', category='овощи', unit='кг'),
    ]
    suppliers = [Supplier(name='FishPro'), Supplier(name='AgroTrade'), Supplier(name='PrimeFood')]
    db.add_all(products + suppliers)
    db.flush()

    today = date.today()
    for idx, restaurant in enumerate(restaurants):
        start = today - timedelta(days=today.weekday() + 7)
        period_prev = Period(restaurant_id=restaurant.id, start_date=start - timedelta(days=7), end_date=start - timedelta(days=1), status='closed')
        period_cur = Period(restaurant_id=restaurant.id, start_date=start, end_date=start + timedelta(days=6), status='issues')
        db.add_all([period_prev, period_cur])
        db.flush()
        create_standard_blocks(db, period_prev.id)
        create_standard_blocks(db, period_cur.id)

        prev_metric = Metric(period_id=period_prev.id, revenue=2_000_000, avg_check=1700, guest_count=1150, food_cost_percent=24, fot_percent=12, write_offs_value=70000, negative_stock_value=0)
        cur_metric = Metric(period_id=period_cur.id, revenue=1_700_000 - idx * 50000, avg_check=1500, guest_count=1000, food_cost_percent=27, fot_percent=14, write_offs_value=120000, negative_stock_value=5000)
        db.add_all([prev_metric, cur_metric])
        db.flush()
        create_metric_issues(db, cur_metric)

        blocks = db.query(Block).filter(Block.period_id == period_cur.id).all()
        revenue_block = next(b for b in blocks if b.code == 'revenue_check')
        issue = Issue(period_id=period_cur.id, block_id=revenue_block.id, type=IssueType.revenue, title='Падение выручки', description='Нужно проверить маркетинг', severity=Severity.yellow)
        db.add(issue)
        db.flush()
        analysis = IssueAnalysis(issue_id=issue.id, reason='Сезонный спад', solution='Запустить акцию', result='', assigned_user_id=users[3].id)
        task = Task(block_id=revenue_block.id, title='Подготовить план акций', description='Согласовать с собственником', assigned_user_id=users[3].id)
        comment = Comment(issue_id=issue.id, user_id=users[2].id, text='Подтверждаю снижение по отчетам')
        db.add_all([analysis, task, comment])

    db.flush()
    prices = [
        ProductPrice(product_id=products[0].id, supplier_id=suppliers[0].id, restaurant_id=restaurants[0].id, price=1000, price_date=today - timedelta(days=7), created_by_user_id=users[2].id),
        ProductPrice(product_id=products[0].id, supplier_id=suppliers[0].id, restaurant_id=restaurants[0].id, price=1130, price_date=today, created_by_user_id=users[2].id),
    ]
    db.add_all(prices)
    db.flush()
    create_supplier_price_issue(db, prices[1])
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)


if __name__ == '__main__':
    main()
