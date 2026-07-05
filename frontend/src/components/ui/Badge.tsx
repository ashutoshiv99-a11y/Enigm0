import { cn } from '../../utils/cn'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: 'neutral' | 'accent' | 'success' | 'warning'
}

const toneStyles = {
  neutral: 'border-white/10 bg-slate-800/80 text-slate-300',
  accent: 'border-sky-400/20 bg-sky-400/10 text-sky-200',
  success: 'border-emerald-400/20 bg-emerald-400/10 text-emerald-200',
  warning: 'border-amber-400/20 bg-amber-400/10 text-amber-200',
}

export function Badge({ tone = 'neutral', className, children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full border px-2.5 py-1 text-xs font-medium',
        toneStyles[tone],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  )
}
