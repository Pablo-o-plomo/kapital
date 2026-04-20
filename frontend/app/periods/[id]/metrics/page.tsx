'use client'

import { FormEvent, useEffect, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type MetricForm = {
  period_id: number
  revenue: number
  avg_check: number
  guest_count: number
  food_cost_value: number
  food_cost_percent: number
  fot_value: number
  fot_percent: number
  write_offs_value: number
  inventory_diff_value: number
  negative_stock_value: number
  comments: string
}

const numberFields: Array<keyof MetricForm> = [
  'revenue',
  'avg_check',
  'guest_count',
  'food_cost_value',
  'food_cost_percent',
  'fot_value',
  'fot_percent',
  'write_offs_value',
  'inventory_diff_value',
  'negative_stock_value',
]

export default function MetricsPage({ params }: { params: { id: string } }) {
  const [metricId, setMetricId] = useState<number | null>(null)
  const [saved, setSaved] = useState('')
  const [form, setForm] = useState<MetricForm>({
    period_id: Number(params.id),
    revenue: 0,
    avg_check: 0,
    guest_count: 0,
    food_cost_value: 0,
    food_cost_percent: 0,
    fot_value: 0,
    fot_percent: 0,
    write_offs_value: 0,
    inventory_diff_value: 0,
    negative_stock_value: 0,
    comments: '',
  })

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<any>(`/periods/${params.id}/metrics`, {}, token)
      .then((metric) => {
        setMetricId(metric.id)
        setForm({ ...form, ...metric, period_id: Number(params.id) })
      })
      .catch(() => undefined)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id])

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem('token') || ''
    const payload = { ...form }

    if (metricId) {
      await apiFetch(`/metrics/${metricId}`, { method: 'PATCH', body: JSON.stringify(payload) }, token)
      setSaved('Метрики обновлены')
      return
    }

    const created = await apiFetch<any>('/metrics', { method: 'POST', body: JSON.stringify(payload) }, token)
    setMetricId(created.id)
    setSaved('Метрики сохранены')
  }

  return (
    <main className='mx-auto max-w-5xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Метрики недели #{params.id}</h1>
      {saved && <p className='mb-4 text-emerald-400'>{saved}</p>}
      <form onSubmit={onSubmit} className='card grid gap-3 p-4 md:grid-cols-2'>
        {numberFields.map((field) => (
          <label key={field} className='text-sm'>
            <span className='mb-1 block text-slate-300'>{field}</span>
            <input
              type='number'
              step='0.01'
              className='w-full rounded border border-slate-700 bg-slate-900 p-2'
              value={form[field] as number}
              onChange={(e) => setForm((prev) => ({ ...prev, [field]: Number(e.target.value) }))}
            />
          </label>
        ))}
        <label className='md:col-span-2'>
          <span className='mb-1 block text-sm text-slate-300'>comments</span>
          <textarea
            className='h-24 w-full rounded border border-slate-700 bg-slate-900 p-2'
            value={form.comments}
            onChange={(e) => setForm((prev) => ({ ...prev, comments: e.target.value }))}
          />
        </label>
        <button type='submit' className='rounded bg-emerald-600 px-4 py-2 font-semibold hover:bg-emerald-500 md:col-span-2'>
          Сохранить метрики
        </button>
      </form>
    </main>
  )
}
