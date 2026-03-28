import axios from 'axios'
import { supabase } from './supabaseClient'

// Determine API URL based on environment
function getApiBaseUrl() {
  // If VITE_API_URL is set, use it
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // In Codespaces, construct URL from current host
  if (window.location.hostname.includes('github.dev')) {
    // Replace the frontend port (5173) with backend port (5000)
    const backendUrl = window.location.origin.replace('-5173.', '-5000.')
    return `${backendUrl}/api`
  }
  
  // Default for local development
  return 'http://localhost:5000/api'
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
