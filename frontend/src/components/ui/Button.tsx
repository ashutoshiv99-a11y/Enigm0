import { forwardRef } from 'react'
import { cn } from '../../utils/cn'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

const buttonStyles = {
  primary:
    'border border-sky-400/30 bg-sky-400/15 text-sky-100 shadow-[0_10px_30px_rgba(56,189,248,0.12)] hover:bg-sky-400/25',
  secondary: 'border border-slate-700/80 bg-slate-900/70 text-slate-200 hover:bg-slate-800/80',
  ghost: 'border border-transparent bg-transparent text-slate-300 hover:bg-slate-800/60',
}

const sizeStyles = {
  sm: 'px-3 py-2 text-sm',
  md: 'px-4 py-2.5 text-sm',
  lg: 'px-5 py-3 text-base',
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { className, variant = 'primary', size = 'md', isLoading = false, children, disabled, ...props },
  ref,
) {
  return (
    <button
      ref={ref}
      type={props.type ?? 'button'}
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-2xl font-medium transition-all duration-200 hover:-translate-y-0.5 hover:scale-[1.01] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60',
        buttonStyles[variant],
        sizeStyles[size],
        className,
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
      ) : null}
      <span>{children}</span>
    </button>
  )
})
