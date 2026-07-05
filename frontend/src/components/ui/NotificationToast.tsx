import { AnimatePresence, motion } from 'framer-motion'
import { CheckCircle2, X } from 'lucide-react'
import { cn } from '../../utils/cn'

interface NotificationToastProps {
  title: string
  description?: string
  open: boolean
  onClose: () => void
  tone?: 'info' | 'success' | 'warning'
}

const toneStyles = {
  info: 'border-sky-400/20 bg-sky-400/10 text-sky-100',
  success: 'border-emerald-400/20 bg-emerald-400/10 text-emerald-100',
  warning: 'border-amber-400/20 bg-amber-400/10 text-amber-100',
}

export function NotificationToast({
  title,
  description,
  open,
  onClose,
  tone = 'info',
}: NotificationToastProps) {
  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className={cn(
            'fixed bottom-6 right-6 z-50 flex max-w-sm items-start gap-3 rounded-[24px] border p-4 shadow-[0_20px_60px_rgba(2,6,23,0.35)] backdrop-blur-xl',
            toneStyles[tone],
          )}
        >
          <CheckCircle2 className="mt-0.5 shrink-0" size={18} />
          <div className="flex-1">
            <p className="text-sm font-medium">{title}</p>
            {description ? <p className="mt-1 text-sm text-slate-300/90">{description}</p> : null}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full p-1 transition hover:bg-white/10"
          >
            <X size={14} />
          </button>
        </motion.div>
      ) : null}
    </AnimatePresence>
  )
}
