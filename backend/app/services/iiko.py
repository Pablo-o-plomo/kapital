from typing import Any

import httpx

from app.core.config import settings


class IikoIntegrationError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _to_user_message(status_code: int, payload: dict[str, Any] | None = None) -> str:
    detail = (payload or {}).get('errorDescription') or (payload or {}).get('description')
    if status_code == 401:
        return 'Unauthorized: check IIKO_API_LOGIN'
    if status_code == 400:
        return f'Bad request: {detail or "invalid request parameters"}'
    if status_code >= 500:
        return 'iiko API internal error'
    return detail or 'iiko API request failed'


async def get_access_token() -> str:
    if not settings.iiko_api_login:
        raise IikoIntegrationError(400, 'IIKO_API_LOGIN is not configured')

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f'{settings.iiko_base_url}/api/1/access_token',
                json={'apiLogin': settings.iiko_api_login},
            )
    except httpx.RequestError as exc:
        raise IikoIntegrationError(503, f'Network error: failed to connect to iiko API ({exc})') from exc

    if response.status_code >= 400:
        payload = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
        raise IikoIntegrationError(response.status_code, _to_user_message(response.status_code, payload))

    payload: dict[str, Any] = response.json()
    token = payload.get('token')
    if not token:
        raise IikoIntegrationError(500, 'Token was not returned by iiko API')
    return str(token)


async def _authorized_post(endpoint: str, token: str, body: dict[str, Any]) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f'{settings.iiko_base_url}{endpoint}',
                headers={'Authorization': f'Bearer {token}'},
                json=body,
            )
    except httpx.RequestError as exc:
        raise IikoIntegrationError(503, f'Network error: failed to connect to iiko API ({exc})') from exc

    payload = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
    if response.status_code >= 400:
        raise IikoIntegrationError(response.status_code, _to_user_message(response.status_code, payload))
    return payload


async def get_organizations(token: str) -> list[dict[str, Any]]:
    payload = await _authorized_post('/api/1/organizations', token, {'returnAdditionalInfo': True})
    return payload.get('organizations', [])


async def get_terminal_groups(token: str, organization_id: str) -> list[dict[str, Any]]:
    payload = await _authorized_post('/api/1/terminal_groups', token, {'organizationIds': [organization_id]})
    groups = payload.get('terminalGroups', [])
    return [group for group in groups if group.get('organizationId') == organization_id]


async def get_nomenclature(token: str, organization_id: str, start_revision: int = 0) -> dict[str, Any]:
    payload = await _authorized_post(
        '/api/1/nomenclature',
        token,
        {'organizationId': organization_id, 'startRevision': start_revision},
    )
    products = payload.get('products', [])
    return {
        'products_count': len(products),
        'revision': payload.get('revision', start_revision),
        'groups_count': len(payload.get('groups', [])),
    }


async def get_iiko_check() -> dict[str, Any]:
    try:
        token = await get_access_token()
        organizations = await get_organizations(token)
        return {
            'connection_status': 'success',
            'token_received': True,
            'organizations_found': len(organizations),
            'error': None,
        }
    except IikoIntegrationError as exc:
        return {
            'connection_status': 'error',
            'token_received': False,
            'organizations_found': 0,
            'error': exc.message,
        }
