import { AnimatePresence, motion } from 'framer-motion'
import { X } from 'lucide-react'
import { cn } from '../../utils/cn'

interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  className?: string
}

export function Modal({ open, onClose, title, children, className }: ModalProps) {
  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4 backdrop-blur"
          onClick={onClose}
        >
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.98 }}
            transition={{ duration: 0.2 }}
            className={cn(
              'w-full max-w-lg rounded-[28px] border border-white/10 bg-slate-900/90 p-6 shadow-[0_24px_80px_rgba(2,6,23,0.45)] backdrop-blur-xl',
              className,
            )}
            onClick={(event) => event.stopPropagation()}
          >
            {title ? (
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
                <button
                  type="button"
                  onClick={onClose}
                  className="rounded-full border border-white/10 p-2 text-slate-400 transition hover:bg-slate-800 hover:text-slate-100"
                >
                  <X size={16} />
                </button>
              </div>
            ) : null}
            {children}
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  )
}
