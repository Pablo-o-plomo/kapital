'use client'

import Link from 'next/link'
import { useEffect, useMemo, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Issue = {
  id: number
  period_id: number
  type: string
  title: string
  severity: 'green' | 'yellow' | 'red'
  status: 'open' | 'in_progress' | 'resolved'
}

type Period = { id: number; restaurant_id: number }
type Restaurant = { id: number; name: string }

const severityClass: Record<string, string> = {
  green: 'text-emerald-400',
  yellow: 'text-amber-400',
  red: 'text-rose-400',
}

export default function IssuesPage() {
  const [issues, setIssues] = useState<Issue[]>([])
  const [periods, setPeriods] = useState<Period[]>([])
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])

  const [status, setStatus] = useState('all')
  const [severity, setSeverity] = useState('all')
  const [restaurantId, setRestaurantId] = useState('all')

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    Promise.all([
      apiFetch<Issue[]>('/issues', {}, token),
      apiFetch<Period[]>('/periods', {}, token),
      apiFetch<Restaurant[]>('/restaurants', {}, token),
    ]).then(([issuesRows, periodRows, restaurantRows]) => {
      setIssues(issuesRows)
      setPeriods(periodRows)
      setRestaurants(restaurantRows)
    })
  }, [])

  const periodRestaurantMap = useMemo(() => new Map(periods.map((p) => [p.id, p.restaurant_id])), [periods])
  const restaurantMap = useMemo(() => new Map(restaurants.map((r) => [r.id, r.name])), [restaurants])

  const filtered = useMemo(() => {
    return issues.filter((issue) => {
      const restId = periodRestaurantMap.get(issue.period_id)
      if (status !== 'all' && issue.status !== status) return false
      if (severity !== 'all' && issue.severity !== severity) return false
      if (restaurantId !== 'all' && String(restId) !== restaurantId) return false
      return true
    })
  }, [issues, periodRestaurantMap, restaurantId, severity, status])

  return (
    <main className='mx-auto max-w-7xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Проблемы и отклонения</h1>

      <div className='mb-4 grid gap-3 rounded-xl border border-slate-800 bg-slate-900 p-4 md:grid-cols-3'>
        <select className='rounded bg-slate-800 p-2' value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value='all'>Все статусы</option>
          <option value='open'>open</option>
          <option value='in_progress'>in_progress</option>
          <option value='resolved'>resolved</option>
        </select>
        <select className='rounded bg-slate-800 p-2' value={severity} onChange={(e) => setSeverity(e.target.value)}>
          <option value='all'>Все уровни</option>
          <option value='green'>green</option>
          <option value='yellow'>yellow</option>
          <option value='red'>red</option>
        </select>
        <select className='rounded bg-slate-800 p-2' value={restaurantId} onChange={(e) => setRestaurantId(e.target.value)}>
          <option value='all'>Все рестораны</option>
          {restaurants.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
      </div>

      <div className='card overflow-auto'>
        <table className='w-full text-sm'>
          <thead className='bg-slate-800'>
            <tr>
              <th className='p-2 text-left'>Название</th>
              <th className='p-2 text-left'>Тип</th>
              <th className='p-2 text-left'>Серьезность</th>
              <th className='p-2 text-left'>Статус</th>
              <th className='p-2 text-left'>Ресторан</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((issue) => (
              <tr key={issue.id} className='border-t border-slate-800'>
                <td className='p-2'>
                  <Link href={`/issues/${issue.id}`} className='text-emerald-400 hover:underline'>
                    {issue.title}
                  </Link>
                </td>
                <td className='p-2'>{issue.type}</td>
                <td className={`p-2 font-semibold ${severityClass[issue.severity] || ''}`}>{issue.severity}</td>
                <td className='p-2'>{issue.status}</td>
                <td className='p-2'>{restaurantMap.get(periodRestaurantMap.get(issue.period_id) || 0) || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
