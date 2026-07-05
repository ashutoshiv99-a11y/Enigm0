import { cn } from '../../utils/cn'

interface NavigationItemProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  active?: boolean
  icon?: React.ReactNode
}

export function NavigationItem({
  active = false,
  icon,
  children,
  className,
  ...props
}: NavigationItemProps) {
  return (
    <a
      className={cn(
        'flex items-center gap-3 rounded-2xl px-3 py-2 text-sm transition hover:-translate-y-0.5 hover:scale-[1.01]',
        active
          ? 'bg-sky-400/10 text-sky-100 shadow-[0_10px_30px_rgba(56,189,248,0.08)]'
          : 'text-slate-400 hover:bg-slate-800/70 hover:text-slate-200',
        className,
      )}
      {...props}
    >
      {icon ? <span className="shrink-0">{icon}</span> : null}
      <span>{children}</span>
    </a>
  )
}
