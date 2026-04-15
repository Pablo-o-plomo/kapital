import { headers } from 'next/headers'

import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'

async function getCheck() {
  try {
    const h = headers()
    const host = h.get('host')
    const protocol = process.env.APP_ENV === 'production' ? 'https' : 'http'
    const res = await fetch(`${protocol}://${host}/api/system/backend-check`, { cache: 'no-store' })
    if (!res.ok) return { error: `status ${res.status}` }
    return await res.json()
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'unknown error' }
  }
}

export default async function ApiTestPage() {
  const data = await getCheck()

  return (
    <AppShell>
      <Card>
        <h2 className='mb-3 text-lg font-semibold'>Проверка связи frontend → backend API</h2>
        <pre className='overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-200'>
{JSON.stringify(data, null, 2)}
        </pre>
      </Card>
    </AppShell>
  )
}
