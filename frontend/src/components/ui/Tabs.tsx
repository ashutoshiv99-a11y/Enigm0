import { motion } from 'framer-motion'
import { useState } from 'react'
import { cn } from '../../utils/cn'

interface TabItem {
  id: string
  label: string
}

interface TabsProps {
  items: TabItem[]
  defaultValue?: string
  onChange?: (value: string) => void
}

export function Tabs({ items, defaultValue, onChange }: TabsProps) {
  const [active, setActive] = useState(defaultValue ?? items[0]?.id)

  return (
    <div className="flex gap-2 rounded-full border border-white/10 bg-slate-950/70 p-1.5">
      {items.map((item) => {
        const isActive = active === item.id
        return (
          <button
            key={item.id}
            type="button"
            onClick={() => {
              setActive(item.id)
              onChange?.(item.id)
            }}
            className={cn(
              'relative rounded-full px-4 py-2 text-sm text-slate-300 transition',
              isActive && 'text-slate-100',
            )}
          >
            {isActive ? (
              <motion.span
                layoutId="tabs-active"
                className="absolute inset-0 rounded-full bg-sky-400/15"
              />
            ) : null}
            <span className="relative z-10">{item.label}</span>
          </button>
        )
      })}
    </div>
  )
}
