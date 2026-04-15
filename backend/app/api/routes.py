from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.entities import Restaurant
from app.schemas.entities import RestaurantOut
from app.seed import reset_and_seed_data
from app.services.dashboard import get_kitchen, get_losses, get_prep, get_profitability, get_summary, get_suppliers
from app.services.iiko import (
    IikoIntegrationError,
    get_access_token,
    get_iiko_check,
    get_nomenclature,
    get_organizations,
    get_terminal_groups,
)
from app.services.auth import AuthError, login, verify_token

router = APIRouter()


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/api/restaurants', response_model=list[RestaurantOut])
def restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.get('/api/restaurants/{restaurant_id}', response_model=RestaurantOut)
def restaurant_detail(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail='Restaurant not found')
    return restaurant


@router.get('/api/dashboard/summary')
def dashboard_summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get('/api/dashboard/losses')
def dashboard_losses(db: Session = Depends(get_db)):
    return get_losses(db)


@router.get('/api/dashboard/suppliers')
def dashboard_suppliers(db: Session = Depends(get_db)):
    return get_suppliers(db)


@router.get('/api/dashboard/prep')
def dashboard_prep(db: Session = Depends(get_db)):
    return get_prep(db)


@router.get('/api/dashboard/kitchen')
def dashboard_kitchen(db: Session = Depends(get_db)):
    return get_kitchen(db)


@router.get('/api/dashboard/profitability')
def dashboard_profitability(db: Session = Depends(get_db)):
    return get_profitability(db)


@router.post('/api/demo/reset-data')
def reset_demo_data(db: Session = Depends(get_db)):
    reset_and_seed_data(db)
    return {'status': 'ok', 'message': 'Demo data reset completed'}


@router.get('/api/integrations/iiko/check')
async def iiko_check():
    return await get_iiko_check()


@router.get('/api/integrations/iiko/organizations')
async def iiko_organizations():
    try:
        token = await get_access_token()
        organizations = await get_organizations(token)
        return {'organizations': organizations}
    except IikoIntegrationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get('/api/integrations/iiko/terminal-groups')
async def iiko_terminal_groups(organization_id: str | None = Query(default=None)):
    org_id = organization_id or settings.iiko_organization_id
    if not org_id:
        raise HTTPException(status_code=400, detail='Bad request: invalid organizationId')

    try:
        token = await get_access_token()
        groups = await get_terminal_groups(token, org_id)
        return {'organization_id': org_id, 'terminal_groups': groups}
    except IikoIntegrationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get('/api/integrations/iiko/nomenclature')
async def iiko_nomenclature(
    organization_id: str | None = Query(default=None),
    start_revision: int = Query(default=0),
):
    org_id = organization_id or settings.iiko_organization_id
    if not org_id:
        raise HTTPException(status_code=400, detail='Bad request: invalid organizationId')

    try:
        token = await get_access_token()
        nomenclature = await get_nomenclature(token, org_id, start_revision)
        return {'organization_id': org_id, **nomenclature}
    except IikoIntegrationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get('/api/integrations/iiko/overview')
async def iiko_overview(organization_id: str | None = Query(default=None)):
    try:
        token = await get_access_token()
        organizations = await get_organizations(token)

        selected_org_id = organization_id or settings.iiko_organization_id or (organizations[0].get('id') if organizations else '')
        selected_org = next((item for item in organizations if item.get('id') == selected_org_id), None)

        terminal_groups = await get_terminal_groups(token, selected_org_id) if selected_org_id else []
        nomenclature = await get_nomenclature(token, selected_org_id, 0) if selected_org_id else {'products_count': 0, 'revision': 0}

        return {
            'connection_status': 'success',
            'token_received': True,
            'organizations': organizations,
            'organizations_found': len(organizations),
            'selected_organization': selected_org,
            'selected_organization_id': selected_org_id,
            'terminal_groups': terminal_groups,
            'terminal_groups_found': len(terminal_groups),
            'products_loaded': nomenclature.get('products_count', 0),
            'revision': nomenclature.get('revision', 0),
        }
    except IikoIntegrationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post('/api/auth/login', response_model=TokenOut)
def auth_login(payload: LoginIn):
    try:
        token = login(payload.email, payload.password)
    except AuthError:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenOut(access_token=token)


@router.get('/api/auth/me')
def auth_me(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Missing bearer token')
    token = authorization.split(' ', 1)[1]
    try:
        payload = verify_token(token)
    except AuthError:
        raise HTTPException(status_code=401, detail='Invalid token')
    return {'email': payload.get('sub'), 'role': payload.get('role')}
