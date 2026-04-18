'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Summary = {
  restaurant_id: number
  restaurant_name: string
  period_id: number
  period_status: string
  red_issues: number
  open_tasks: number
  revenue: number
  food_cost_percent: number
  fot_percent: number
}

export default function DashboardPage() {
  const [items, setItems] = useState<Summary[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<{ restaurants: Summary[] }>('/dashboard/summary', {}, token).then((d) => setItems(d.restaurants)).catch(() => setItems([]))
  }, [])

  return (
    <main className='mx-auto max-w-6xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Dashboard</h1>
      <div className='grid gap-4 md:grid-cols-2 xl:grid-cols-3'>
        {items.map((item) => (
          <div key={item.restaurant_id} className='card p-4'>
            <h2 className='text-lg font-semibold'>{item.restaurant_name}</h2>
            <p className='text-sm text-slate-400'>Неделя #{item.period_id} · {item.period_status}</p>
            <p className='mt-2 text-sm'>🔴 Проблемы: {item.red_issues}</p>
            <p className='text-sm'>📌 Открытые задачи: {item.open_tasks}</p>
            <p className='text-sm'>💰 Выручка: {Math.round(item.revenue).toLocaleString()}</p>
            <p className='text-sm'>Food Cost: {item.food_cost_percent}%</p>
            <p className='text-sm'>ФОТ: {item.fot_percent}%</p>
            <Link className='mt-3 inline-block text-emerald-400' href={`/periods/${item.period_id}`}>Открыть неделю</Link>
          </div>
        ))}
      </div>
    </main>
  )
}
