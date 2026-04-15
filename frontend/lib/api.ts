import { fetchBackend } from './backend-target'

export async function apiGet<T>(path: string): Promise<T> {
  const { res } = await fetchBackend(path)
  if (!res.ok) {
    throw new Error(`API error ${res.status}`)
  }
  return res.json()
}
