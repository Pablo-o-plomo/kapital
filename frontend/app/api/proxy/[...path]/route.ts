import { NextRequest, NextResponse } from 'next/server'

import { fetchBackend } from '@/lib/backend-target'

async function proxy(request: NextRequest, pathParts: string[]) {
  const path = `/${pathParts.join('/')}`
  const method = request.method
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }

  const bodyAllowed = !['GET', 'HEAD'].includes(method)
  const body = bodyAllowed ? await request.text() : undefined

  try {
    const { res, base } = await fetchBackend(path, {
      method,
      headers,
      body,
    })

    const text = await res.text()
    const contentType = res.headers.get('content-type') || 'application/json'

    return new NextResponse(text, {
      status: res.status,
      headers: {
        'content-type': contentType,
        'x-proxy-backend': base,
      },
    })
  } catch (error) {
    return NextResponse.json(
      { detail: error instanceof Error ? error.message : 'backend proxy failed' },
      { status: 502 },
    )
  }
}

export async function GET(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxy(request, params.path)
}

export async function POST(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxy(request, params.path)
}
