<template>
  <div v-if="authStore.state.authModalOpen" class="modal-backdrop" @click.self="authStore.closeAuthModal">
    <div class="modal-card">
      <!-- Close button -->
      <button class="close-btn" @click="authStore.closeAuthModal">×</button>

      <!-- Header -->
      <div class="modal-header">
        <img src="/obrive-logo.svg" alt="Brain" class="modal-logo" />
        <h2 class="modal-brand font-microgramma">BRAIN</h2>
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
          <div class="input-password-wrap">
            <input
              v-model="loginForm.password"
              :type="showLoginPassword ? 'text' : 'password'"
              placeholder="••••••••"
              class="input-field input-field-password"
              required
              :disabled="loading"
            />
            <button
              type="button"
              class="password-toggle-btn"
              @click="showLoginPassword = !showLoginPassword"
              :title="showLoginPassword ? 'Hide password' : 'Show password'"
              tabindex="-1"
            >
              <svg v-if="showLoginPassword" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
              <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </button>
          </div>
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
          <div class="input-password-wrap">
            <input
              v-model="registerForm.password"
              :type="showRegisterPassword ? 'text' : 'password'"
              placeholder="••••••••"
              class="input-field input-field-password"
              required
              minlength="8"
              :disabled="loading"
            />
            <button
              type="button"
              class="password-toggle-btn"
              @click="showRegisterPassword = !showRegisterPassword"
              :title="showRegisterPassword ? 'Hide password' : 'Show password'"
              tabindex="-1"
            >
              <svg v-if="showRegisterPassword" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
              <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </button>
          </div>
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

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onUnmounted } from 'vue'
import authStore from '../store/auth'
import authApi from '../api/auth'

const loading = ref(false)
const resending = ref(false)
const resendCooldown = ref(0)
const showLoginPassword = ref(false)
const showRegisterPassword = ref(false)
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
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 24px;
  width: 100%;
  max-width: 440px;
  padding: 36px 32px 30px;
  box-shadow: 0 25px 60px -15px rgba(7, 57, 51, 0.22), 0 0 0 1px rgba(162, 241, 223, 0.25);
  font-family: var(--font-sans, 'Inter', system-ui, sans-serif);
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
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(7, 57, 51, 0.06);
  border: none;
  font-size: 1.25rem;
  color: #4a635d;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(7, 57, 51, 0.15);
  color: #000000;
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 22px;
}

.modal-logo {
  display: block;
  height: 36px;
  width: auto;
  margin: 0 auto 10px auto;
  object-fit: contain;
}

.modal-brand {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-weight: 800;
  font-size: 1.55rem;
  color: #073933;
  letter-spacing: 0.06em;
  margin: 0;
  text-transform: uppercase;
}

.modal-subtitle {
  font-size: 0.82rem;
  color: #073933;
  margin-top: 4px;
  font-weight: 500;
  opacity: 0.85;
}

.tabs {
  display: flex;
  background: #F0F5F3;
  border: 1px solid rgba(7, 57, 51, 0.1);
  border-radius: 9999px;
  padding: 4px;
  gap: 4px;
  margin-bottom: 22px;
}

.tab-btn {
  flex: 1;
  padding: 9px 16px;
  background: transparent;
  border: none;
  border-radius: 9999px;
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.86rem;
  font-weight: 600;
  color: #4a635d;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.19, 1, 0.22, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-btn:hover:not(.active) {
  color: #000000;
}

.tab-btn.active {
  background: #000000;
  color: #A2F1DF;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.alert {
  padding: 11px 15px;
  border-radius: 12px;
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.82rem;
  margin-bottom: 16px;
  line-height: 1.45;
}

.error-alert {
  background: #FEF2F2;
  color: #991B1B;
  border: 1px solid #FECACA;
  font-weight: 500;
}

.notice-alert {
  background: rgba(162, 241, 223, 0.25);
  color: #073933;
  border: 1px solid rgba(7, 57, 51, 0.2);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-alert {
  background: #ECFDF5;
  color: #065F46;
  border: 1px solid #A7F3D0;
  font-weight: 500;
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
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.82rem;
  font-weight: 600;
  color: #000000;
}

.input-password-wrap {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-field {
  width: 100%;
  padding: 12px 16px;
  background: #F8FAF9;
  border: 1.5px solid rgba(7, 57, 51, 0.16);
  border-radius: 12px;
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.92rem;
  color: #000000;
  outline: none;
  transition: all 0.2s ease;
}

.input-field::placeholder {
  color: #8c9e99;
}

.input-field-password {
  padding-right: 44px;
}

.input-field:focus {
  border-color: #073933;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.45);
}

.password-toggle-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  padding: 4px;
  color: #6b827c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.password-toggle-btn:hover {
  color: #073933;
}

.eye-icon {
  width: 18px;
  height: 18px;
}

.submit-btn {
  background: #000000;
  color: #A2F1DF;
  border: 1.5px solid #000000;
  border-radius: 9999px;
  padding: 13px 20px;
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  margin-top: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
}

.submit-btn:hover:not(:disabled) {
  background: #073933;
  border-color: #073933;
  color: #FFFFFF;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(7, 57, 51, 0.25);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.switch-prompt {
  text-align: center;
  font-size: 0.84rem;
  color: #000000;
  margin-top: 8px;
}

.switch-link, .inline-link {
  background: transparent;
  border: none;
  color: #073933;
  font-weight: 700;
  cursor: pointer;
  padding: 0 4px;
  font-size: inherit;
  text-decoration: underline;
  text-decoration-color: rgba(7, 57, 51, 0.35);
  transition: all 0.2s ease;
}

.switch-link:hover, .inline-link:hover {
  color: #000000;
  text-decoration-color: #000000;
}

.forgot-desc {
  font-size: 0.88rem;
  color: #000000;
  line-height: 1.5;
  margin: 0;
}

.otp-header {
  text-align: center;
  margin-bottom: 8px;
}

.otp-icon-wrap {
  font-size: 2.2rem;
  margin-bottom: 6px;
}

.otp-title {
  margin: 0 0 6px 0;
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-size: 1.35rem;
  color: #000000;
  font-weight: 800;
  text-transform: uppercase;
}

.otp-desc {
  font-size: 0.86rem;
  color: #000000;
  line-height: 1.5;
  margin: 0;
}

.otp-desc strong {
  color: #073933;
}

.otp-input {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 10px;
  padding: 12px;
  color: #000000;
  background: #F8FAF9;
  border: 1.5px solid rgba(7, 57, 51, 0.2);
  border-radius: 12px;
  font-family: var(--font-mono, monospace);
}

.otp-actions {
  display: flex;
  justify-content: center;
  margin-top: 6px;
}

.resend-btn {
  background: transparent;
  border: none;
  color: #073933;
  font-family: var(--font-sans, 'Inter', sans-serif);
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  text-decoration-color: rgba(7, 57, 51, 0.35);
  padding: 4px 8px;
  transition: all 0.2s ease;
}

.resend-btn:hover:not(:disabled) {
  color: #000000;
  text-decoration-color: #000000;
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
  background: rgba(7, 57, 51, 0.06);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 9999px;
  color: #073933;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.45rem 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.admin-wishlist-link:hover {
  color: #A2F1DF;
  border-color: #000000;
  background: #000000;
}
</style>
