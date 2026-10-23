<template>
  <div class="reset-page">
    <div class="reset-card">
      <div class="reset-header">
        <img src="../assets/logo/obrive-white-logo.svg" alt="ObMind Logo" class="brand-logo" />
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
  router.push('/console')
  setTimeout(() => {
    authStore.openAuthModal('login')
  }, 200)
}

const goToHome = () => {
  router.push('/console')
}
</script>

<style scoped>
.reset-page {
  min-height: 100vh;
  background: #070b0e;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #ffffff;
}

.reset-card {
  background: rgba(12, 18, 22, 0.85);
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  width: 100%;
  max-width: 460px;
  padding: 36px;
  border: 1px solid rgba(0, 229, 163, 0.25);
  backdrop-filter: blur(16px);
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
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.5rem;
  letter-spacing: 2px;
  color: #ffffff;
  margin: 0;
  font-weight: 800;
}

.brand-sub {
  font-size: 0.82rem;
  color: #94a3b8;
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
  color: #cbd5e1;
}

.input-field {
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.92rem;
  outline: none;
}

.input-field:focus {
  border-color: #00E5A3;
  box-shadow: 0 0 0 2px rgba(0, 229, 163, 0.2);
}

.error-banner {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.primary-btn {
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  color: #070b0e;
  border: none;
  border-radius: 10px;
  padding: 13px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 6px 20px rgba(0, 229, 163, 0.35);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 229, 163, 0.5);
  color: #000;
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
  color: #94a3b8;
  font-size: 0.82rem;
  cursor: pointer;
  text-align: center;
  margin-top: 6px;
  transition: color 0.2s ease;
}

.text-link:hover {
  color: #00E5A3;
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
  background: rgba(0, 229, 163, 0.15);
  color: #00E5A3;
  border: 2px solid #00E5A3;
  box-shadow: 0 0 20px rgba(0, 229, 163, 0.3);
}

.state-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.state-desc {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-bottom: 22px;
}
</style>
