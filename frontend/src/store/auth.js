import { reactive, computed } from 'vue'

const TOKEN_KEY = 'brain_access_token'
const REFRESH_KEY = 'brain_refresh_token'
const USER_KEY = 'brain_user'
const LEGACY_TOKEN_KEY = 'obmind_access_token'
const LEGACY_REFRESH_KEY = 'obmind_refresh_token'
const LEGACY_USER_KEY = 'obmind_user'

const state = reactive({
  user: null,
  accessToken: localStorage.getItem(TOKEN_KEY) || localStorage.getItem(LEGACY_TOKEN_KEY) || localStorage.getItem('token') || null,
  refreshToken: localStorage.getItem(REFRESH_KEY) || localStorage.getItem(LEGACY_REFRESH_KEY) || null,
  authModalOpen: false,
  authModalTab: 'login', // 'login' | 'register' | 'forgot' | 'verify-otp'
  authNotice: '',
  verifyEmailTarget: '',
  profileModalOpen: false,
  initialized: false
})

// Load saved user from localStorage
try {
  const savedUser = localStorage.getItem(USER_KEY) || localStorage.getItem(LEGACY_USER_KEY) || localStorage.getItem('user')
  if (savedUser) {
    state.user = JSON.parse(savedUser)
  }
} catch (e) {
  console.warn('Failed to parse cached user:', e)
}

export const authStore = {
  state,
  isAuthenticated: computed(() => Boolean(state.accessToken && state.user)),
  isVerified: computed(() => Boolean(state.user && state.user.is_verified)),
  isAdmin: computed(() => Boolean(state.user && (state.user.role === 'admin' || state.user.email === 'ai@obrive.com'))),
  user: computed(() => state.user),
  accessToken: computed(() => state.accessToken),
  refreshToken: computed(() => state.refreshToken),

  setSession(accessToken, refreshToken, user) {
    state.accessToken = accessToken
    if (refreshToken) {
      state.refreshToken = refreshToken
      localStorage.setItem(REFRESH_KEY, refreshToken)
    }
    if (accessToken) {
      localStorage.setItem(TOKEN_KEY, accessToken)
      localStorage.setItem('token', accessToken)
    }
    if (user) {
      state.user = user
      localStorage.setItem(USER_KEY, JSON.stringify(user))
      localStorage.setItem('user', JSON.stringify(user))
    }
  },

  updateUser(user) {
    state.user = { ...(state.user || {}), ...user }
    localStorage.setItem(USER_KEY, JSON.stringify(state.user))
    localStorage.setItem('user', JSON.stringify(state.user))
  },

  clearSession() {
    state.accessToken = null
    state.refreshToken = null
    state.user = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(LEGACY_TOKEN_KEY)
    localStorage.removeItem('token')
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(LEGACY_REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(LEGACY_USER_KEY)
    localStorage.removeItem('user')
  },

  openAuthModal(tab = 'login', notice = '', targetEmail = '') {
    state.authModalTab = tab
    state.authNotice = notice
    if (targetEmail) {
      state.verifyEmailTarget = targetEmail
    } else if (state.user?.email) {
      state.verifyEmailTarget = state.user.email
    }
    state.authModalOpen = true
  },

  closeAuthModal() {
    state.authModalOpen = false
    state.authNotice = ''
  },

  openProfileModal() {
    state.profileModalOpen = true
  },

  closeProfileModal() {
    state.profileModalOpen = false
  }
}

export default authStore
