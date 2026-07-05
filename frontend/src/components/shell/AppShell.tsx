import { motion } from 'framer-motion'
import {
  Bot,
  ChevronRight,
  Clock3,
  Compass,
  FileText,
  History,
  ImageIcon,
  Layers3,
  Mic,
  PanelLeftClose,
  PanelLeftOpen,
  PlugZap,
  Search,
  Settings,
  Sparkles,
  SunMoon,
} from 'lucide-react'
import { useMemo, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { Avatar } from '../ui/Avatar'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { Card } from '../ui/Card'
import { GlassPanel } from '../ui/GlassPanel'
import { NavigationItem } from '../ui/NavigationItem'
import { SidebarItem } from '../ui/SidebarItem'
import { Textarea } from '../ui/Textarea'
import { useAppStore } from '../../store/appStore'
import { useTheme } from '../../hooks/useTheme'

const sidebarItems = [
  { label: 'New Chat', icon: <Sparkles size={16} /> },
  { label: 'History', icon: <History size={16} /> },
  { label: 'Search', icon: <Search size={16} /> },
  { label: 'Documents', icon: <FileText size={16} /> },
  { label: 'Images', icon: <ImageIcon size={16} /> },
  { label: 'Voice', icon: <Mic size={16} /> },
  { label: 'Plugins', icon: <PlugZap size={16} /> },
  { label: 'Settings', icon: <Settings size={16} /> },
]

const topNavItems = [
  { label: 'Overview', href: '/', icon: <Compass size={15} /> },
  { label: 'Chat', href: '/chat', icon: <Bot size={15} /> },
  { label: 'Insights', href: '/insights', icon: <Layers3 size={15} /> },
]

export function AppShell() {
  const location = useLocation()
  const { sidebarOpen, toggleSidebar } = useAppStore()
  const { theme, setTheme } = useTheme()
  const [contextOpen, setContextOpen] = useState(true)

  const now = useMemo(() => new Date(), [])

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(125,211,252,0.12),_transparent_45%),linear-gradient(135deg,_#020617_0%,_#0f172a_100%)] text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-3 py-3 sm:px-4 lg:px-6">
        <GlassPanel className="flex flex-1 flex-col overflow-hidden">
          <header className="flex items-center justify-between border-b border-white/10 px-4 py-3 sm:px-6">
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleSidebar}
                className="rounded-full border-white/10 p-2"
              >
                {sidebarOpen ? <PanelLeftClose size={16} /> : <PanelLeftOpen size={16} />}
              </Button>
              <div>
                <div className="flex items-center gap-2">
                  <Sparkles size={16} className="text-sky-300" />
                  <p className="text-sm font-semibold tracking-wide text-slate-100">
                    Enigm0 Assistant
                  </p>
                </div>
                <p className="text-xs text-slate-400">Adaptive workspace</p>
              </div>
            </div>

            <div className="hidden items-center gap-2 md:flex">
              <Badge tone="accent">
                {now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </Badge>
              <Badge tone="success">Connected</Badge>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                className="rounded-full border-white/10 p-2"
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              >
                <SunMoon size={16} />
              </Button>
              <Button variant="ghost" size="sm" className="rounded-full border-white/10 p-2">
                <Settings size={16} />
              </Button>
              <Avatar initials="EA" size="md" className="ml-1" />
            </div>
          </header>

          <div className="flex flex-1 flex-col lg:flex-row">
            <motion.aside
              layout
              className={`border-r border-white/10 bg-slate-950/45 backdrop-blur-xl transition-all duration-300 ${sidebarOpen ? 'w-full lg:w-72' : 'w-0 overflow-hidden lg:w-20'}`}
            >
              <div className="flex h-full flex-col gap-4 p-3 sm:p-4">
                <Button
                  variant="primary"
                  className="justify-between rounded-[20px] px-3 py-3 text-sm"
                >
                  <span className="flex items-center gap-2">
                    <Sparkles size={15} />
                    {sidebarOpen ? 'New Chat' : 'New'}
                  </span>
                  <ChevronRight size={15} />
                </Button>

                <nav className="space-y-1.5">
                  {sidebarItems.map((item) => (
                    <SidebarItem
                      key={item.label}
                      active={item.label === 'History'}
                      icon={item.icon}
                    >
                      {sidebarOpen ? item.label : ''}
                    </SidebarItem>
                  ))}
                </nav>

                <div className="mt-auto rounded-[24px] border border-white/10 bg-slate-900/60 p-3">
                  <div className="flex items-center gap-2 text-sm text-slate-300">
                    <Clock3 size={15} className="text-sky-300" />
                    {sidebarOpen ? 'Workspace synced' : 'Synced'}
                  </div>
                  <p className="mt-2 text-xs text-slate-500">
                    Local shell ready for future AI surfaces.
                  </p>
                </div>
              </div>
            </motion.aside>

            <div className="flex min-w-0 flex-1 flex-col">
              <div className="border-b border-white/10 px-4 py-3 sm:px-6">
                <div className="flex flex-wrap items-center gap-2">
                  {topNavItems.map((item) => (
                    <NavigationItem
                      key={item.label}
                      href={item.href}
                      active={location.pathname === item.href}
                      icon={item.icon}
                    >
                      {item.label}
                    </NavigationItem>
                  ))}
                </div>
              </div>

              <div className="flex flex-1 flex-col xl:flex-row">
                <main className="flex-1 p-4 sm:p-6">
                  <div className="flex h-full flex-col gap-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium uppercase tracking-[0.3em] text-sky-300">
                          Workspace
                        </p>
                        <h1 className="text-2xl font-semibold text-slate-100">Assistant shell</h1>
                      </div>
                      <Badge tone="neutral">Layout only</Badge>
                    </div>

                    <div className="grid gap-4 lg:grid-cols-[1.4fr_0.6fr]">
                      <Card className="min-h-[220px]">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm font-medium text-slate-300">
                              Conversation canvas
                            </p>
                            <p className="text-sm text-slate-500">
                              Resilient multi-panel layout prepared for future views.
                            </p>
                          </div>
                          <Badge tone="accent">Ready</Badge>
                        </div>
                        <div className="mt-6 space-y-3">
                          <div className="h-3 w-4/5 rounded-full bg-slate-800/80" />
                          <div className="h-3 w-3/5 rounded-full bg-slate-800/80" />
                          <div className="h-3 w-2/3 rounded-full bg-slate-800/80" />
                        </div>
                      </Card>
                      <Card className="min-h-[220px]">
                        <p className="text-sm font-medium text-slate-300">Context snapshot</p>
                        <div className="mt-4 space-y-3">
                          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-3 text-sm text-slate-400">
                            Active context remains modular and isolated.
                          </div>
                          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-3 text-sm text-slate-400">
                            Flexible right rail for tools or memory.
                          </div>
                        </div>
                      </Card>
                    </div>
                  </div>
                </main>

                <motion.aside
                  layout
                  className={`border-l border-white/10 bg-slate-950/35 backdrop-blur-xl transition-all duration-300 ${contextOpen ? 'w-full xl:w-80' : 'w-0 overflow-hidden xl:w-16'}`}
                >
                  <div className="flex h-full flex-col gap-3 p-3 sm:p-4">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-semibold text-slate-200">Context</p>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="rounded-full border-white/10 p-2"
                        onClick={() => setContextOpen((open) => !open)}
                      >
                        {contextOpen ? <PanelLeftClose size={15} /> : <PanelLeftOpen size={15} />}
                      </Button>
                    </div>
                    <Card glass className="p-3">
                      <p className="text-sm font-medium text-slate-300">Session focus</p>
                      <p className="mt-2 text-sm text-slate-500">
                        Use this panel for memory, tools, or live state.
                      </p>
                    </Card>
                    <Card glass className="p-3">
                      <p className="text-sm font-medium text-slate-300">Capabilities</p>
                      <div className="mt-3 space-y-2 text-sm text-slate-500">
                        <div className="rounded-2xl border border-white/10 bg-slate-900/60 px-3 py-2">
                          Voice ready
                        </div>
                        <div className="rounded-2xl border border-white/10 bg-slate-900/60 px-3 py-2">
                          Documents ready
                        </div>
                      </div>
                    </Card>
                  </div>
                </motion.aside>
              </div>

              <div className="border-t border-white/10 bg-slate-950/40 p-4 sm:p-6">
                <Card className="p-3">
                  <div className="flex flex-col gap-3 lg:flex-row lg:items-end">
                    <div className="flex-1">
                      <Textarea
                        placeholder="Ask the assistant anything"
                        className="min-h-[90px] resize-y"
                      />
                    </div>
                    <div className="flex flex-wrap gap-2 lg:flex-col lg:items-end">
                      <Button variant="secondary">Attach</Button>
                      <Button variant="primary">Send</Button>
                    </div>
                  </div>
                  <div className="mt-3 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                    <Badge tone="accent">Multimodal</Badge>
                    <Badge tone="neutral">Keyboard ready</Badge>
                    <Badge tone="neutral">Resizable composer</Badge>
                  </div>
                  <div className="mt-3 h-2 cursor-row-resize rounded-full bg-slate-800/70" />
                </Card>
              </div>
            </div>
          </div>
        </GlassPanel>
      </div>
    </div>
  )
}
