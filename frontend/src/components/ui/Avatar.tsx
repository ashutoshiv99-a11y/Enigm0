import { cn } from '../../utils/cn'

interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string
  alt?: string
  initials?: string
  size?: 'sm' | 'md' | 'lg'
}

const sizeStyles = {
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-14 w-14 text-base',
}

export function Avatar({
  src,
  alt = 'avatar',
  initials,
  size = 'md',
  className,
  ...props
}: AvatarProps) {
  return (
    <div
      className={cn(
        'flex items-center justify-center overflow-hidden rounded-full border border-white/10 bg-slate-800/80 text-slate-100 shadow-sm',
        sizeStyles[size],
        className,
      )}
      {...props}
    >
      {src ? <img src={src} alt={alt} className="h-full w-full object-cover" /> : (initials ?? 'U')}
    </div>
  )
}
