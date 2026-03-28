import axios from 'axios'
import { supabase } from './supabaseClient'

// Determine API URL based on environment
function getApiBaseUrl() {
  // If VITE_API_URL is set, use it
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Use relative URL - Vite proxy handles /api requests
  // This works for both local dev and Codespaces
  return '/api'
}

const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
})

// Add auth token to every request
apiClient.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }
  return config
})

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
