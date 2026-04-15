import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

export default async function PrepPage() {
  let data: any = { prep_items: [] }
  let apiError = ''
  try {
    data = await apiGet<any>('/api/dashboard/prep')
  } catch {
    apiError = 'Не удалось загрузить данные заготовок из backend API.'
  }

  return (
    <AppShell>
      {apiError ? <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-xs text-red-200'>{apiError}</div> : null}
      <Card>
        <h2 className='mb-4 text-lg font-semibold'>Заготовки и риск перепроизводства</h2>
        <div className='overflow-x-auto'>
          <table className='w-full text-sm'>
            <thead><tr className='text-slate-400'><th>Позиция</th><th>Срок жизни</th><th>Остаток</th><th>Продажи</th><th>Рекомендация</th><th>Риск</th></tr></thead>
            <tbody>{data.prep_items.map((i: any) => <tr key={i.id} className='border-t border-slate-800'><td className='py-2'>{i.item_name}</td><td>{i.shelf_life_hours} ч</td><td>{i.current_stock}</td><td>{i.avg_sales_per_lifetime}</td><td>{i.recommended_prep}</td><td className={i.overproduction_risk>70?'text-red-300':'text-emerald-300'}>{i.overproduction_risk}%</td></tr>)}</tbody>
          </table>
        </div>
      </Card>
    </AppShell>
  )
}
