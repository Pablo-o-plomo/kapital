from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


class AuthError(Exception):
    pass


def login(email: str, password: str) -> str:
    if email.strip().lower() != settings.admin_email.lower() or password != settings.admin_password:
        raise AuthError('Invalid credentials')

    payload = {
        'sub': email.strip().lower(),
        'role': 'operations_director',
        'exp': datetime.now(timezone.utc) + timedelta(hours=12),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm='HS256')


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])
    except jwt.PyJWTError as exc:
        raise AuthError('Invalid token') from exc
