import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

const fallback = {
  station_performance: [
    { station_name: 'Гриль', load_percent: 88, avg_cook_time: 17.2 },
    { station_name: 'Горячий цех', load_percent: 92, avg_cook_time: 19.1 },
    { station_name: 'Экспедиция', load_percent: 95, avg_cook_time: 16.4 }
  ],
  bottlenecks: [
    { station_name: 'Горячий цех', avg_cook_time: 19.1, load_percent: 92 },
    { station_name: 'Экспедиция', avg_cook_time: 16.4, load_percent: 95 }
  ]
}

export default async function KitchenPage() {
  const data = await apiGet<any>('/api/dashboard/kitchen', fallback)
  return (
    <AppShell>
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
