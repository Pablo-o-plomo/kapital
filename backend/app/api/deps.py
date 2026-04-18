from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import RestaurantUser, User, UserRole
from app.services.auth import decode_token


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Missing bearer token')
    token = authorization.split(' ', 1)[1]
    payload = decode_token(token)
    user = db.query(User).filter(User.id == int(payload['sub'])).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail='Invalid user')
    return user


def require_roles(*roles: UserRole):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles and user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail='Insufficient permissions')
        return user

    return checker


def allowed_restaurant_ids(db: Session, user: User) -> list[int]:
    if user.role == UserRole.admin:
        return [r for (r,) in db.query(RestaurantUser.restaurant_id).all()]
    rows = db.query(RestaurantUser.restaurant_id).filter(RestaurantUser.user_id == user.id).all()
    return [r for (r,) in rows]
