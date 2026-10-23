<template>
  <div class="reset-page">
    <div class="reset-card">
      <div class="reset-header">
        <img src="../assets/logo/obrive-logo.svg" alt="ObMind Logo" class="brand-logo" />
        <h1 class="brand-title">OBMIND</h1>
        <p class="brand-sub">Reset Your Password</p>
      </div>

      <!-- Success State -->
      <div v-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title">Password Reset Complete!</h2>
        <p class="state-desc">Your password has been securely updated. You can now log in.</p>
        <button class="primary-btn" @click="openLogin">
          Log In to ObMind →
        </button>
      </div>

      <!-- Form State -->
      <form v-else @submit.prevent="handleSubmit" class="reset-form">
        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label class="form-label">New Password</label>
          <input
            v-model="newPassword"
            type="password"
            placeholder="At least 8 characters"
            class="input-field"
            required
            minlength="8"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Confirm New Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Repeat your new password"
            class="input-field"
            required
            minlength="8"
            :disabled="loading"
          />
        </div>

        <button
          type="submit"
          class="primary-btn full-width"
          :disabled="loading || !newPassword || !confirmPassword"
        >
          {{ loading ? 'Updating Password...' : 'Save New Password' }}
        </button>

        <button type="button" class="text-link" @click="goToHome">
          ← Cancel and return home
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import authApi from '../api/auth'
import authStore from '../store/auth'

const route = useRoute()
const router = useRouter()

const token = route.query.token || ''
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const success = ref(false)
const errorMessage = ref('')

const handleSubmit = async () => {
  if (!token) {
    errorMessage.value = 'Password reset token is missing from the URL.'
    return
  }

  if (newPassword.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    await authApi.resetPassword({
      token,
      new_password: newPassword.value
    })
    success.value = true
  } catch (err) {
    errorMessage.value = err.message || 'Failed to reset password. The link may have expired.'
  } finally {
    loading.value = false
  }
}

const openLogin = () => {
  router.push('/')
  setTimeout(() => {
    authStore.openAuthModal('login')
  }, 200)
}

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.reset-page {
  min-height: 100vh;
  background: #A2F1DF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.reset-card {
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(7, 65, 57, 0.12);
  width: 100%;
  max-width: 460px;
  padding: 36px;
  border: 1px solid rgba(7, 65, 57, 0.12);
}

.reset-header {
  text-align: center;
  margin-bottom: 26px;
}

.brand-logo {
  height: 36px;
  margin-bottom: 10px;
}

.brand-title {
  font-family: 'Michroma', sans-serif;
  font-size: 1.5rem;
  letter-spacing: 2px;
  color: #074139;
  margin: 0;
}

.brand-sub {
  font-size: 0.82rem;
  color: #526361;
  margin-top: 4px;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #074139;
}

.input-field {
  padding: 10px 14px;
  border: 1px solid rgba(7, 65, 57, 0.25);
  border-radius: 8px;
  font-size: 0.92rem;
  outline: none;
}

.input-field:focus {
  border-color: #074139;
  box-shadow: 0 0 0 2px rgba(7, 65, 57, 0.15);
}

.error-banner {
  background: #FEF2F2;
  color: #B91C1C;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 0.85rem;
  border: 1px solid #FCA5A5;
}

.primary-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn:hover:not(:disabled) {
  background: #052e28;
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.full-width {
  width: 100%;
}

.text-link {
  background: transparent;
  border: none;
  color: #526361;
  font-size: 0.82rem;
  cursor: pointer;
  text-align: center;
  margin-top: 6px;
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.status-icon {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.success-icon {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
  border: 2px solid #10B981;
}

.state-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #074139;
  margin-bottom: 8px;
}

.state-desc {
  font-size: 0.9rem;
  color: #526361;
  margin-bottom: 22px;
}
</style>
