'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Task = { id: number; block_id: number; title: string; status: string; assigned_user_id?: number }
type Issue = { id: number; title: string; severity: string; status: string; block_id: number }

export default function BlockPage({ params }: { params: { id: string; blockId: string } }) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [issues, setIssues] = useState<Issue[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Task[]>('/tasks', {}, token).then((rows) => setTasks(rows.filter((t) => String(t.block_id) === params.blockId)))
    apiFetch<Issue[]>(`/periods/${params.id}/issues`, {}, token).then((rows) => setIssues(rows.filter((i) => String(i.block_id) === params.blockId)))
  }, [params.id, params.blockId])

  return (
    <main className='mx-auto max-w-6xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Блок #{params.blockId}</h1>
      <div className='grid gap-4 md:grid-cols-2'>
        <section className='card p-4'>
          <h2 className='mb-2 font-semibold'>Задачи</h2>
          {tasks.length === 0 && <p className='text-sm text-slate-400'>Задач нет</p>}
          {tasks.map((task) => (
            <p key={task.id} className='text-sm'>
              {task.title} — {task.status}
            </p>
          ))}
        </section>
        <section className='card p-4'>
          <h2 className='mb-2 font-semibold'>Проблемы</h2>
          {issues.length === 0 && <p className='text-sm text-slate-400'>Проблем нет</p>}
          {issues.map((issue) => (
            <Link key={issue.id} className='block text-sm text-emerald-400 hover:underline' href={`/issues/${issue.id}`}>
              {issue.title} — {issue.severity}/{issue.status}
            </Link>
          ))}
        </section>
      </div>
    </main>
  )
}
