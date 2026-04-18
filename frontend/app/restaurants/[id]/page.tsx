'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Period = { id: number; start_date: string; end_date: string; status: string; restaurant_id: number }

export default function RestaurantPage({ params }: { params: { id: string } }) {
  const [periods, setPeriods] = useState<Period[]>([])
  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Period[]>('/periods', {}, token).then((rows) => setPeriods(rows.filter((p) => String(p.restaurant_id) === params.id)))
  }, [params.id])

  return (
    <main className='mx-auto max-w-5xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Ресторан #{params.id} — недели</h1>
      <div className='space-y-3'>
        {periods.map((p) => (
          <div key={p.id} className='card p-4'>
            <p>Период {p.start_date} — {p.end_date}</p>
            <p className='text-sm text-slate-400'>Статус: {p.status}</p>
            <Link className='text-emerald-400' href={`/periods/${p.id}`}>Открыть</Link>
          </div>
        ))}
      </div>
    </main>
  )
}
