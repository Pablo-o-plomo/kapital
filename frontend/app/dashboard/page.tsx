import { AlertTriangle, CircleDollarSign, TrendingDown, TrendingUp } from 'lucide-react'

import { AppShell } from '@/components/app-shell'
import { RevenueProfitChart, SimpleBars } from '@/components/charts'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

const summaryFallback = {
  total_revenue: 55900000,
  total_net_profit: 7860000,
  total_write_offs: 2720000,
  critical_alerts_count: 3
}

const profitabilityFallback = {
  restaurant_profitability_table: [
    { id: 1, city: 'Москва', name: 'Москва / Авиапарк', monthly_revenue: 14200000, net_profit: 2960000, margin_percent: 20.8 },
    { id: 2, city: 'Ростов-на-Дону', name: 'Ростов-на-Дону', monthly_revenue: 8600000, net_profit: 980000, margin_percent: 11.4 },
    { id: 3, city: 'Южно-Сахалинск', name: 'Южно-Сахалинск', monthly_revenue: 12300000, net_profit: 1040000, margin_percent: 8.5 },
    { id: 4, city: 'Сочи', name: 'Сочи', monthly_revenue: 9700000, net_profit: 1670000, margin_percent: 17.2 },
    { id: 5, city: 'Санкт-Петербург', name: 'Санкт-Петербург', monthly_revenue: 11100000, net_profit: 1210000, margin_percent: 10.9 }
  ],
  worst_performers: [
    { id: 3, name: 'Южно-Сахалинск', margin_percent: 8.5 },
    { id: 5, name: 'Санкт-Петербург', margin_percent: 10.9 },
    { id: 2, name: 'Ростов-на-Дону', margin_percent: 11.4 }
  ]
}

const iikoFallback = { connected: false, organizations_count: 0, error: 'IIKO_API_LOGIN is not configured' }

const lossesFallback = {
  losses_by_category: [
    { category: 'порча', amount: 480000 },
    { category: 'брак', amount: 360000 },
    { category: 'персонал', amount: 520000 },
    { category: 'комплименты', amount: 240000 }
  ]
}

export default async function DashboardPage() {
  const [summary, profitability, losses, iikoStatus] = await Promise.all([
    apiGet('/api/dashboard/summary', summaryFallback),
    apiGet('/api/dashboard/profitability', profitabilityFallback),
    apiGet('/api/dashboard/losses', lossesFallback),
    apiGet('/api/integrations/iiko/status', iikoFallback)
  ])

  const chartData = profitability.restaurant_profitability_table.map((r: any) => ({ name: r.city, revenue: r.monthly_revenue, profit: r.net_profit }))

  return (
    <AppShell>
      <div className='mb-3 rounded-xl border border-amber-600/30 bg-amber-500/10 px-4 py-2 text-xs text-amber-200'>
        Если backend временно недоступен, отображаются встроенные демо-данные.
      </div>

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
            <li>• Превышение food cost в Южно-Сахалинске.</li>
            <li>• Перегруз станции экспедиции в 2 точках.</li>
            <li>• Рост закупочных цен у ключевых поставщиков.</li>
          </ul>
        </Card>
      </div>
    </AppShell>
  )
}
