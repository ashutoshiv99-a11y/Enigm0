import { cn } from '../../utils/cn'

interface SkeletonLoaderProps {
  className?: string
}

export function SkeletonLoader({ className }: SkeletonLoaderProps) {
  return <div className={cn('animate-pulse rounded-2xl bg-slate-800/70', className)} />
}
