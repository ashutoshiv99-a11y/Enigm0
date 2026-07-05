import { AnimatePresence, motion } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import { useState } from 'react'
import { cn } from '../../utils/cn'

interface DropdownProps {
  label: string
  children: React.ReactNode
  className?: string
}

export function Dropdown({ label, children, className }: DropdownProps) {
  const [open, setOpen] = useState(false)

  return (
    <div className="relative inline-block">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className={cn(
          'inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-2 text-sm text-slate-100 shadow-sm backdrop-blur-xl',
          className,
        )}
      >
        {label}
        <ChevronDown size={14} />
      </button>
      <AnimatePresence>
        {open ? (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 6 }}
            className="absolute right-0 z-20 mt-2 min-w-44 rounded-2xl border border-white/10 bg-slate-950/95 p-2 shadow-[0_20px_50px_rgba(2,6,23,0.38)]"
          >
            {children}
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  )
}
