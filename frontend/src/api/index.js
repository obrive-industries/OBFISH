import axios from 'axios'
import i18n from '../i18n'
import authStore from '../store/auth'

// Create Axios instance
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 300000, // 5 minutes
  headers: {
    'Content-Type': 'application/json'
  }
})

let isRefreshing = false
let refreshSubscribers = []

function onRefreshed(token) {
  refreshSubscribers.forEach(cb => cb(token))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb) {
  refreshSubscribers.push(cb)
}

// Request interceptor: attach language and Bearer JWT token
service.interceptors.request.use(
  config => {
    config.headers['Accept-Language'] = i18n.global.locale.value
    const token = localStorage.getItem('brain_access_token') || localStorage.getItem('obmind_access_token') || localStorage.getItem('token') || authStore.state.accessToken
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor: handle automatic token refresh and error extraction
service.interceptors.response.use(
  response => {
    const res = response.data

    if (!res.success && res.success !== undefined) {
      console.error('API Error:', res.error || res.message || 'Unknown error')
      const apiError = new Error(res.error || res.message || 'Error')
      if (res.code) apiError.code = res.code
      return Promise.reject(apiError)
    }

    return res
  },
  async error => {
    const originalRequest = error.config
    const responseStatus = error.response?.status
    const errorCode = error.response?.data?.code

    // Handle token expiration: attempt transparent refresh
    if (responseStatus === 401 && (errorCode === 'TOKEN_EXPIRED' || !originalRequest._retry)) {
      const refreshToken = localStorage.getItem('brain_refresh_token') || localStorage.getItem('obmind_refresh_token')
      if (refreshToken && !originalRequest._retry) {
        if (!isRefreshing) {
          isRefreshing = true
          originalRequest._retry = true

          try {
            const refreshRes = await axios.post('/api/auth/refresh', {
              refresh_token: refreshToken
            })

            const newAccessToken = refreshRes.data?.access_token
            const newRefreshToken = refreshRes.data?.refresh_token || refreshToken
            const updatedUser = refreshRes.data?.user
            if (newAccessToken) {
              localStorage.setItem('brain_access_token', newAccessToken)
              localStorage.setItem('token', newAccessToken)
              if (newRefreshToken) {
                localStorage.setItem('brain_refresh_token', newRefreshToken)
              }
              if (updatedUser) {
                localStorage.setItem('brain_user', JSON.stringify(updatedUser))
                localStorage.setItem('user', JSON.stringify(updatedUser))
              }
              // Sync with authStore to prevent user session desync
              authStore.setSession(newAccessToken, newRefreshToken, updatedUser || authStore.state.user)

              onRefreshed(newAccessToken)
              isRefreshing = false

              originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`
              return service(originalRequest)
            }
          } catch (refreshErr) {
            isRefreshing = false
            localStorage.removeItem('brain_access_token')
            localStorage.removeItem('obmind_access_token')
            localStorage.removeItem('token')
            localStorage.removeItem('brain_refresh_token')
            localStorage.removeItem('obmind_refresh_token')
            localStorage.removeItem('brain_user')
            localStorage.removeItem('obmind_user')
            localStorage.removeItem('user')
            authStore.clearSession()
            window.dispatchEvent(new CustomEvent('brain-auth-logout'))
            window.dispatchEvent(new CustomEvent('obmind-auth-logout'))
            return Promise.reject(refreshErr)
          }
        } else {
          // Queue duplicate requests until token refresh completes
          return new Promise(resolve => {
            addRefreshSubscriber(token => {
              originalRequest.headers['Authorization'] = `Bearer ${token}`
              resolve(service(originalRequest))
            })
          })
        }
      }
    }

    // Handle blob error responses (e.g. from failed downloads)
    if (error.response?.data instanceof Blob) {
      try {
        const text = await error.response.data.text()
        const parsed = JSON.parse(text)
        if (parsed.error || parsed.message) {
          error.message = parsed.error || parsed.message
        }
      } catch (e) {
        // Not a JSON blob, keep standard error
      }
    }

    const apiError = error.response?.data?.error || error.response?.data?.message
    if (typeof apiError === 'string' && apiError) {
      error.message = apiError
    }
    if (errorCode) error.code = errorCode
    error.status = responseStatus

    // Any plan-gated endpoint can raise the pricing popup, not just Start Engine.
    if (responseStatus === 402 && String(errorCode || '').startsWith('PLAN_')) {
      window.dispatchEvent(
        new CustomEvent('brain-plan-required', { detail: { code: errorCode } })
      )
    }

    return Promise.reject(error)
  }
)

export default service
