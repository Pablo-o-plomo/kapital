'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Block = { id: number; name: string; code: string; status: string }
type Period = { id: number; restaurant_id: number; start_date: string; end_date: string; status: string }
type Issue = { id: number; block_id: number; severity: string; status: string }
type Task = { id: number; block_id: number; status: string }
type Metric = { revenue: number; food_cost_percent: number; fot_percent: number }

export default function PeriodPage({ params }: { params: { id: string } }) {
  const [period, setPeriod] = useState<Period | null>(null)
  const [blocks, setBlocks] = useState<Block[]>([])
  const [issues, setIssues] = useState<Issue[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [metric, setMetric] = useState<Metric | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Period>(`/periods/${params.id}`, {}, token).then(setPeriod)
    apiFetch<Block[]>(`/periods/${params.id}/blocks`, {}, token).then(setBlocks)
    apiFetch<Issue[]>(`/periods/${params.id}/issues`, {}, token).then(setIssues)
    apiFetch<Task[]>('/tasks', {}, token).then((rows) => setTasks(rows))
    apiFetch<Metric>(`/periods/${params.id}/metrics`, {}, token).then(setMetric).catch(() => setMetric(null))
  }, [params.id])

  const taskByBlock = useMemo(() => {
    const map = new Map<number, Task[]>()
    tasks.forEach((task) => {
      const list = map.get(task.block_id) || []
      list.push(task)
      map.set(task.block_id, list)
    })
    return map
  }, [tasks])

  const issuesByBlock = useMemo(() => {
    const map = new Map<number, Issue[]>()
    issues.forEach((issue) => {
      const list = map.get(issue.block_id) || []
      list.push(issue)
      map.set(issue.block_id, list)
    })
    return map
  }, [issues])

  const redIssues = issues.filter((issue) => issue.severity === 'red' && issue.status !== 'resolved').length
  const openTasks = tasks.filter((task) => task.status === 'open' || task.status === 'in_progress').length

  return (
    <main className='mx-auto max-w-7xl p-6'>
      <Nav />
      <h1 className='text-2xl font-bold'>Операционный кабинет недели #{params.id}</h1>
      {period && <p className='mb-4 text-slate-300'>Ресторан: {period.restaurant_id} · {period.start_date} — {period.end_date} · Статус: {period.status}</p>}

      <div className='mb-5 grid gap-3 md:grid-cols-4'>
        <div className='card p-3'>🔴 Red issues: <strong>{redIssues}</strong></div>
        <div className='card p-3'>📌 Open tasks: <strong>{openTasks}</strong></div>
        <div className='card p-3'>💰 Revenue: <strong>{Math.round(metric?.revenue || 0).toLocaleString()}</strong></div>
        <div className='card p-3'>Food Cost / ФОТ: <strong>{metric?.food_cost_percent || 0}% / {metric?.fot_percent || 0}%</strong></div>
      </div>

      <div className='mb-5 flex gap-3'>
        <Link href={`/periods/${params.id}/metrics`} className='rounded bg-emerald-600 px-3 py-2 text-sm font-semibold hover:bg-emerald-500'>
          Ввод метрик
        </Link>
        <Link href='/issues' className='rounded border border-slate-700 px-3 py-2 text-sm hover:border-slate-500'>
          Все проблемы
        </Link>
      </div>

      <div className='grid gap-4 md:grid-cols-2 lg:grid-cols-3'>
        {blocks.map((block) => {
          const blockIssues = issuesByBlock.get(block.id) || []
          const blockTasks = taskByBlock.get(block.id) || []
          return (
            <Link href={`/periods/${params.id}/blocks/${block.id}`} key={block.id} className='card p-4 hover:border-emerald-500'>
              <h2 className='font-semibold'>{block.name}</h2>
              <p className='text-sm text-slate-400'>Код: {block.code}</p>
              <p className='text-sm text-slate-400'>Статус: {block.status}</p>
              <p className='mt-3 text-sm'>Проблемы: {blockIssues.length}</p>
              <p className='text-sm'>Задачи: {blockTasks.length}</p>
            </Link>
          )
        })}
      </div>
    </main>
  )
}
