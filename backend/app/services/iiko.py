from typing import Any

import httpx

from app.core.config import settings


async def get_iiko_access_token() -> str:
    if not settings.iiko_api_login:
        raise ValueError('IIKO_API_LOGIN is not configured')

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f'{settings.iiko_base_url}/api/1/access_token',
            json={'apiLogin': settings.iiko_api_login},
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        token = payload.get('token')
        if not token:
            raise ValueError('Token was not returned by iiko API')
        return str(token)


async def get_iiko_status() -> dict[str, Any]:
    try:
        token = await get_iiko_access_token()
    except Exception as exc:  # noqa: BLE001 - surface integration error to API response
        return {'connected': False, 'error': str(exc)}

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f'{settings.iiko_base_url}/api/1/organizations',
            json={'accessToken': token, 'returnAdditionalInfo': False},
        )
        if response.status_code >= 400:
            return {'connected': False, 'error': f'iiko organizations error: {response.status_code}'}

        payload = response.json()
        organizations = payload.get('organizations', [])
        return {'connected': True, 'organizations_count': len(organizations)}
