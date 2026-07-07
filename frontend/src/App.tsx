import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { create } from 'zustand';
import {
  MessageSquare, History, Search, FileText, Image as ImageIcon, 
  Mic, Settings, Puzzle, Sun, Moon, Wifi, PanelLeftClose, 
  PanelLeftOpen, PanelRightClose, PanelRightOpen, Send, Paperclip, 
  Bot, Clock
} from 'lucide-react';

// --- GLOBAL STATE MANAGEMENT (Zustand) ---
interface AppState {
  leftSidebarOpen: boolean;
  rightPanelOpen: boolean;
  activeTab: string;
  theme: 'dark' | 'light';
  messages: Array<{id: string, role: string, text: string, action?: string}>;
  isThinking: boolean;
  toggleLeftSidebar: () => void;
  toggleRightPanel: () => void;
  setActiveTab: (tab: string) => void;
  toggleTheme: () => void;
  addMessage: (msg: any) => void;
  setIsThinking: (status: boolean) => void;
}

const useAppStore = create<AppState>((set) => ({
  leftSidebarOpen: true,
  rightPanelOpen: false,
  activeTab: 'chat',
  theme: 'dark',
  messages: [{ id: '1', role: 'jarvis', text: 'System online. I am ready, sir.', action: 'system' }],
  isThinking: false,
  toggleLeftSidebar: () => set((state) => ({ leftSidebarOpen: !state.leftSidebarOpen })),
  toggleRightPanel: () => set((state) => ({ rightPanelOpen: !state.rightPanelOpen })),
  setActiveTab: (tab) => set({ activeTab: tab }),
  toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  setIsThinking: (status) => set({ isThinking: status }),
}));

// --- DESIGN SYSTEM COMPONENTS ---
const GlassPanel = ({ children, className = '', ...props }: any) => (
  <div 
    className={`bg-zinc-900/40 backdrop-blur-2xl border border-white/5 shadow-2xl ${className}`}
    {...props}
  >
    {children}
  </div>
);

const IconButton = ({ icon: Icon, onClick, isActive, className = '' }: any) => (
  <motion.button
    whileHover={{ scale: 1.05, backgroundColor: "rgba(255, 255, 255, 0.1)" }}
    whileTap={{ scale: 0.95 }}
    onClick={onClick}
    className={`p-2 rounded-xl transition-colors duration-200 flex items-center justify-center
      ${isActive ? 'bg-white/10 text-white shadow-inner' : 'text-zinc-400 hover:text-white'} 
      ${className}
    `}
  >
    <Icon size={20} strokeWidth={1.5} />
  </motion.button>
);

