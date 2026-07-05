export interface AppConfig {
  appName: string
  apiBaseUrl: string
  environment: string
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}
