import { cn } from '../../utils/cn'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glass?: boolean
}

export function Card({ className, glass = true, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-[24px] border border-white/10 bg-slate-900/70 p-5 shadow-[0_18px_50px_rgba(2,6,23,0.28)] backdrop-blur-xl transition-all duration-200 hover:-translate-y-1 hover:scale-[1.01]',
        glass && 'bg-white/8',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  )
}
