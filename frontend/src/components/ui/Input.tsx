import { forwardRef } from 'react'
import { cn } from '../../utils/cn'

type InputProps = React.InputHTMLAttributes<HTMLInputElement>

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { className, ...props },
  ref,
) {
  return (
    <input
      ref={ref}
      className={cn(
        'w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-sky-400/40 focus:ring-2 focus:ring-sky-400/20',
        className,
      )}
      {...props}
    />
  )
})
