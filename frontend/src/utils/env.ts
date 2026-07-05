const env = import.meta.env

export const appConfig = {
  appName: env.VITE_APP_NAME ?? 'Enigm0 Assistant',
  apiBaseUrl: env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  environment: env.MODE ?? 'development',
}
