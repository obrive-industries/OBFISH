import { reactive, computed } from 'vue'

const TOKEN_KEY = 'obmind_access_token'
const REFRESH_KEY = 'obmind_refresh_token'
const USER_KEY = 'obmind_user'

const state = reactive({
  user: null,
  accessToken: localStorage.getItem(TOKEN_KEY) || null,
  refreshToken: localStorage.getItem(REFRESH_KEY) || null,
  authModalOpen: false,
  authModalTab: 'login', // 'login' | 'register' | 'forgot'
  authNotice: '',
  profileModalOpen: false,
  initialized: false
})

// Load saved user from localStorage
try {
  const savedUser = localStorage.getItem(USER_KEY)
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
    }
    if (user) {
      state.user = user
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    }
  },

  updateUser(user) {
    state.user = { ...(state.user || {}), ...user }
    localStorage.setItem(USER_KEY, JSON.stringify(state.user))
  },

  clearSession() {
    state.accessToken = null
    state.refreshToken = null
    state.user = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
  },

  openAuthModal(tab = 'login', notice = '') {
    state.authModalTab = tab
    state.authNotice = notice
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
