'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Block = { id: number; name: string; code: string; status: string }
type Period = { id: number; restaurant_id: number; start_date: string; end_date: string; status: string }

export default function PeriodPage({ params }: { params: { id: string } }) {
  const [period, setPeriod] = useState<Period | null>(null)
  const [blocks, setBlocks] = useState<Block[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Period>(`/periods/${params.id}`, {}, token).then(setPeriod)
    apiFetch<Block[]>(`/periods/${params.id}/blocks`, {}, token).then(setBlocks)
  }, [params.id])

  return (
    <main className='mx-auto max-w-6xl p-6'>
      <Nav />
      <h1 className='text-2xl font-bold'>Неделя #{params.id}</h1>
      {period && <p className='mb-4 text-slate-300'>Ресторан: {period.restaurant_id} | {period.start_date} — {period.end_date} | Статус: {period.status}</p>}
      <div className='grid gap-4 md:grid-cols-2 lg:grid-cols-3'>
        {blocks.map((b) => (
          <Link href={`/periods/${params.id}/blocks/${b.id}`} key={b.id} className='card p-4 hover:border-emerald-500'>
            <h2 className='font-semibold'>{b.name}</h2>
            <p className='text-sm text-slate-400'>Код: {b.code}</p>
            <p className='text-sm'>Статус: {b.status}</p>
          </Link>
        ))}
      </div>
    </main>
  )
}
