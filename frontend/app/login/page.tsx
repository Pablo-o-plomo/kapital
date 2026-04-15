'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload?.detail || 'Неверный логин или пароль')
      }
      document.cookie = `ops_token=${payload.access_token}; Path=/; Max-Age=43200; SameSite=Lax`
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка входа')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,#1e3a8a,#020617)] p-4'>
      <div className='w-full max-w-md rounded-3xl border border-slate-700 bg-slate-900/90 p-8 shadow-2xl'>
        <h1 className='text-2xl font-bold'>Kapital — Операционный директор</h1>
        <p className='mb-6 mt-2 text-sm text-slate-400'>Рабочая авторизация через backend API</p>

        <form onSubmit={handleSubmit} className='space-y-3'>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder='Ваш логин'
            className='w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3'
          />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder='Ваш пароль'
            type='password'
            className='w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3'
          />
          {error ? <p className='text-sm text-red-300'>{error}</p> : null}
          <Button type='submit' className='w-full py-3' disabled={loading}>
            {loading ? 'Проверка...' : 'Войти в систему'}
          </Button>
        </form>
      </div>
    </div>
  )
}
