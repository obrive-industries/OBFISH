<template>
  <div v-if="authStore.state.authModalOpen" class="modal-backdrop" @click.self="authStore.closeAuthModal">
    <div class="modal-card">
      <!-- Close button -->
      <button class="close-btn" @click="authStore.closeAuthModal">×</button>

      <!-- Header -->
      <div class="modal-header">
        <img src="../assets/logo/obrive-logo.svg" alt="Brain" class="modal-logo" />
        <h2 class="modal-brand">BRAIN</h2>
        <p class="modal-subtitle">Swarm Intelligence Platform</p>
      </div>

      <!-- Tab Switcher (Login / Register) -->
      <div v-if="authStore.state.authModalTab !== 'forgot' && authStore.state.authModalTab !== 'verify-otp'" class="tabs">
        <button
          :class="['tab-btn', { active: authStore.state.authModalTab === 'login' }]"
          @click="switchTab('login')"
        >
          Sign In
        </button>
        <button
          :class="['tab-btn', { active: authStore.state.authModalTab === 'register' }]"
          @click="switchTab('register')"
        >
          Create Account
        </button>
      </div>

      <!-- Notice Alert -->
      <div v-if="authStore.state.authNotice" class="alert notice-alert">
        <span class="notice-icon">🔒</span> {{ authStore.state.authNotice }}
      </div>

      <!-- Error / Success Alert -->
      <div v-if="errorMsg" class="alert error-alert">
        {{ errorMsg }}
      </div>
      <div v-if="successMsg" class="alert success-alert">
        {{ successMsg }}
      </div>

      <!-- 1. LOGIN FORM -->
      <form v-if="authStore.state.authModalTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input
            v-model="loginForm.email"
            type="email"
            placeholder="you@company.com"
            class="input-field"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <div class="label-row">
            <label class="form-label">Password</label>
            <button type="button" class="inline-link" @click="switchTab('forgot')">
              Forgot password?
            </button>
          </div>
          <input
            v-model="loginForm.password"
            type="password"
            placeholder="••••••••"
            class="input-field"
            required
            :disabled="loading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing In...' : 'Sign In →' }}
        </button>

        <p class="switch-prompt">
          Don't have an account?
          <button type="button" class="switch-link" @click="switchTab('register')">
            Create an account
          </button>
        </p>
      </form>

      <!-- 2. REGISTER FORM -->
      <form v-else-if="authStore.state.authModalTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label class="form-label">Full Name</label>
          <input
            v-model="registerForm.fullName"
            type="text"
            placeholder="Yash Sharma"
            class="input-field"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Work Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            placeholder="you@company.com"
            class="input-field"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password (min 8 characters)</label>
          <input
            v-model="registerForm.password"
            type="password"
            placeholder="••••••••"
            class="input-field"
            required
            minlength="8"
            :disabled="loading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Create Account & Verify →' }}
        </button>

        <p class="switch-prompt">
          Already have an account?
          <button type="button" class="switch-link" @click="switchTab('login')">
            Sign In
          </button>
        </p>
      </form>

      <!-- 3. FORGOT PASSWORD FORM -->
      <form v-else-if="authStore.state.authModalTab === 'forgot'" @submit.prevent="handleForgot" class="auth-form">
        <p class="forgot-desc">
          Enter your email address and we'll send you a password reset link.
        </p>

        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input
            v-model="forgotEmail"
            type="email"
            placeholder="you@company.com"
            class="input-field"
            required
            :disabled="loading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
        </button>

        <p class="switch-prompt">
          Remembered your password?
          <button type="button" class="switch-link" @click="switchTab('login')">
            Back to Sign In
          </button>
        </p>
      </form>

      <!-- 4. OTP VERIFICATION FORM -->
      <form v-else-if="authStore.state.authModalTab === 'verify-otp'" @submit.prevent="handleVerifyOtp" class="auth-form">
        <div class="otp-header">
          <div class="otp-icon-wrap">✉️</div>
          <h3 class="otp-title font-microgramma">Verify Email</h3>
          <p class="otp-desc">
            We sent a 6-digit verification code to<br/>
            <strong>{{ displayTargetEmail }}</strong>
          </p>
        </div>

        <div class="form-group">
          <label class="form-label" style="text-align: center;">Enter 6-Digit Code</label>
          <input
            v-model="otpCode"
            type="text"
            maxlength="6"
            pattern="[0-9]{6}"
            inputmode="numeric"
            placeholder="••••••"
            class="input-field otp-input"
            required
            autocomplete="one-time-code"
            :disabled="loading"
            @input="handleOtpInput"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading || otpCode.trim().length < 6">
          {{ loading ? 'Verifying Code...' : 'Verify Email & Activate →' }}
        </button>

        <div class="otp-actions">
          <button 
            type="button" 
            class="resend-btn" 
            :disabled="resendCooldown > 0 || resending"
            @click="handleResendOtp"
          >
            {{ resending ? 'Sending...' : resendCooldown > 0 ? `Resend code in ${resendCooldown}s` : 'Resend Code' }}
          </button>
        </div>

        <p class="switch-prompt">
          Want to use a different account?
          <button type="button" class="switch-link" @click="switchTab('login')">
            Back to Sign In
          </button>
        </p>
      </form>

      <!-- Modal Footer Admin Access -->
      <div class="modal-admin-footer">
        <button
          type="button"
          class="admin-wishlist-link"
          @click="openWishlistSubmissions"
        >
          📋 View Wishlist Submissions (Admin)
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authStore from '../store/auth'
import authApi from '../api/auth'

