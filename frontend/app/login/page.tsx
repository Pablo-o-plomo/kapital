'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiFetch } from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('password123')
  const [error, setError] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const res = await apiFetch<{ access_token: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      localStorage.setItem('token', res.access_token)
      router.push('/dashboard')
    } catch (err) {
      setError('Неверные учетные данные или backend недоступен')
    }
  }

  return (
    <main className='mx-auto mt-24 max-w-md card p-6'>
      <h1 className='mb-4 text-2xl font-bold'>Вход в систему</h1>
      <form onSubmit={onSubmit} className='space-y-3'>
        <input className='w-full rounded bg-slate-800 p-2' value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' />
        <input className='w-full rounded bg-slate-800 p-2' type='password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' />
        {error && <p className='text-sm text-red-400'>{error}</p>}
        <button className='w-full rounded bg-emerald-600 p-2 font-medium'>Войти</button>
      </form>
    </main>
  )
}
