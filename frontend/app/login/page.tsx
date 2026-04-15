'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function LoginPage() {
  const router = useRouter()
  return (
    <div className='flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,#1e3a8a,#020617)] p-4'>
      <div className='w-full max-w-md rounded-3xl border border-slate-700 bg-slate-900/90 p-8 shadow-2xl'>
        <h1 className='text-2xl font-bold'>Операционный директор</h1>
        <p className='mb-6 mt-2 text-sm text-slate-400'>Investor demo для сети ресторанов</p>
        <input placeholder='demo@restaurant.ai' className='mb-3 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3' />
        <input placeholder='••••••••' type='password' className='mb-6 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3' />
        <Button className='w-full py-3' onClick={() => router.push('/dashboard')}>Войти в систему</Button>
      </div>
    </div>
  )
}
