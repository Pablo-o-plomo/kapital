const candidates = [
  process.env.BACKEND_PUBLIC_URL,
  process.env.BACKEND_INTERNAL_URL,
  process.env.NEXT_PUBLIC_API_URL,
  'http://backend:8000',
  'http://localhost:8000',
].filter(Boolean) as string[]

export function getBackendTargets(): string[] {
  return [...new Set(candidates.map((item) => item.replace(/\/$/, '')))]
}

export async function fetchBackend(path: string, init?: RequestInit) {
  const errors: string[] = []
  for (const base of getBackendTargets()) {
    try {
      const res = await fetch(`${base}${path}`, { ...init, cache: 'no-store' })
      return { res, base }
    } catch (error) {
      errors.push(`${base}: ${error instanceof Error ? error.message : 'unknown error'}`)
    }
  }
  throw new Error(`All backend targets failed: ${errors.join(' | ')}`)
}
