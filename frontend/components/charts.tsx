'use client'

import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from 'recharts'

const COLORS = ['#3B82F6', '#8B5CF6', '#14B8A6', '#F97316', '#EF4444', '#EAB308']

export function RevenueProfitChart({ data }: { data: Array<{ name: string; revenue: number; profit: number }> }) {
  return <div className='h-72 w-full'><ResponsiveContainer><LineChart data={data}><CartesianGrid strokeDasharray='3 3' stroke='#334155' /><XAxis dataKey='name' stroke='#94a3b8' /><YAxis stroke='#94a3b8' /><Tooltip /><Legend /><Line type='monotone' dataKey='revenue' stroke='#3B82F6' /><Line type='monotone' dataKey='profit' stroke='#22C55E' /></LineChart></ResponsiveContainer></div>
}

export function LossesPie({ data }: { data: Array<{ category: string; amount: number }> }) {
  return <div className='h-72 w-full'><ResponsiveContainer><PieChart><Pie data={data} dataKey='amount' nameKey='category' outerRadius={100} label>{data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer></div>
}

export function SimpleBars({ data, x, y }: { data: Array<Record<string, string | number>>; x: string; y: string }) {
  return <div className='h-72 w-full'><ResponsiveContainer><BarChart data={data}><CartesianGrid strokeDasharray='3 3' stroke='#334155' /><XAxis dataKey={x} stroke='#94a3b8' /><YAxis stroke='#94a3b8' /><Tooltip /><Bar dataKey={y} fill='#8B5CF6' /></BarChart></ResponsiveContainer></div>
}
