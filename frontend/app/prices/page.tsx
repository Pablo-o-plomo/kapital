'use client'

import { useEffect, useMemo, useState } from 'react'
import { Nav } from '@/components/nav'
import { apiFetch } from '@/lib/api'

type Price = { id: number; product_id: number; supplier_id: number; restaurant_id: number; price: number; price_date: string }
type Product = { id: number; name: string }
type Supplier = { id: number; name: string }
type Restaurant = { id: number; name: string }

function getStatus(change: number | null) {
  if (change === null) return { label: 'ok', color: 'text-emerald-400' }
  if (change > 10) return { label: 'red', color: 'text-rose-400' }
  if (change > 5) return { label: 'yellow', color: 'text-amber-400' }
  return { label: 'ok', color: 'text-emerald-400' }
}

export default function PricesPage() {
  const [prices, setPrices] = useState<Price[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])

  useEffect(() => {
    const token = localStorage.getItem('token') || ''
    Promise.all([
      apiFetch<Price[]>('/prices', {}, token),
      apiFetch<Product[]>('/products', {}, token),
      apiFetch<Supplier[]>('/suppliers', {}, token),
      apiFetch<Restaurant[]>('/restaurants', {}, token),
    ]).then(([priceRows, productRows, supplierRows, restaurantRows]) => {
      setPrices(priceRows)
      setProducts(productRows)
      setSuppliers(supplierRows)
      setRestaurants(restaurantRows)
    })
  }, [])

  const productsMap = useMemo(() => new Map(products.map((p) => [p.id, p.name])), [products])
  const suppliersMap = useMemo(() => new Map(suppliers.map((s) => [s.id, s.name])), [suppliers])
  const restaurantsMap = useMemo(() => new Map(restaurants.map((r) => [r.id, r.name])), [restaurants])

  const rows = useMemo(() => {
    const sorted = [...prices].sort((a, b) => {
      const keyA = `${a.restaurant_id}-${a.product_id}`
      const keyB = `${b.restaurant_id}-${b.product_id}`
      if (keyA !== keyB) return keyA.localeCompare(keyB)
      return a.price_date.localeCompare(b.price_date)
    })

    const prevByKey = new Map<string, number>()
    return sorted
      .map((price) => {
        const key = `${price.restaurant_id}-${price.product_id}`
        const prev = prevByKey.get(key)
        const change = prev && prev > 0 ? ((Number(price.price) - prev) / prev) * 100 : null
        prevByKey.set(key, Number(price.price))
        return { ...price, change }
      })
      .sort((a, b) => b.price_date.localeCompare(a.price_date))
  }, [prices])

  return (
    <main className='mx-auto max-w-7xl p-6'>
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
              <th className='p-2 text-left'>Изменение</th>
              <th className='p-2 text-left'>Статус</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const status = getStatus(row.change)
              return (
                <tr key={row.id} className='border-t border-slate-800'>
                  <td className='p-2'>{productsMap.get(row.product_id) || `#${row.product_id}`}</td>
                  <td className='p-2'>{suppliersMap.get(row.supplier_id) || `#${row.supplier_id}`}</td>
                  <td className='p-2'>{restaurantsMap.get(row.restaurant_id) || `#${row.restaurant_id}`}</td>
                  <td className='p-2'>{Number(row.price).toLocaleString()}</td>
                  <td className='p-2'>{row.price_date}</td>
                  <td className='p-2'>{row.change === null ? '—' : `${row.change.toFixed(2)}%`}</td>
                  <td className={`p-2 font-semibold ${status.color}`}>{status.label}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </main>
  )
}
