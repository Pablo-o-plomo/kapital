from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import allowed_restaurant_ids, get_current_user, require_roles
from app.db.session import get_db
from app.models.entities import (
    Block,
    Comment,
    Company,
    Issue,
    IssueAnalysis,
    IssueStatus,
    Metric,
    Period,
    PeriodStatus,
    Product,
    ProductPrice,
    Restaurant,
    RestaurantUser,
    Supplier,
    Task,
    TaskStatus,
    User,
    UserRole,
)
from app.schemas.entities import *
from app.services.auth import hash_password, login
from app.services.rules import can_close_period, create_metric_issues, create_standard_blocks, create_supplier_price_issue, validate_issue_resolve

router = APIRouter()


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.post('/auth/register', response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner))):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, 'Email already exists')
    user = User(full_name=payload.full_name, email=payload.email, hashed_password=hash_password(payload.password), role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/auth/login', response_model=TokenOut)
def auth_login(payload: LoginIn, db: Session = Depends(get_db)):
    return TokenOut(access_token=login(db, payload.email, payload.password))


@router.get('/auth/me', response_model=UserOut)
def auth_me(user: User = Depends(get_current_user)):
    return user


@router.get('/users', response_model=list[UserOut])
def users(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner))):
    return db.query(User).all()


@router.get('/users/{user_id}', response_model=UserOut)
def user_detail(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, 'User not found')
    return user


@router.get('/restaurants', response_model=list[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role in [UserRole.admin, UserRole.owner]:
        return db.query(Restaurant).all()
    ids = allowed_restaurant_ids(db, user)
    return db.query(Restaurant).filter(Restaurant.id.in_(ids)).all()


@router.post('/restaurants', response_model=RestaurantOut)
def create_restaurant(payload: RestaurantCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner))):
    restaurant = Restaurant(**payload.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get('/restaurants/{restaurant_id}', response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(404, 'Restaurant not found')
    if user.role not in [UserRole.admin, UserRole.owner] and restaurant.id not in allowed_restaurant_ids(db, user):
        raise HTTPException(403, 'Forbidden')
    return restaurant


@router.get('/periods', response_model=list[PeriodOut])
def periods(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Period)
    if user.role not in [UserRole.admin, UserRole.owner]:
        ids = allowed_restaurant_ids(db, user)
        query = query.filter(Period.restaurant_id.in_(ids))
    return query.order_by(Period.start_date.desc()).all()


@router.post('/periods', response_model=PeriodOut)
def create_period(payload: PeriodCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager))):
    period = Period(**payload.model_dump())
    db.add(period)
    db.flush()
    create_standard_blocks(db, period.id)
    db.commit()
    db.refresh(period)
    return period


@router.get('/periods/{period_id}', response_model=PeriodOut)
def period_detail(period_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(404, 'Period not found')
    if user.role not in [UserRole.admin, UserRole.owner] and period.restaurant_id not in allowed_restaurant_ids(db, user):
        raise HTTPException(403, 'Forbidden')
    return period


@router.patch('/periods/{period_id}', response_model=PeriodOut)
def update_period(period_id: int, payload: PeriodUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager))):
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(404, 'Period not found')
    if payload.status == PeriodStatus.closed:
        ok, reason = can_close_period(db, period.id)
        if not ok:
            raise HTTPException(400, reason)
    period.status = payload.status
    db.commit()
    db.refresh(period)
    return period


@router.get('/periods/{period_id}/blocks', response_model=list[BlockOut])
def period_blocks(period_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Block).filter(Block.period_id == period_id).all()


@router.get('/tasks', response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Task)
    if user.role == UserRole.chef:
        query = query.filter(Task.title.ilike('%кух%') | Task.title.ilike('%food cost%') | Task.title.ilike('%списан%') | Task.title.ilike('%закуп%'))
    return query.order_by(Task.created_at.desc()).all()


@router.post('/tasks', response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant))):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get('/tasks/{task_id}', response_model=TaskOut)
def task_detail(task_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, 'Task not found')
    return task


@router.patch('/tasks/{task_id}', response_model=TaskOut)
def task_update(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant, UserRole.chef))):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, 'Task not found')
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    if task.status == TaskStatus.done and not task.completed_at:
        task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


@router.delete('/tasks/{task_id}')
def task_delete(task_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager))):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, 'Task not found')
    db.delete(task)
    db.commit()
    return {'status': 'ok'}


@router.get('/issues', response_model=list[IssueOut])
def list_issues(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Issue).order_by(Issue.created_at.desc()).all()


@router.get('/issues/{issue_id}', response_model=IssueOut)
def issue_detail(issue_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(404, 'Issue not found')
    return issue


@router.get('/periods/{period_id}/issues', response_model=list[IssueOut])
def period_issues(period_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Issue).filter(Issue.period_id == period_id).order_by(Issue.created_at.desc()).all()


@router.post('/issues', response_model=IssueOut)
def create_issue(payload: IssueCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant))):
    issue = Issue(**payload.model_dump())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


