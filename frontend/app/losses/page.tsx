import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { LossesPie, SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

export default async function LossesPage() {
  let data: any = { losses_by_category: [], losses_by_restaurant: [], total_losses: 0 }
  let apiError = ''
  try {
    data = await apiGet<any>('/api/dashboard/losses')
  } catch {
    apiError = 'Не удалось загрузить данные потерь из backend API.'
  }

  return (
    <AppShell>
      {apiError ? <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-xs text-red-200'>{apiError}</div> : null}
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
