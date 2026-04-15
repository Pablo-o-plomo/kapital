import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { LossesPie, SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

const fallback = {
  losses_by_category: [
    { category: 'порча', amount: 480000 },
    { category: 'брак', amount: 360000 },
    { category: 'персонал', amount: 520000 },
    { category: 'комплименты', amount: 240000 }
  ],
  losses_by_restaurant: [
    { restaurant: 'Южно-Сахалинск', amount: 760000 },
    { restaurant: 'Санкт-Петербург', amount: 640000 },
    { restaurant: 'Ростов-на-Дону', amount: 510000 }
  ],
  total_losses: 2720000
}

export default async function LossesPage() {
  const data = await apiGet<any>('/api/dashboard/losses', fallback)
  return (
    <AppShell>
      <div className='grid gap-4 lg:grid-cols-2'>
        <Card><h2 className='mb-3 text-lg font-semibold'>Потери по категориям</h2><LossesPie data={data.losses_by_category} /></Card>
        <Card><h2 className='mb-3 text-lg font-semibold'>Потери по ресторанам</h2><SimpleBars data={data.losses_by_restaurant} x='restaurant' y='amount' /></Card>
      </div>
      <Card className='mt-4'>
        <h2 className='mb-2 text-lg font-semibold'>Итого потерь: {data.total_losses.toLocaleString('ru-RU')} ₽</h2>
        <p className='text-slate-300'>Основные утечки: порча, ошибки персонала и инвентаризация минус.</p>
      </Card>
    </AppShell>
  )
}
