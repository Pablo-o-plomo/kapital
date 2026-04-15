import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

export default async function RestaurantsPage() {
  let restaurants: any[] = []
  let apiError = ''
  try {
    restaurants = await apiGet<any[]>('/api/restaurants')
  } catch {
    apiError = 'Не удалось загрузить рестораны из backend API.'
  }

  return (
    <AppShell>
      {apiError ? <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-xs text-red-200'>{apiError}</div> : null}
      <Card>
        <h2 className='mb-4 text-lg font-semibold'>Рестораны сети</h2>
        <div className='overflow-x-auto'>
          <table className='w-full text-sm'>
            <thead className='text-slate-400'><tr>{['Название','Город','Формат','Выручка','Средний чек','Food cost','Labor cost','Списания','Прибыль','Статус'].map(h => <th key={h} className='px-2 py-3 text-left'>{h}</th>)}</tr></thead>
            <tbody>
              {restaurants.map(r => (
                <tr key={r.id} className='border-t border-slate-800'>
                  <td className='px-2 py-3'>{r.name}</td><td>{r.city}</td><td>{r.format}</td><td>{r.monthly_revenue.toLocaleString('ru-RU')} ₽</td><td>{r.avg_check} ₽</td><td>{r.food_cost_percent}%</td><td>{r.labor_cost_percent}%</td><td>{r.write_offs.toLocaleString('ru-RU')} ₽</td><td>{r.net_profit.toLocaleString('ru-RU')} ₽</td><td><span className={`rounded-full px-2 py-1 text-xs ${r.status==='critical'?'bg-red-500/20 text-red-300':r.status==='attention'?'bg-orange-500/20 text-orange-300':'bg-emerald-500/20 text-emerald-300'}`}>{r.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </AppShell>
  )
}
