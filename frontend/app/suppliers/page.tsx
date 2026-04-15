import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { SimpleBars } from '@/components/charts'
import { apiGet } from '@/lib/api'

const fallback = {
  largest_price_changes: [
    { supplier: 'OceanLine', price_change_percent: 18.4 },
    { supplier: 'ProteinHub', price_change_percent: 12.2 },
    { supplier: 'FreshNorth', price_change_percent: 9.6 }
  ],
  risky_suppliers: [
    { supplier: 'OceanLine', product_name: 'Лосось охлажденный', price: 1480, market_avg_price: 1290 },
    { supplier: 'ProteinHub', product_name: 'Говядина', price: 870, market_avg_price: 790 }
  ]
}

export default async function SuppliersPage() {
  const data = await apiGet<any>('/api/dashboard/suppliers', fallback)
  return (
    <AppShell>
      <div className='grid gap-4 lg:grid-cols-2'>
        <Card><h2 className='mb-3 text-lg font-semibold'>Рост цен по поставщикам</h2><SimpleBars data={data.largest_price_changes} x='supplier' y='price_change_percent' /></Card>
        <Card><h2 className='mb-3 text-lg font-semibold'>Рискованные поставщики</h2><ul className='space-y-2 text-sm'>{data.risky_suppliers.map((s: any, i: number) => <li key={i} className='rounded-lg bg-slate-800 p-3'>{s.supplier}: {s.product_name} ({s.price} ₽ vs рынок {s.market_avg_price} ₽)</li>)}</ul></Card>
      </div>
    </AppShell>
  )
}
