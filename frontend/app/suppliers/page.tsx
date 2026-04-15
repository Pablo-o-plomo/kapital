import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

export default async function SuppliersPage() {
  const data = await apiGet<any>('/api/dashboard/suppliers')
  return (
    <AppShell>
      <div className='grid gap-4 lg:grid-cols-2'>
        <Card><h2 className='mb-3 text-lg font-semibold'>Рост цен по поставщикам</h2><SimpleBars data={data.largest_price_changes} x='supplier' y='price_change_percent' /></Card>
        <Card><h2 className='mb-3 text-lg font-semibold'>Рискованные поставщики</h2><ul className='space-y-2 text-sm'>{data.risky_suppliers.map((s: any, i: number) => <li key={i} className='rounded-lg bg-slate-800 p-3'>{s.supplier}: {s.product_name} ({s.price} ₽ vs рынок {s.market_avg_price} ₽)</li>)}</ul></Card>
      </div>
    </AppShell>
  )
}
