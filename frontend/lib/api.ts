const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000'

export async function apiGet<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_URL}${path}`, { cache: 'no-store' })
    if (!res.ok) {
      throw new Error(`API error ${res.status}`)
    }
    return (await res.json()) as T
  } catch {
    return fallback
  }
}
