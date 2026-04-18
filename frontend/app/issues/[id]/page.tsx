'use client'

import { useEffect, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Issue = { id: number; title: string; description: string; severity: string; status: string }
type Analysis = { reason: string; solution: string; result: string; assigned_user_id?: number; deadline?: string }

export default function IssuePage({ params }: { params: { id: string } }) {
  const [issue, setIssue] = useState<Issue | null>(null)
  const [analysis, setAnalysis] = useState<Analysis | null>(null)

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Issue>(`/issues/${params.id}`, {}, token).then(setIssue)
    apiFetch<Analysis>(`/issues/${params.id}/analysis`, {}, token).then(setAnalysis).catch(() => setAnalysis(null))
  }, [params.id])

  return (
    <main className='mx-auto max-w-4xl p-6'>
      <Nav />
      {issue && (
        <div className='card p-5'>
          <h1 className='text-2xl font-bold'>{issue.title}</h1>
          <p className='mt-2 text-slate-300'>{issue.description}</p>
          <p className='mt-2'>Severity: {issue.severity}</p>
          <p>Status: {issue.status}</p>
          <hr className='my-4 border-slate-700' />
          <h2 className='font-semibold'>Разбор причин</h2>
          <p>Reason: {analysis?.reason || '—'}</p>
          <p>Solution: {analysis?.solution || '—'}</p>
          <p>Result: {analysis?.result || '—'}</p>
          <p>Ответственный: {analysis?.assigned_user_id || '—'}</p>
          <p>Deadline: {analysis?.deadline || '—'}</p>
        </div>
      )}
    </main>
  )
}
