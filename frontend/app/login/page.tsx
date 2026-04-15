'use client'

import { FormEvent, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

const DEMO_LOGIN = process.env.NEXT_PUBLIC_DEMO_LOGIN || 'demo@restaurant.ai'
const DEMO_PASSWORD = process.env.NEXT_PUBLIC_DEMO_PASSWORD || 'OpsDirector2026!'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState(DEMO_LOGIN)
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const credentialsHint = useMemo(
    () => `Логин: ${DEMO_LOGIN} · Пароль: ${DEMO_PASSWORD}`,
    []
  )

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (email.trim() !== DEMO_LOGIN || password !== DEMO_PASSWORD) {
      setError('Неверный логин или пароль. Используйте демо-доступ ниже.')
      return
    }

    document.cookie = 'ops_demo_auth=1; Path=/; Max-Age=86400; SameSite=Lax'
    router.push('/dashboard')
  }

  return (
    <div className='flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,#1e3a8a,#020617)] p-4'>
      <div className='w-full max-w-md rounded-3xl border border-slate-700 bg-slate-900/90 p-8 shadow-2xl'>
        <h1 className='text-2xl font-bold'>Операционный директор</h1>
        <p className='mb-2 mt-2 text-sm text-slate-400'>Investor demo для сети ресторанов</p>
        <p className='mb-6 rounded-lg bg-blue-500/10 px-3 py-2 text-xs text-blue-200'>{credentialsHint}</p>

        <form onSubmit={handleSubmit} className='space-y-3'>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder='demo@restaurant.ai'
            className='w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3'
          />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder='Введите пароль'
            type='password'
            className='w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3'
          />
          {error ? <p className='text-sm text-red-300'>{error}</p> : null}
          <Button type='submit' className='w-full py-3'>
            Войти в систему
          </Button>
        </form>
      </div>
    </div>
  )
}
