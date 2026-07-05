export type ThemeMode = 'dark'

export interface ThemeTokens {
  background: string
  surface: string
  surfaceAlt: string
  border: string
  text: string
  textMuted: string
  accent: string
  accentSoft: string
  shadow: string
}

export const themeTokens: Record<ThemeMode, ThemeTokens> = {
  dark: {
    background: '#020617',
    surface: 'rgba(15, 23, 42, 0.72)',
    surfaceAlt: 'rgba(30, 41, 59, 0.8)',
    border: 'rgba(148, 163, 184, 0.18)',
    text: '#f8fafc',
    textMuted: '#94a3b8',
    accent: '#7dd3fc',
    accentSoft: 'rgba(125, 211, 252, 0.16)',
    shadow: '0 20px 45px rgba(2, 6, 23, 0.35)',
  },
}
