import { cn } from '@/lib/utils'

export function Button({ className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn('rounded-xl bg-blue-500 px-4 py-2 font-semibold text-white transition hover:bg-blue-400', className)}
      {...props}
    >
      {children}
    </button>
  )
}
