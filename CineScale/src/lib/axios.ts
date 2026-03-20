import axios, { AxiosError } from 'axios'
import toast from 'react-hot-toast'

// Typed API error shape returned by FastAPI
export interface ApiError {
  detail: string | { msg: string; type: string }[]
}

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  timeout: 60_000,
  headers: {
    'Accept': 'application/json',
  },
})

// ── Response interceptor ────────────────────────────────────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    // No response — network / CORS / timeout
    if (!error.response) {
      toast.error('Network error — is the API running?')
      return Promise.reject(error)
    }

    const { status, data } = error.response

    // Resolve a human-readable message from FastAPI's detail field
    const detail = data?.detail
    const message =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(', ')
          : `Request failed (${status})`

    switch (status) {
      case 400: toast.error(`Bad request: ${message}`);        break
      case 404: toast.error(`Not found: ${message}`);          break
      case 413: toast.error('File too large');                  break
      case 422: toast.error(`Validation error: ${message}`);   break
      case 500: toast.error('Server error — check API logs');  break
      default:  toast.error(message)
    }

    return Promise.reject(error)
  }
)

export default apiClient
