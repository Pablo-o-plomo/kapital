from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Restaurant
from app.schemas.entities import RestaurantOut
from app.seed import reset_and_seed_data
from app.services.dashboard import get_kitchen, get_losses, get_prep, get_profitability, get_summary, get_suppliers
from app.services.iiko import get_iiko_status
from app.services.auth import AuthError, login, verify_token

router = APIRouter()


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'



@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/api/restaurants", response_model=list[RestaurantOut])
def restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.get("/api/restaurants/{restaurant_id}", response_model=RestaurantOut)
def restaurant_detail(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get("/api/dashboard/losses")
def dashboard_losses(db: Session = Depends(get_db)):
    return get_losses(db)


@router.get("/api/dashboard/suppliers")
def dashboard_suppliers(db: Session = Depends(get_db)):
    return get_suppliers(db)


@router.get("/api/dashboard/prep")
def dashboard_prep(db: Session = Depends(get_db)):
    return get_prep(db)


@router.get("/api/dashboard/kitchen")
def dashboard_kitchen(db: Session = Depends(get_db)):
    return get_kitchen(db)


@router.get("/api/dashboard/profitability")
def dashboard_profitability(db: Session = Depends(get_db)):
    return get_profitability(db)


@router.post("/api/demo/reset-data")
def reset_demo_data(db: Session = Depends(get_db)):
    reset_and_seed_data(db)
    return {"status": "ok", "message": "Demo data reset completed"}


@router.get("/api/integrations/iiko/status")
async def iiko_integration_status():
    return await get_iiko_status()


@router.post("/api/auth/login", response_model=TokenOut)
def auth_login(payload: LoginIn):
    try:
        token = login(payload.email, payload.password)
    except AuthError:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenOut(access_token=token)


@router.get("/api/auth/me")
def auth_me(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Missing bearer token')
    token = authorization.split(' ', 1)[1]
    try:
        payload = verify_token(token)
    except AuthError:
        raise HTTPException(status_code=401, detail='Invalid token')
    return {'email': payload.get('sub'), 'role': payload.get('role')}
