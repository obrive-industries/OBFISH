import axios from 'axios'
import i18n from '../i18n'

// Create Axios instance
const service = axios.create({
  baseURL: '',
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
    const token = localStorage.getItem('obmind_access_token')
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
      return Promise.reject(new Error(res.error || res.message || 'Error'))
    }

    return res
  },
  async error => {
    const originalRequest = error.config
    const responseStatus = error.response?.status
    const errorCode = error.response?.data?.code

    // Handle token expiration: attempt transparent refresh
    if (responseStatus === 401 && errorCode === 'TOKEN_EXPIRED' && !originalRequest._retry) {
      const refreshToken = localStorage.getItem('obmind_refresh_token')
      if (refreshToken) {
        if (!isRefreshing) {
          isRefreshing = true
          originalRequest._retry = true

          try {
            const refreshRes = await axios.post('/api/auth/refresh', {
              refresh_token: refreshToken
            })

            const newAccessToken = refreshRes.data?.access_token
            if (newAccessToken) {
              localStorage.setItem('obmind_access_token', newAccessToken)
              if (refreshRes.data?.user) {
                localStorage.setItem('obmind_user', JSON.stringify(refreshRes.data.user))
              }
              onRefreshed(newAccessToken)
              isRefreshing = false

              originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`
              return service(originalRequest)
            }
          } catch (refreshErr) {
            isRefreshing = false
            localStorage.removeItem('obmind_access_token')
            localStorage.removeItem('obmind_refresh_token')
            localStorage.removeItem('obmind_user')
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

    const apiError = error.response?.data?.error || error.response?.data?.message
    if (typeof apiError === 'string' && apiError) {
      error.message = apiError
    }

    return Promise.reject(error)
  }
)

export default service
