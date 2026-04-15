import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

const fallbackRestaurants = [
  { id: 1, name: 'Москва / Авиапарк', city: 'Москва', format: 'Флагман', monthly_revenue: 14200000, avg_check: 1680, food_cost_percent: 31.5, labor_cost_percent: 27.8, write_offs: 420000, net_profit: 2960000, status: 'stable' },
  { id: 2, name: 'Ростов-на-Дону', city: 'Ростов-на-Дону', format: 'Street Casual', monthly_revenue: 8600000, avg_check: 1180, food_cost_percent: 35.9, labor_cost_percent: 29.5, write_offs: 510000, net_profit: 980000, status: 'attention' },
  { id: 3, name: 'Южно-Сахалинск', city: 'Южно-Сахалинск', format: 'Premium Seafood', monthly_revenue: 12300000, avg_check: 2140, food_cost_percent: 38.4, labor_cost_percent: 30.6, write_offs: 760000, net_profit: 1040000, status: 'critical' }
]

export default async function RestaurantsPage() {
  const restaurants = await apiGet<any[]>('/api/restaurants', fallbackRestaurants)
  return (
    <AppShell>
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
