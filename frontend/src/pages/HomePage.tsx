import { motion } from 'framer-motion'
import { Bot, ShieldCheck, Sparkles } from 'lucide-react'

export function HomePage() {
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
      <div className="space-y-2">
        <p className="text-sm font-medium uppercase tracking-[0.3em] text-cyan-400">
          Frontend foundation
        </p>
        <h1 className="text-3xl font-semibold">A scalable shell for the Enigm0 AI experience</h1>
        <p className="max-w-2xl text-slate-400">
          This foundation keeps the existing Python backend untouched while offering a modular React
          structure for future chat, insights, and automation surfaces.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
          <Bot className="mb-3 text-cyan-400" />
          <h2 className="font-semibold">AI-first shell</h2>
          <p className="mt-2 text-sm text-slate-400">
            Prepared for command-driven, conversational workflows.
          </p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
          <Sparkles className="mb-3 text-fuchsia-400" />
          <h2 className="font-semibold">Extensible architecture</h2>
          <p className="mt-2 text-sm text-slate-400">
            Features, hooks, services, and store are separated for growth.
          </p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-5">
          <ShieldCheck className="mb-3 text-emerald-400" />
          <h2 className="font-semibold">Typed and validated</h2>
          <p className="mt-2 text-sm text-slate-400">
            TypeScript, routing, and environment configuration are in place.
          </p>
        </div>
      </div>
    </motion.div>
  )
}
