import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

export default async function KitchenPage() {
  let data: any = { station_performance: [], bottlenecks: [] }
  let apiError = ''
  try {
    data = await apiGet<any>('/api/dashboard/kitchen')
  } catch {
    apiError = 'Не удалось загрузить данные кухни из backend API.'
  }

  return (
    <AppShell>
      {apiError ? <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-xs text-red-200'>{apiError}</div> : null}
      <div className='grid gap-4 lg:grid-cols-2'>
        <Card><h2 className='mb-3 text-lg font-semibold'>Загрузка станций</h2><SimpleBars data={data.station_performance} x='station_name' y='load_percent' /></Card>
        <Card>
          <h2 className='mb-3 text-lg font-semibold'>Узкие места</h2>
          <ul className='space-y-2 text-sm'>{data.bottlenecks.map((b: any, i: number) => <li key={i} className='rounded-lg bg-slate-800 p-3'>{b.station_name}: {b.avg_cook_time} мин, загрузка {b.load_percent}%</li>)}</ul>
        </Card>
      </div>
    </AppShell>
  )
}
