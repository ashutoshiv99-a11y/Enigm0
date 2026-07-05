import { motion } from 'framer-motion'

export function LoadingSpinner({ size = 20 }: { size?: number }) {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ repeat: Number.POSITIVE_INFINITY, duration: 1, ease: 'linear' }}
      className="rounded-full border-2 border-slate-700 border-t-sky-400"
      style={{ width: size, height: size }}
    />
  )
}