const SidebarItem = ({ icon: Icon, label, isActive, onClick, isOpen }: any) => (
  <motion.button
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300
      ${isActive ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'text-zinc-400 hover:bg-white/5 hover:text-white'}
    `}
  >
    <Icon size={20} strokeWidth={1.5} className={isActive ? 'text-blue-400' : ''} />
    <AnimatePresence>
      {isOpen && (
        <motion.span
          initial={{ opacity: 0, width: 0 }}
          animate={{ opacity: 1, width: 'auto' }}
          exit={{ opacity: 0, width: 0 }}
          className="whitespace-nowrap font-medium text-sm tracking-wide"
        >
          {label}
        </motion.span>
      )}
    </AnimatePresence>
  </motion.button>
);

const Avatar = ({ src, fallback }: any) => (
  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-zinc-700 to-zinc-900 border border-white/10 flex items-center justify-center overflow-hidden shrink-0 shadow-lg">
    {src ? <img src={src} alt="avatar" className="h-full w-full object-cover" /> : <span className="text-zinc-300 font-medium">{fallback}</span>}
  </div>
);

// --- LAYOUT COMPONENTS ---
const TopNav = () => {
  const { toggleLeftSidebar, toggleRightPanel, leftSidebarOpen, rightPanelOpen, theme, toggleTheme } = useAppStore();
  
  return (
    <GlassPanel className="h-16 w-full flex items-center justify-between px-4 z-50 rounded-b-2xl mb-4">
      <div className="flex items-center gap-4">
        <IconButton icon={leftSidebarOpen ? PanelLeftClose : PanelLeftOpen} onClick={toggleLeftSidebar} />
        <div className="flex items-center gap-3">
          <Bot size={24} className="text-blue-500" />
          <div>
            <h1 className="text-zinc-100 font-bold text-sm tracking-widest uppercase">ENIGM0</h1>
            <div className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse"></span>
              <span className="text-zinc-400 text-xs tracking-wider uppercase">Nexus Secure</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 text-zinc-400 bg-black/20 px-3 py-1.5 rounded-full border border-white/5">
          <Clock size={14} />
          <span className="text-xs font-medium tracking-wide">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <IconButton icon={theme === 'dark' ? Sun : Moon} onClick={toggleTheme} />
        <IconButton icon={rightPanelOpen ? PanelRightClose : PanelRightOpen} onClick={toggleRightPanel} />
        <div className="h-8 w-px bg-white/10 mx-1"></div>
        <Avatar fallback="AK" />
      </div>
    </GlassPanel>
  );
};

const Sidebar = () => {
  const { leftSidebarOpen, activeTab, setActiveTab } = useAppStore();
  
  return (
    <motion.div
      initial={false}
      animate={{ width: leftSidebarOpen ? 240 : 72 }}
      className="h-full flex flex-col gap-2 shrink-0 z-40"
    >
      <GlassPanel className="flex-1 rounded-2xl flex flex-col p-3 overflow-hidden">
        <div className="flex-1 flex flex-col gap-2 pt-2">
          <SidebarItem icon={MessageSquare} label="New Chat" isActive={activeTab === 'chat'} onClick={() => setActiveTab('chat')} isOpen={leftSidebarOpen} />
          <SidebarItem icon={History} label="History" isActive={activeTab === 'history'} onClick={() => setActiveTab('history')} isOpen={leftSidebarOpen} />
          <SidebarItem icon={Search} label="Search" isActive={activeTab === 'search'} onClick={() => setActiveTab('search')} isOpen={leftSidebarOpen} />
          
          <div className="my-4 h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
          
          <SidebarItem icon={FileText} label="Documents" isActive={activeTab === 'docs'} onClick={() => setActiveTab('docs')} isOpen={leftSidebarOpen} />
          <SidebarItem icon={ImageIcon} label="Images" isActive={activeTab === 'images'} onClick={() => setActiveTab('images')} isOpen={leftSidebarOpen} />
          <SidebarItem icon={Mic} label="Voice" isActive={activeTab === 'voice'} onClick={() => setActiveTab('voice')} isOpen={leftSidebarOpen} />
          <SidebarItem icon={Puzzle} label="Plugins" isActive={activeTab === 'plugins'} onClick={() => setActiveTab('plugins')} isOpen={leftSidebarOpen} />
        </div>
        
        <div className="mt-auto pt-4">
          <SidebarItem icon={Settings} label="Settings" isActive={activeTab === 'settings'} onClick={() => setActiveTab('settings')} isOpen={leftSidebarOpen} />
        </div>
      </GlassPanel>
    </motion.div>
  );
};

const RightPanel = () => {
  const { rightPanelOpen } = useAppStore();
  
  return (
    <AnimatePresence>
      {rightPanelOpen && (
        <motion.div
          initial={{ opacity: 0, width: 0, x: 20 }}
          animate={{ opacity: 1, width: 280, x: 0 }}
          exit={{ opacity: 0, width: 0, x: 20 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
          className="h-full shrink-0 z-40 pl-4 overflow-hidden"
        >
          <GlassPanel className="h-full rounded-2xl p-5 flex flex-col">
            <h3 className="text-zinc-100 font-semibold text-sm tracking-wider uppercase mb-6 flex items-center gap-2">
              <Wifi size={16} className="text-blue-400" /> System Status
            </h3>
            
            <div className="flex flex-col gap-6">
              <div className="bg-black/20 p-4 rounded-xl border border-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-zinc-400 text-xs font-medium uppercase tracking-wider">Swarm Logic</span>
                  <span className="text-green-400 text-xs font-bold">ACTIVE</span>
                </div>
                <div className="w-full bg-zinc-800 rounded-full h-1.5 mb-1 overflow-hidden">
                  <div className="bg-blue-500 h-1.5 rounded-full w-3/4"></div>
                </div>
                <span className="text-zinc-500 text-[10px] uppercase">75% Capacity</span>
              </div>
              
              <div className="bg-black/20 p-4 rounded-xl border border-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-zinc-400 text-xs font-medium uppercase tracking-wider">Omni-Logger</span>
                  <span className="text-green-400 text-xs font-bold">ONLINE</span>
                </div>
                <div className="w-full bg-zinc-800 rounded-full h-1.5 mb-1 overflow-hidden">
                  <div className="bg-purple-500 h-1.5 rounded-full w-1/3"></div>
                </div>
                <span className="text-zinc-500 text-[10px] uppercase">33% Memory Cache</span>
              </div>
            </div>
            
            <div className="mt-auto">
               <h3 className="text-zinc-400 font-medium text-xs tracking-wider uppercase mb-3">Recent Context</h3>
               <div className="text-zinc-500 text-xs italic bg-black/20 p-3 rounded-lg border border-white/5">
                 Awaiting new background events...
               </div>
            </div>
          </GlassPanel>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

const MainContent = () => {
  const { messages, isThinking, addMessage, setIsThinking } = useAppStore();
  const [inputText, setInputText] = useState('');
  const endOfMessagesRef = useRef<HTMLDivElement>(null);
  
  // Create a reference to hold our permanent WebSocket connection
  const wsRef = useRef<WebSocket | null>(null);

  // Hook up the WebSocket when the app loads
  useEffect(() => {
    let ws: WebSocket | null = null;
    
    try {
      ws = new WebSocket('ws://127.0.0.1:8000/ws/chat');
      
      ws.onopen = () => {
        console.log('[Nexus] WebSocket Connection Established');
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.role === 'system') {
          // The backend pinged us to say it's working
          console.log(data.text);
        } else {
          // The backend sent the final answer
          setIsThinking(false);
          addMessage({ id: Date.now().toString(), role: data.role, text: data.text, action: data.action });
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
        setIsThinking(false);
        addMessage({ id: Date.now().toString(), role: 'jarvis', text: "System Error: Connection to neural bridge lost. Is api_server.py running?" });
      };

      wsRef.current = ws;
    } catch (err) {
      console.warn("WebSocket restriction caught:", err);
      setTimeout(() => {
        addMessage({ 
          id: Date.now().toString(), 
          role: 'jarvis', 
          text: "Note: Real-time backend connections are restricted in this preview sandbox. Run this UI locally to connect to your Python J.A.R.V.I.S. backend.",
          action: "preview_mode"
        });
      }, 1000);
    }

    // Cleanup connection if we close the window
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []); // Run once on mount

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isThinking]);

  const handleSend = () => {
    if (!inputText.trim()) return;
    
    const userMsg = inputText;
    setInputText('');
    addMessage({ id: Date.now().toString(), role: 'user', text: userMsg });
    setIsThinking(true);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Shoot the message down the WebSocket pipe instantly!
      wsRef.current.send(JSON.stringify({ message: userMsg }));
    } else {
      // Graceful fallback if WebSocket is not available
      setTimeout(() => {
        setIsThinking(false);
        addMessage({ 
          id: Date.now().toString(), 
          role: 'jarvis', 
          text: "I am running in a preview sandbox without access to your local backend. Please run the frontend locally to execute Python Swarm commands.",
          action: "system"
        });
      }, 1500);
    }
  };

  return (
    <div className="flex-1 h-full flex flex-col px-4 relative z-0 min-w-0">
      <div className="flex-1 overflow-y-auto pb-4 scrollbar-hide flex flex-col gap-6 pt-8 pr-2">
        
        {messages.map((msg) => (
          <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex gap-4 max-w-3xl mx-auto w-full">
            {msg.role === 'user' ? (
              <>
                <Avatar fallback="U" />
                <div className="pt-1">
                  <p className="text-zinc-100 font-medium text-sm mb-1">User</p>
                  <p className="text-zinc-300 text-base leading-relaxed">{msg.text}</p>
                </div>
              </>
            ) : (
              <>
                <Avatar src="https://ui-avatars.com/api/?name=E&background=0D8ABC&color=fff" />
                <div className="pt-1 w-full min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="text-blue-400 font-medium text-sm">ENIGM0</p>
                    {msg.action && <span className="text-zinc-600 text-xs uppercase tracking-wider border border-white/10 px-2 py-0.5 rounded bg-black/20">Action: {msg.action}</span>}
                  </div>
                  <GlassPanel className="p-4 mt-2 rounded-2xl rounded-tl-none bg-blue-500/5 border-blue-500/10 overflow-hidden">
                    <p className="text-zinc-200 text-base leading-relaxed whitespace-pre-wrap break-words">{msg.text}</p>
                  </GlassPanel>
                </div>
              </>
            )}
          </motion.div>
        ))}
        
        {isThinking && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4 max-w-3xl mx-auto w-full">
             <Avatar src="https://ui-avatars.com/api/?name=E&background=0D8ABC&color=fff" />
             <div className="pt-3 pl-2">
               <span className="flex h-2 w-2 relative">
                 <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                 <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
               </span>
             </div>
          </motion.div>
        )}
        <div ref={endOfMessagesRef} className="h-1" />
      </div>

      {/* Bottom Input Area */}
      <div className="max-w-3xl mx-auto w-full pb-6 pt-2 shrink-0">
        <GlassPanel className="p-2 rounded-2xl flex items-end gap-2 bg-zinc-900/80 focus-within:border-blue-500/50 focus-within:ring-1 focus-within:ring-blue-500/50 transition-all duration-300 shadow-2xl">
          <IconButton icon={Paperclip} className="mb-1 hover:bg-white/10" />
          <textarea 
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Message J.A.R.V.I.S..."
            className="flex-1 bg-transparent border-none focus:ring-0 text-zinc-100 placeholder-zinc-500 resize-none max-h-32 min-h-[44px] py-3 px-2 text-base outline-none scrollbar-hide"
            rows={1}
          />
          <div className="flex items-center gap-1 mb-1">
            <IconButton icon={Mic} className="hover:bg-red-500/20 hover:text-red-400" />
            <motion.button
              onClick={handleSend}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-blue-600 hover:bg-blue-500 text-white p-2.5 rounded-xl ml-1 shadow-lg shadow-blue-500/20 flex items-center justify-center"
            >
              <Send size={18} />
            </motion.button>
          </div>
        </GlassPanel>
        <p className="text-center text-zinc-600 text-xs mt-3 tracking-wide">
          ENIGM0 operates using local Swarm Intelligence and LLaMA-3.3-70B.
        </p>
      </div>
    </div>
  );
};

export default function App() {
  
  return (
    <div className={`min-h-screen w-full flex flex-col p-4 font-sans antialiased overflow-hidden selection:bg-blue-500/30 selection:text-blue-200
      bg-zinc-950 text-zinc-100`}
      style={{
        backgroundImage: `radial-gradient(circle at 50% 0%, rgba(29, 78, 216, 0.15), transparent 50%), 
                          radial-gradient(circle at 100% 100%, rgba(147, 51, 234, 0.1), transparent 50%)`
      }}
    >
      <TopNav />
      <div className="flex-1 flex overflow-hidden w-full relative">
        <Sidebar />
        <MainContent />
        <RightPanel />
      </div>
    </div>
  );
}