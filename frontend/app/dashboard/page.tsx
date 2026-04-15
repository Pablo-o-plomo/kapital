import { AlertTriangle, CircleDollarSign, TrendingDown, TrendingUp } from 'lucide-react'

import { AppShell } from '@/components/app-shell'
import { RevenueProfitChart, SimpleBars } from '@/components/charts'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

export default async function DashboardPage() {
  let summary: any = { total_revenue: 0, total_net_profit: 0, total_write_offs: 0, critical_alerts_count: 0 }
  let profitability: any = { restaurant_profitability_table: [], worst_performers: [] }
  let losses: any = { losses_by_category: [] }
  let iikoStatus: any = { connected: false, organizations_count: 0, error: '' }
  let apiError = ''

  try {
    ;[summary, profitability, losses, iikoStatus] = await Promise.all([
      apiGet('/api/dashboard/summary'),
      apiGet('/api/dashboard/profitability'),
      apiGet('/api/dashboard/losses'),
      apiGet('/api/integrations/iiko/check'),
    ])
  } catch {
    apiError = 'Backend API недоступен или не настроен. Проверьте сервис backend и переменные окружения.'
  }

  const chartData = profitability.restaurant_profitability_table.map((r: any) => ({ name: r.city, revenue: r.monthly_revenue, profit: r.net_profit }))

  return (
    <AppShell>
      {apiError ? (
        <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-xs text-red-200'>{apiError}</div>
      ) : null}

      <div className='mb-3 rounded-xl border border-cyan-600/30 bg-cyan-500/10 px-4 py-2 text-xs text-cyan-200'>
        iiko статус: {iikoStatus.connected ? `подключено (${iikoStatus.organizations_count} орг.)` : `не подключено${iikoStatus.error ? ` — ${iikoStatus.error}` : ''}`}
      </div>

      <div className='grid gap-4 md:grid-cols-2 xl:grid-cols-4'>
        <Card><p className='text-slate-400'>Выручка сети</p><p className='mt-2 text-2xl font-bold'>{summary.total_revenue.toLocaleString('ru-RU')} ₽</p><CircleDollarSign className='mt-2 text-blue-400' /></Card>
        <Card><p className='text-slate-400'>Чистая прибыль</p><p className='mt-2 text-2xl font-bold text-emerald-300'>{summary.total_net_profit.toLocaleString('ru-RU')} ₽</p><TrendingUp className='mt-2 text-emerald-400' /></Card>
        <Card><p className='text-slate-400'>Списания</p><p className='mt-2 text-2xl font-bold text-orange-300'>{summary.total_write_offs.toLocaleString('ru-RU')} ₽</p><TrendingDown className='mt-2 text-orange-400' /></Card>
        <Card><p className='text-slate-400'>Критические алерты</p><p className='mt-2 text-2xl font-bold text-red-300'>{summary.critical_alerts_count}</p><AlertTriangle className='mt-2 text-red-400' /></Card>
      </div>

      <div className='mt-4 grid gap-4 lg:grid-cols-2'>
        <Card><h2 className='mb-3 text-lg font-semibold'>Выручка vs прибыль</h2><RevenueProfitChart data={chartData} /></Card>
        <Card><h2 className='mb-3 text-lg font-semibold'>Где утекают деньги</h2><SimpleBars data={losses.losses_by_category} x='category' y='amount' /></Card>
      </div>

      <div className='mt-4 grid gap-4 lg:grid-cols-2'>
        <Card>
          <h2 className='mb-3 text-lg font-semibold'>Проблемные рестораны</h2>
          <ul className='space-y-2 text-sm'>
            {profitability.worst_performers.map((r: any) => <li key={r.id} className='rounded-lg bg-slate-800 p-3'>{r.name} — маржинальность {r.margin_percent}%</li>)}
          </ul>
        </Card>
        <Card>
          <h2 className='mb-3 text-lg font-semibold'>Краткий список рисков</h2>
          <ul className='space-y-2 text-sm text-slate-300'>
            <li>• Превышение food cost по точкам с отклонениями.</li>
            <li>• Перегрузка кухонных станций в пиковые часы.</li>
            <li>• Рост закупочных цен у ключевых поставщиков.</li>
          </ul>
        </Card>
      </div>
    </AppShell>
  )
}