const router = useRouter()

const openWishlistSubmissions = () => {
  authStore.closeAuthModal()
  router.push('/admin/wishlist')
}

const loading = ref(false)
const resending = ref(false)
const resendCooldown = ref(0)
const errorMsg = ref('')
const successMsg = ref('')
const otpCode = ref('')
let timerInterval = null

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  fullName: '',
  email: '',
  password: ''
})

const forgotEmail = ref('')

const displayTargetEmail = computed(() => {
  return authStore.state.verifyEmailTarget || registerForm.email || authStore.user.value?.email || 'your email'
})

const startResendTimer = (seconds = 60) => {
  resendCooldown.value = seconds
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    if (resendCooldown.value > 0) {
      resendCooldown.value--
    } else {
      clearInterval(timerInterval)
      timerInterval = null
    }
  }, 1000)
}

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

const handleOtpInput = (e) => {
  // Only keep numbers
  otpCode.value = e.target.value.replace(/\D/g, '').slice(0, 6)
  if (otpCode.value.length === 6) {
    handleVerifyOtp()
  }
}

const switchTab = (tab) => {
  errorMsg.value = ''
  successMsg.value = ''
  authStore.state.authModalTab = tab
}

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const res = await authApi.login({
      email: loginForm.email.trim(),
      password: loginForm.password
    })

    authStore.setSession(res.access_token, res.refresh_token, res.user)
    successMsg.value = 'Signed in successfully!'
    setTimeout(() => {
      authStore.closeAuthModal()
      loginForm.email = ''
      loginForm.password = ''
      successMsg.value = ''
    }, 600)
  } catch (err) {
    errorMsg.value = err.message || 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const emailToVerify = registerForm.email.trim()
    const res = await authApi.register({
      email: emailToVerify,
      password: registerForm.password,
      full_name: registerForm.fullName.trim()
    })

    authStore.setSession(res.access_token, res.refresh_token, res.user)
    authStore.state.verifyEmailTarget = emailToVerify
    otpCode.value = ''
    successMsg.value = 'Account created! Enter the 6-digit code sent to your email.'
    authStore.state.authModalTab = 'verify-otp'
    startResendTimer(60)
  } catch (err) {
    errorMsg.value = err.message || 'Failed to create account.'
  } finally {
    loading.value = false
  }
}

const handleVerifyOtp = async () => {
  const code = otpCode.value.trim()
  if (code.length < 6) {
    errorMsg.value = 'Please enter the complete 6-digit verification code.'
    return
  }

  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const res = await authApi.verifyOtp({
      email: displayTargetEmail.value,
      otp: code
    })

    if (res.access_token) {
      authStore.setSession(res.access_token, authStore.state.refreshToken, res.user)
    } else if (res.user) {
      authStore.state.user = res.user
      localStorage.setItem('brain_user', JSON.stringify(res.user))
      localStorage.setItem('obmind_user', JSON.stringify(res.user))
    }

    successMsg.value = 'Email verified successfully! Welcome to Brain.'
    setTimeout(() => {
      authStore.closeAuthModal()
      otpCode.value = ''
      successMsg.value = ''
      registerForm.fullName = ''
      registerForm.email = ''
      registerForm.password = ''
    }, 1000)
  } catch (err) {
    errorMsg.value = err.message || 'Invalid or expired code. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleResendOtp = async () => {
  if (resendCooldown.value > 0 || resending.value) return
  const email = displayTargetEmail.value
  if (!email || email === 'your email') {
    errorMsg.value = 'Email address not found. Please sign in again.'
    return
  }

  resending.value = true
  errorMsg.value = ''
  try {
    await authApi.resendVerification(email)
    successMsg.value = 'A new 6-digit verification code has been sent!'
    startResendTimer(60)
  } catch (err) {
    errorMsg.value = err.message || 'Failed to resend code.'
  } finally {
    resending.value = false
  }
}

