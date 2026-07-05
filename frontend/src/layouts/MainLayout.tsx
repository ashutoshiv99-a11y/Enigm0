import { Outlet } from 'react-router-dom'
import { AppShell } from '../components/shell/AppShell'

export function MainLayout() {
  return (
    <div className="min-h-screen bg-transparent">
      <AppShell />
      <Outlet />
    </div>
  )
}
