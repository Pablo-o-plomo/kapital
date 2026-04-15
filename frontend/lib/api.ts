import 'server-only'

import { headers } from 'next/headers'

function getOrigin() {
  const h = headers()
  const host = h.get('host')
  const proto = process.env.APP_ENV === 'production' ? 'https' : 'http'
  return `${proto}://${host}`
}

export async function apiGet<T>(path: string): Promise<T> {
  const origin = getOrigin()
  const res = await fetch(`${origin}/api/proxy${path}`, { cache: 'no-store' })
  if (!res.ok) {
    throw new Error(`API error ${res.status}`)
  }
  return res.json()
}
