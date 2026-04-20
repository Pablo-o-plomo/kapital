'use client'

import { useEffect, useMemo, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Task = {
  id: number
  block_id: number
  title: string
  description: string
  status: 'open' | 'in_progress' | 'done' | 'canceled'
  assigned_user_id?: number
  deadline?: string
}

type User = { id: number; full_name: string }

const statusClass: Record<string, string> = {
  open: 'text-rose-400',
  in_progress: 'text-amber-400',
  done: 'text-emerald-400',
  canceled: 'text-slate-400',
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [status, setStatus] = useState('all')

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    Promise.all([apiFetch<Task[]>('/tasks', {}, token), apiFetch<User[]>('/users', {}, token).catch(() => [])]).then(([taskRows, userRows]) => {
      setTasks(taskRows)
      setUsers(userRows)
    })
  }, [])

  const userMap = useMemo(() => new Map(users.map((u) => [u.id, u.full_name])), [users])
  const filtered = useMemo(() => tasks.filter((t) => status === 'all' || t.status === status), [tasks, status])

  return (
    <main className='mx-auto max-w-7xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Задачи</h1>
      <div className='mb-4'>
        <select className='rounded bg-slate-800 p-2' value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value='all'>Все статусы</option>
          <option value='open'>open</option>
          <option value='in_progress'>in_progress</option>
          <option value='done'>done</option>
          <option value='canceled'>canceled</option>
        </select>
      </div>
      <div className='card overflow-auto'>
        <table className='w-full text-sm'>
          <thead className='bg-slate-800'>
            <tr>
              <th className='p-2 text-left'>Заголовок</th>
              <th className='p-2 text-left'>Статус</th>
              <th className='p-2 text-left'>Дедлайн</th>
              <th className='p-2 text-left'>Ответственный</th>
              <th className='p-2 text-left'>Блок</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((task) => (
              <tr key={task.id} className='border-t border-slate-800'>
                <td className='p-2'>{task.title}</td>
                <td className={`p-2 font-semibold ${statusClass[task.status] || ''}`}>{task.status}</td>
                <td className='p-2'>{task.deadline || '—'}</td>
                <td className='p-2'>{(task.assigned_user_id && userMap.get(task.assigned_user_id)) || task.assigned_user_id || '—'}</td>
                <td className='p-2'>#{task.block_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