const handleForgot = async () => {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    await authApi.forgotPassword(forgotEmail.value.trim())
    successMsg.value = 'If an account exists, a reset link has been sent to your email.'
  } catch (err) {
    errorMsg.value = err.message || 'Failed to send reset link.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-card {
  position: relative;
  background: #FFFFFF;
  border: 1px solid #CCCCCC;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  padding: 34px 32px 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  font-family: var(--font-sans, "Space Grotesk", system-ui, sans-serif);
  animation: modalEnter 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 18px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #888888;
  cursor: pointer;
  line-height: 1;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #000000;
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 20px;
}

.modal-logo {
  display: block;
  height: 34px;
  width: auto;
  margin: 0 auto 10px auto;
  object-fit: contain;
}

.modal-brand {
  font-family: var(--font-display, "Space Grotesk", sans-serif) !important;
  font-weight: 700;
  font-size: 1.45rem;
  color: #000000;
  letter-spacing: -0.01em;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.82rem;
  color: #666666;
  margin-top: 4px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #E5E5E5;
  margin-bottom: 20px;
}

.tab-btn {
  flex: 1;
  padding: 10px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
  font-weight: 700;
  color: #888888;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: -1px;
}

.tab-btn.active {
  color: #000000;
  border-bottom-color: #000000;
}

.alert {
  padding: 10px 14px;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  margin-bottom: 16px;
  line-height: 1.4;
}

.error-alert {
  background: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FCA5A5;
}

.notice-alert {
  background: #FFFDF0;
  color: #A08940;
  border: 1px solid #F0E4B0;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-alert {
  background: #F0FFF4;
  color: #2E7D32;
  border: 1px solid #B8E8C4;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 700;
  color: #000000;
}

.input-field {
  padding: 10px 14px;
  background: #FAFAFA;
  border: 1px solid #DDDDDD;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #000000;
  background: #FFFFFF;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.submit-btn {
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  border-radius: 6px;
  padding: 12px;
  font-family: var(--font-mono, monospace);
  font-size: 0.92rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 4px;
  letter-spacing: 0.5px;
}

.submit-btn:hover:not(:disabled) {
  background: #FF4500;
  border-color: #FF4500;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.switch-prompt {
  text-align: center;
  font-size: 0.82rem;
  color: #666666;
  margin-top: 6px;
}

.switch-link, .inline-link {
  background: transparent;
  border: none;
  color: #000000;
  font-weight: 700;
  cursor: pointer;
  padding: 0 4px;
  font-size: inherit;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.switch-link:hover, .inline-link:hover {
  color: #FF4500;
}

.forgot-desc {
  font-size: 0.88rem;
  color: #666666;
  line-height: 1.5;
  margin: 0;
}

.otp-header {
  text-align: center;
  margin-bottom: 4px;
}

.otp-icon-wrap {
  font-size: 2rem;
  margin-bottom: 6px;
}

.otp-title {
  margin: 0 0 6px 0;
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.25rem;
  color: #000000;
  font-weight: 700;
}

.otp-desc {
  font-size: 0.85rem;
  color: #666666;
  line-height: 1.5;
  margin: 0;
}

.otp-input {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 10px;
  padding: 12px;
  color: #000000;
  background: #FAFAFA;
  font-family: var(--font-mono, monospace);
}

.otp-actions {
  display: flex;
  justify-content: center;
  margin-top: 4px;
}

.resend-btn {
  background: transparent;
  border: none;
  color: #000000;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  padding: 4px 8px;
  transition: color 0.2s ease;
}

.resend-btn:hover:not(:disabled) {
  color: #FF4500;
}

.resend-btn:disabled {
  color: #999999;
  cursor: not-allowed;
  text-decoration: none;
}

.modal-admin-footer {
  margin-top: 1.5rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  text-align: center;
}

.admin-wishlist-link {
  background: transparent;
  border: 1px dashed rgba(0, 0, 0, 0.25);
  border-radius: 9999px;
  color: #555555;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.35rem 0.85rem;
  transition: all 0.2s ease;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.admin-wishlist-link:hover {
  color: #000000;
  border-color: #000000;
  background: rgba(0, 0, 0, 0.04);
}
</style>
