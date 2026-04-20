'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'

const links = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/issues', label: 'Проблемы' },
  { href: '/tasks', label: 'Задачи' },
  { href: '/prices', label: 'Цены' },
  { href: '/restaurants/1', label: 'Рестораны' },
]

export function Nav() {
  const router = useRouter()

  return (
    <div className='mb-6 flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900 p-4'>
      <div className='flex flex-wrap gap-4 text-sm text-slate-200'>
        {links.map((link) => (
          <Link key={link.href} href={link.href} className='hover:text-emerald-400'>
            {link.label}
          </Link>
        ))}
      </div>
      <button
        className='rounded bg-slate-700 px-3 py-1 text-sm hover:bg-slate-600'
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
