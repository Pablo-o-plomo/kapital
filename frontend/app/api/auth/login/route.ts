import { NextRequest, NextResponse } from 'next/server'

import { fetchBackend } from '@/lib/backend-target'

const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@kapital.director'
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'ChangeMeStrongPassword'

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}))

  try {
    const { res } = await fetchBackend('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    const payload = await res.json().catch(() => ({ detail: 'Backend auth error' }))
    if (!res.ok) {
      return NextResponse.json(payload, { status: res.status })
    }

    return NextResponse.json(payload)
  } catch {
    if (body?.email?.toLowerCase?.() === ADMIN_EMAIL.toLowerCase() && body?.password === ADMIN_PASSWORD) {
      const fallbackToken = Buffer.from(`${body.email}:${Date.now()}`).toString('base64url')
      return NextResponse.json({ access_token: fallbackToken, token_type: 'bearer', source: 'frontend_fallback' })
    }

    return NextResponse.json({ detail: 'Unable to reach backend auth service' }, { status: 502 })
  }
}