@router.patch('/issues/{issue_id}', response_model=IssueOut)
def patch_issue(issue_id: int, payload: IssueUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant, UserRole.chef))):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(404, 'Issue not found')
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(issue, k, v)
    if issue.status == IssueStatus.resolved:
        try:
            validate_issue_resolve(db, issue)
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
    db.commit()
    db.refresh(issue)
    return issue




@router.get('/issues/{issue_id}/analysis', response_model=IssueAnalysisOut)
def get_issue_analysis(issue_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    analysis = db.query(IssueAnalysis).filter(IssueAnalysis.issue_id == issue_id).first()
    if not analysis:
        raise HTTPException(404, 'Analysis not found')
    return analysis

@router.post('/issues/{issue_id}/analysis', response_model=IssueAnalysisOut)
def create_analysis(issue_id: int, payload: IssueAnalysisIn, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant))):
    if db.query(IssueAnalysis).filter(IssueAnalysis.issue_id == issue_id).first():
        raise HTTPException(400, 'Analysis already exists')
    analysis = IssueAnalysis(issue_id=issue_id, **payload.model_dump())
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.patch('/issues/{issue_id}/analysis', response_model=IssueAnalysisOut)
def patch_analysis(issue_id: int, payload: IssueAnalysisIn, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.manager, UserRole.accountant))):
    analysis = db.query(IssueAnalysis).filter(IssueAnalysis.issue_id == issue_id).first()
    if not analysis:
        raise HTTPException(404, 'Analysis not found')
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(analysis, k, v)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.post('/comments', response_model=CommentOut)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not payload.issue_id and not payload.task_id:
        raise HTTPException(400, 'issue_id or task_id required')
    comment = Comment(user_id=user.id, **payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get('/issues/{issue_id}/comments', response_model=list[CommentOut])
def issue_comments(issue_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Comment).filter(Comment.issue_id == issue_id).order_by(Comment.created_at.desc()).all()


@router.get('/tasks/{task_id}/comments', response_model=list[CommentOut])
def task_comments(task_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()


@router.post('/metrics', response_model=MetricOut)
def create_metric(payload: MetricCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.accountant, UserRole.manager))):
    metric = Metric(**payload.model_dump())
    db.add(metric)
    db.flush()
    create_metric_issues(db, metric)
    db.commit()
    db.refresh(metric)
    return metric


@router.get('/periods/{period_id}/metrics', response_model=MetricOut)
def get_period_metric(period_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    metric = db.query(Metric).filter(Metric.period_id == period_id).first()
    if not metric:
        raise HTTPException(404, 'Metric not found')
    return metric


@router.patch('/metrics/{metric_id}', response_model=MetricOut)
def update_metric(metric_id: int, payload: MetricUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.accountant, UserRole.manager))):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(404, 'Metric not found')
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(metric, k, v)
    create_metric_issues(db, metric)
    db.commit()
    db.refresh(metric)
    return metric


@router.get('/products', response_model=list[ProductOut])
def products(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Product).all()


@router.post('/products', response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.accountant))):
    row = Product(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get('/suppliers', response_model=list[SupplierOut])
def suppliers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Supplier).all()


@router.post('/suppliers', response_model=SupplierOut)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.accountant))):
    row = Supplier(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get('/prices', response_model=list[ProductPriceOut])
def prices(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(ProductPrice).order_by(ProductPrice.price_date.desc()).all()


@router.post('/prices', response_model=ProductPriceOut)
def create_price(payload: ProductPriceCreate, db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.admin, UserRole.owner, UserRole.accountant))):
    row = ProductPrice(**payload.model_dump(), created_by_user_id=user.id)
    db.add(row)
    db.flush()
    create_supplier_price_issue(db, row)
    db.commit()
    db.refresh(row)
    return row


@router.get('/dashboard/summary')
def dashboard_summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rest_query = db.query(Restaurant)
    if user.role not in [UserRole.admin, UserRole.owner]:
        ids = allowed_restaurant_ids(db, user)
        rest_query = rest_query.filter(Restaurant.id.in_(ids))
    restaurants = rest_query.all()

    payload = []
    for restaurant in restaurants:
        period = (
            db.query(Period)
            .filter(Period.restaurant_id == restaurant.id)
            .order_by(Period.end_date.desc())
            .first()
        )
        if not period:
            continue
        metric = db.query(Metric).filter(Metric.period_id == period.id).first()
        red_issues = db.query(Issue).filter(Issue.period_id == period.id, Issue.severity == 'red', Issue.status != IssueStatus.resolved).count()
        open_tasks = db.query(Task).join(Block, Task.block_id == Block.id).filter(Block.period_id == period.id, Task.status.in_([TaskStatus.open, TaskStatus.in_progress])).count()
        payload.append(
            {
                'restaurant_id': restaurant.id,
                'restaurant_name': restaurant.name,
                'period_id': period.id,
                'period_status': period.status,
                'period_dates': f'{period.start_date} - {period.end_date}',
                'red_issues': red_issues,
                'open_tasks': open_tasks,
                'revenue': float(metric.revenue) if metric else 0,
                'food_cost_percent': metric.food_cost_percent if metric else 0,
                'fot_percent': metric.fot_percent if metric else 0,
            }
        )
    return {'restaurants': payload}
