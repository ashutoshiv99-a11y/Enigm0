export async function fetchHealth() {
  const response = await fetch(
    `${import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'}/health`,
  )

  if (!response.ok) {
    throw new Error('Unable to reach backend health endpoint')
  }

  return response.json()
}
