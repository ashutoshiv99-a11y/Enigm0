import { cn } from '../../utils/cn'

type GlassPanelProps = React.HTMLAttributes<HTMLDivElement>

export function GlassPanel({ className, children, ...props }: GlassPanelProps) {
  return (
    <div
      className={cn(
        'rounded-[28px] border border-white/10 bg-white/8 shadow-[0_24px_60px_rgba(2,6,23,0.25)] backdrop-blur-2xl transition-all duration-200 hover:-translate-y-1 hover:scale-[1.005]',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  )
}
