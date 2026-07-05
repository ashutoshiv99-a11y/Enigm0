import { useEffect } from 'react'
import { useAppStore } from '../store/appStore'

export function useTheme() {
  const theme = useAppStore((state) => state.theme)
  const setTheme = useAppStore((state) => state.setTheme)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
  }, [theme])

  return { theme, setTheme }
}
