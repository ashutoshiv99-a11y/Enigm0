import { cn } from '../../utils/cn'

interface SidebarItemProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  active?: boolean
  icon?: React.ReactNode
}

export function SidebarItem({
  active = false,
  icon,
  children,
  className,
  ...props
}: SidebarItemProps) {
  return (
    <button
      type="button"
      className={cn(
        'flex w-full items-center gap-3 rounded-2xl border px-3 py-2.5 text-left text-sm transition hover:-translate-y-0.5 hover:scale-[1.01]',
        active
          ? 'border-sky-400/20 bg-sky-400/10 text-sky-100 shadow-[0_10px_30px_rgba(56,189,248,0.12)]'
          : 'border-transparent bg-transparent text-slate-300 hover:border-white/10 hover:bg-slate-800/70',
        className,
      )}
      {...props}
    >
      {icon ? <span className="shrink-0">{icon}</span> : null}
      <span>{children}</span>
    </button>
  )
}
