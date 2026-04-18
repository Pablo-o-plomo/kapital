'use client'

import { useEffect, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Price = { id: number; product_id: number; supplier_id: number; restaurant_id: number; price: number; price_date: string }

export default function PricesPage() {
  const [prices, setPrices] = useState<Price[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    apiFetch<Price[]>('/prices', {}, token).then(setPrices)
  }, [])

  return (
    <main className='mx-auto max-w-6xl p-6'>
      <Nav />
      <h1 className='mb-4 text-2xl font-bold'>Закупочные цены</h1>
      <div className='card overflow-auto'>
        <table className='w-full text-sm'>
          <thead className='bg-slate-800'>
            <tr>
              <th className='p-2 text-left'>Продукт</th>
              <th className='p-2 text-left'>Поставщик</th>
              <th className='p-2 text-left'>Ресторан</th>
              <th className='p-2 text-left'>Цена</th>
              <th className='p-2 text-left'>Дата</th>
            </tr>
          </thead>
          <tbody>
            {prices.map((p) => (
              <tr key={p.id} className='border-t border-slate-800'>
                <td className='p-2'>{p.product_id}</td>
                <td className='p-2'>{p.supplier_id}</td>
                <td className='p-2'>{p.restaurant_id}</td>
                <td className='p-2'>{p.price}</td>
                <td className='p-2'>{p.price_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
