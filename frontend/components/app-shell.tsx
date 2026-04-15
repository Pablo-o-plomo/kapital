'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart3, Building2, ChefHat, ClipboardList, Factory, LogOut, Truck } from 'lucide-react'

const nav = [
  { href: '/dashboard', label: 'Дашборд', icon: BarChart3 },
  { href: '/restaurants', label: 'Рестораны', icon: Building2 },
  { href: '/suppliers', label: 'Поставщики', icon: Truck },
  { href: '/losses', label: 'Потери', icon: ClipboardList },
  { href: '/prep', label: 'Заготовки', icon: Factory },
  { href: '/kitchen', label: 'Кухня', icon: ChefHat }
]

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  return (
    <div className='min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100'>
      <div className='mx-auto flex max-w-[1400px] gap-4 p-4 md:p-6'>
        <aside className='hidden w-64 rounded-2xl border border-slate-800 bg-slate-900/80 p-5 lg:block'>
          <h1 className='mb-6 text-lg font-bold text-blue-300'>Ops Director SaaS</h1>
          <nav className='space-y-2'>
            {nav.map((item) => {
              const Icon = item.icon
              const active = pathname === item.href
              return (
                <Link key={item.href} href={item.href} className={`flex items-center gap-3 rounded-xl px-3 py-2 ${active ? 'bg-blue-500 text-white' : 'text-slate-300 hover:bg-slate-800'}`}>
                  <Icon size={16} />
                  {item.label}
                </Link>
              )
            })}
          </nav>
          <Link href='/login' className='mt-10 flex items-center gap-2 rounded-xl px-3 py-2 text-slate-300 hover:bg-slate-800'>
            <LogOut size={16} /> Выйти
          </Link>
        </aside>

        <main className='flex-1'>
          <div className='mb-4 flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-900/60 px-5 py-3'>
            <div>
              <p className='text-sm text-slate-400'>Операционный директор сети ресторанов</p>
              <p className='text-lg font-semibold'>Investor Demo MVP</p>
            </div>
            <span className='rounded-full bg-emerald-500/20 px-3 py-1 text-xs text-emerald-300'>Live demo data</span>
          </div>
          {children}
        </main>
      </div>
    </div>
  )
}
