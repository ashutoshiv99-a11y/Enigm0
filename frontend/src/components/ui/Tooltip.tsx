import { AnimatePresence, motion } from 'framer-motion'
import { useId, useState } from 'react'

interface TooltipProps {
  label: string
  children: React.ReactNode
}

export function Tooltip({ label, children }: TooltipProps) {
  const [visible, setVisible] = useState(false)
  const id = useId()

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      <div id={id}>{children}</div>
      <AnimatePresence>
        {visible ? (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className="absolute left-1/2 top-full z-20 mt-2 -translate-x-1/2 rounded-full border border-white/10 bg-slate-950/90 px-3 py-1 text-xs text-slate-200 shadow-lg"
          >
            {label}
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  )
}
