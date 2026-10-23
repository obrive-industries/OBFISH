<template>
  <div v-if="authStore.state.authModalOpen" class="modal-backdrop" @click.self="authStore.closeAuthModal">
    <div class="modal-card">
      <!-- Close button -->
      <button class="close-btn" @click="authStore.closeAuthModal">×</button>

      <!-- Header -->
      <div class="modal-header">
        <img src="../assets/logo/obrive-logo.svg" alt="ObMind" class="modal-logo" />
        <h2 class="modal-brand">OBMIND</h2>
        <p class="modal-subtitle">Swarm Intelligence Platform</p>
      </div>

      <!-- Tab Switcher (Login / Register) -->
      <div v-if="authStore.state.authModalTab !== 'forgot'" class="tabs">
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import authStore from '../store/auth'
import authApi from '../api/auth'

const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

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
    const res = await authApi.register({
      email: registerForm.email.trim(),
      password: registerForm.password,
      full_name: registerForm.fullName.trim()
    })

    authStore.setSession(res.access_token, res.refresh_token, res.user)
    successMsg.value = 'Account created! Please check your email to verify your account.'
    setTimeout(() => {
      authStore.closeAuthModal()
      registerForm.fullName = ''
      registerForm.email = ''
      registerForm.password = ''
    }, 2500)
  } catch (err) {
    errorMsg.value = err.message || 'Failed to create account.'
  } finally {
    loading.value = false
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
  background: rgba(7, 65, 57, 0.45);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-card {
  position: relative;
  background: #FFFFFF;
  border: 1px solid rgba(7, 65, 57, 0.16);
  border-radius: 16px;
  width: 100%;
  max-width: 440px;
  padding: 34px 32px 30px;
  box-shadow: 0 20px 45px rgba(7, 65, 57, 0.2);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
  font-size: 1.6rem;
  color: #526361;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: #074139;
}

.modal-header {
  text-align: center;
  margin-bottom: 20px;
}

.modal-logo {
  height: 34px;
  margin-bottom: 8px;
}

.modal-brand {
  font-family: 'Michroma', sans-serif;
  font-size: 1.45rem;
  color: #074139;
  letter-spacing: 2px;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.8rem;
  color: #526361;
  margin-top: 4px;
}

.tabs {
  display: flex;
  border-bottom: 1.5px solid rgba(7, 65, 57, 0.12);
  margin-bottom: 20px;
}

.tab-btn {
  flex: 1;
  padding: 10px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 0.9rem;
  font-weight: 600;
  color: #526361;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: -1.5px;
}

.tab-btn.active {
  color: #074139;
  border-bottom-color: #074139;
}

.alert {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  margin-bottom: 16px;
  line-height: 1.4;
}

.error-alert {
  background: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FCA5A5;
}

.notice-alert {
  background: rgba(7, 65, 57, 0.08);
  color: #074139;
  border: 1px solid rgba(7, 65, 57, 0.25);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-alert {
  background: #ECFDF5;
  color: #065F46;
  border: 1px solid #6EE7B7;
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
  font-size: 0.82rem;
  font-weight: 600;
  color: #074139;
}

.input-field {
  padding: 10px 14px;
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 8px;
  font-size: 0.92rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #074139;
  box-shadow: 0 0 0 2px rgba(7, 65, 57, 0.12);
}

.submit-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 4px;
  box-shadow: 0 4px 12px rgba(7, 65, 57, 0.15);
}

.submit-btn:hover:not(:disabled) {
  background: #052e28;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-prompt {
  text-align: center;
  font-size: 0.82rem;
  color: #526361;
  margin-top: 6px;
}

.switch-link, .inline-link {
  background: transparent;
  border: none;
  color: #074139;
  font-weight: 700;
  cursor: pointer;
  padding: 0 4px;
  font-size: inherit;
  text-decoration: underline;
}

.forgot-desc {
  font-size: 0.88rem;
  color: #526361;
  line-height: 1.5;
  margin: 0;
}
</style>
