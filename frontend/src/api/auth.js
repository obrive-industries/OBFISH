import service from './index'

export const authApi = {
  // Sign up with email + password
  register(data) {
    return service.post('/api/auth/register', data)
  },

  // Log in
  login(data) {
    return service.post('/api/auth/login', data)
  },

  // Refresh access token
  refreshToken(refreshToken) {
    return service.post('/api/auth/refresh', { refresh_token: refreshToken })
  },

  // Verify email using token from link
  verifyEmail(token) {
    return service.get('/api/auth/verify-email', { params: { token } })
  },

  // Verify email using 6-digit OTP code
  verifyOtp(data) {
    return service.post('/api/auth/verify-otp', data)
  },

  // Resend verification email
  resendVerification(email) {
    return service.post('/api/auth/resend-verification', { email })
  },

  // Request password reset link
  forgotPassword(email) {
    return service.post('/api/auth/forgot-password', { email })
  },

  // Reset password using token
  resetPassword(data) {
    return service.post('/api/auth/reset-password', data)
  },

  // Get current user profile
  getMe() {
    return service.get('/api/auth/me')
  },

  // Update profile & BYOK LLM settings
  updateProfile(data) {
    return service.put('/api/auth/profile', data)
  },

  // Change password while logged in
  changePassword(data) {
    return service.post('/api/auth/change-password', data)
  },

  // Probe & auto-detect BYOK API key
  probeLlmKey(data) {
    return service.post('/api/auth/probe-llm-key', data)
  }
}

export default authApi
