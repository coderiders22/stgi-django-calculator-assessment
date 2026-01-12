import axios from 'axios'

/**
 * Base API instance
 * Uses environment variable (local + production safe)
 */
const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`,
  withCredentials: true,
})

/**
 * 🔐 Initialize CSRF cookie
 * Must be called once on app startup
 */
export const initCSRF = async () => {
  try {
    await api.get('/auth/csrf/', {
      withCredentials: true,
    })
  } catch (error) {
    console.warn('CSRF init failed (non-fatal):', error)
  }
}

/**
 * Request interceptor
 * Adds CSRF token automatically
 */
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }

  config.withCredentials = true
  return config
})

/**
 * Response interceptor
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login?session_expired=true'
    }
    return Promise.reject(error)
  }
)

export default api
