'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function Nav() {
  const router = useRouter()
  return (
    <div className='mb-6 flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900 p-4'>
      <div className='flex gap-4 text-sm'>
        <Link href='/dashboard'>Dashboard</Link>
        <Link href='/restaurants/1'>Ресторан</Link>
        <Link href='/prices'>Закупочные цены</Link>
      </div>
      <button
        className='rounded bg-slate-700 px-3 py-1 text-sm'
        onClick={() => {
          localStorage.removeItem('token')
          router.push('/login')
        }}
      >
        Выход
      </button>
    </div>
  )
}
