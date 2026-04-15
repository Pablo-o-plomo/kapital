import { NextResponse } from 'next/server'

import { getBackendTargets } from '@/lib/backend-target'

export async function GET() {
  const targets = getBackendTargets()
  const results: Array<{ target: string; ok: boolean; status?: number; error?: string }> = []

  for (const target of targets) {
    try {
      const response = await fetch(`${target}/health`, { cache: 'no-store' })
      results.push({ target, ok: response.ok, status: response.status })
    } catch (error) {
      results.push({ target, ok: false, error: error instanceof Error ? error.message : 'unknown error' })
    }
  }

  return NextResponse.json({ targets, results })
}
