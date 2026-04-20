from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from app.models.entities import (
    Block,
    Issue,
    IssueAnalysis,
    IssueStatus,
    IssueType,
    Metric,
    Period,
    ProductPrice,
    Severity,
    Task,
    TaskStatus,
)

STANDARD_BLOCKS: list[tuple[str, str]] = [
    ('Выручка и чек', 'revenue_check'),
    ('Food Cost', 'food_cost'),
    ('Склад и потери', 'inventory_losses'),
    ('Закупки', 'purchases'),
    ('ФОТ', 'fot'),
    ('Красные зоны', 'red_zones'),
    ('Решения и результат', 'decisions_result'),
]


BLOCK_BY_ISSUE_TYPE = {
    IssueType.food_cost: 'food_cost',
    IssueType.purchases: 'purchases',
    IssueType.inventory: 'inventory_losses',
    IssueType.write_offs: 'inventory_losses',
    IssueType.fot: 'fot',
    IssueType.revenue: 'revenue_check',
    IssueType.avg_check: 'revenue_check',
    IssueType.supplier_price: 'purchases',
    IssueType.custom: 'red_zones',
}


def create_standard_blocks(db: Session, period_id: int) -> list[Block]:
    blocks: list[Block] = []
    for name, code in STANDARD_BLOCKS:
        block = Block(period_id=period_id, name=name, code=code, status='open')
        db.add(block)
        blocks.append(block)
    db.flush()
    return blocks


def _ensure_issue(db: Session, period_id: int, issue_type: IssueType, title: str, description: str, severity: Severity) -> None:
    code = BLOCK_BY_ISSUE_TYPE[issue_type]
    block = db.query(Block).filter(Block.period_id == period_id, Block.code == code).first()
    if not block:
        return
    exists = db.query(Issue).filter(Issue.period_id == period_id, Issue.type == issue_type, Issue.title == title).first()
    if exists:
        return
    db.add(Issue(period_id=period_id, block_id=block.id, type=issue_type, title=title, description=description, severity=severity))


def create_metric_issues(db: Session, metric: Metric) -> None:
    period = db.query(Period).filter(Period.id == metric.period_id).first()
    if not period:
        return

    if metric.food_cost_percent > 25:
        _ensure_issue(db, metric.period_id, IssueType.food_cost, 'Food Cost выше 25%', 'Проверьте закупки и списания.', Severity.red)
    if metric.fot_percent > 13:
        _ensure_issue(db, metric.period_id, IssueType.fot, 'ФОТ выше 13%', 'Требуется оптимизация графиков.', Severity.red)
    if float(metric.write_offs_value) > 100000:
        _ensure_issue(db, metric.period_id, IssueType.write_offs, 'Списания выше 100 000', 'Проверьте контроль потерь.', Severity.red)
    if float(metric.negative_stock_value) > 0:
        _ensure_issue(db, metric.period_id, IssueType.inventory, 'Обнаружены отрицательные остатки', 'Необходимо сверить склад.', Severity.red)

    prev_period = (
        db.query(Period)
        .filter(Period.restaurant_id == period.restaurant_id, Period.end_date < period.start_date)
        .order_by(Period.end_date.desc())
        .first()
    )
    if not prev_period:
        return
    prev_metric = db.query(Metric).filter(Metric.period_id == prev_period.id).first()
    if not prev_metric:
        return

    if float(prev_metric.avg_check) > 0 and float(metric.avg_check) < float(prev_metric.avg_check):
        _ensure_issue(db, metric.period_id, IssueType.avg_check, 'Средний чек снизился', 'Снижение относительно прошлой недели.', Severity.yellow)
    if float(prev_metric.revenue) > 0 and float(metric.revenue) < float(prev_metric.revenue):
        _ensure_issue(db, metric.period_id, IssueType.revenue, 'Выручка снизилась', 'Снижение относительно прошлой недели.', Severity.yellow)


def create_supplier_price_issue(db: Session, price_row: ProductPrice) -> None:
    previous = (
        db.query(ProductPrice)
        .filter(
            ProductPrice.product_id == price_row.product_id,
            ProductPrice.restaurant_id == price_row.restaurant_id,
            ProductPrice.id != price_row.id,
        )
        .order_by(ProductPrice.price_date.desc(), ProductPrice.id.desc())
        .first()
    )
    if not previous or float(previous.price) <= 0:
        return

    growth = (float(price_row.price) - float(previous.price)) / float(previous.price) * 100
    if growth <= 5:
        return

    severity = Severity.red if growth > 10 else Severity.yellow
    current_period = (
        db.query(Period)
        .filter(
            Period.restaurant_id == price_row.restaurant_id,
            Period.start_date <= price_row.price_date,
            Period.end_date >= price_row.price_date,
        )
        .first()
    )
    if not current_period:
        current_period = (
            db.query(Period)
            .filter(Period.restaurant_id == price_row.restaurant_id)
            .order_by(Period.end_date.desc())
            .first()
        )
    if not current_period:
        return

    _ensure_issue(
        db,
        current_period.id,
        IssueType.supplier_price,
        'Рост закупочной цены',
        f'Рост цены составил {growth:.2f}% по сравнению с предыдущей.',
        severity,
    )


def validate_issue_resolve(db: Session, issue: Issue) -> None:
    analysis = db.query(IssueAnalysis).filter(IssueAnalysis.issue_id == issue.id).first()
    if not analysis:
        raise ValueError('Issue cannot be resolved without analysis')
    if not analysis.reason.strip() or not analysis.solution.strip() or not analysis.assigned_user_id:
        raise ValueError('Issue analysis must include reason, solution and assigned user')


def can_close_period(db: Session, period_id: int) -> tuple[bool, str]:
    open_issues = db.query(Issue).filter(Issue.period_id == period_id, Issue.status != IssueStatus.resolved).count()
    if open_issues:
        return False, 'Period has unresolved issues'

    open_tasks = (
        db.query(Task)
        .join(Block, Block.id == Task.block_id)
        .filter(Block.period_id == period_id, Task.status.in_([TaskStatus.open, TaskStatus.in_progress]))
        .count()
    )
    if open_tasks:
        return False, 'Period has open tasks'
    return True, ''
