import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Ops Director MVP',
  description: 'Операционная система управления сетью ресторанов'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='ru'>
      <body>{children}</body>
    </html>
  )
}
