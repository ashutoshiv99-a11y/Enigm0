import { cn } from '../../utils/cn'

interface ProgressBarProps {
  value: number
  max?: number
  className?: string
}

export function ProgressBar({ value, max = 100, className }: ProgressBarProps) {
  const percent = Math.min(100, Math.max(0, (value / max) * 100))

  return (
    <div className={cn('h-2 w-full overflow-hidden rounded-full bg-slate-800/80', className)}>
      <div
        className="h-full rounded-full bg-gradient-to-r from-sky-400/80 to-cyan-300/80 transition-all"
        style={{ width: `${percent}%` }}
      />
    </div>
  )
}
