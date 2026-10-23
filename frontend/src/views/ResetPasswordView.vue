<template>
  <div class="reset-page">
    <div class="reset-card">
      <div class="reset-header">
        <router-link to="/" class="brand-link" title="Return to ObMind Home">
          <img src="../assets/icons/obrive-logo.svg" alt="ObMind Logo" class="brand-logo" />
        </router-link>
        <h1 class="brand-title font-microgramma">OBMIND</h1>
        <p class="brand-sub font-microgramma">Reset Your Password</p>
      </div>

      <!-- Success State -->
      <div v-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title font-microgramma">Password Reset Complete!</h2>
        <p class="state-desc">Your password has been securely updated. You can now log in.</p>
        <button class="primary-btn font-microgramma" @click="openLogin">
          <span>Log In to ObMind</span>
          <span class="btn-arrow">→</span>
        </button>
      </div>

      <!-- Form State -->
      <form v-else @submit.prevent="handleSubmit" class="reset-form">
        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label class="form-label font-microgramma">New Password</label>
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
          <label class="form-label font-microgramma">Confirm New Password</label>
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
          class="primary-btn full-width font-microgramma"
          :disabled="loading || !newPassword || !confirmPassword"
        >
          <span>{{ loading ? 'Updating Password...' : 'Save New Password' }}</span>
          <span class="btn-arrow">→</span>
        </button>

        <button type="button" class="text-link font-microgramma" @click="goToHome">
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
  background: linear-gradient(
    135deg,
    #caede5 0%,
    #beeee3 35%,
    #b2f0e1 70%,
    #98f2dd 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #074139;
}

.reset-card {
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(7, 65, 57, 0.12);
  width: 100%;
  max-width: 480px;
  padding: 44px 40px;
  border: 1.5px solid rgba(7, 65, 57, 0.18);
}

.reset-header {
  text-align: center;
  margin-bottom: 28px;
}

.brand-link {
  display: inline-block;
  text-decoration: none;
}

.brand-logo {
  height: 42px;
  margin-bottom: 12px;
}

.brand-title {
  font-size: 1.6rem;
  letter-spacing: 0.05em;
  color: #074139;
  margin: 0;
  font-weight: 800;
}

.brand-sub {
  font-size: 0.75rem;
  font-weight: 600;
  color: #526361;
  letter-spacing: 0.08em;
  margin-top: 4px;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.04em;
}

.input-field {
  padding: 12px 14px;
  background: #FFFFFF;
  border: 1.5px solid rgba(7, 65, 57, 0.2);
  border-radius: 10px;
  color: #074139;
  font-size: 0.92rem;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-field:focus {
  border-color: #074139;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.45);
}

.error-banner {
  background: #FEF2F2;
  color: #991B1B;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  border: 1px solid #FCA5A5;
}

.primary-btn {
  background: #074139;
  color: #CAEDE5;
  border: none;
  border-radius: 12px;
  padding: 14px 28px;
  font-size: 0.95rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  box-shadow: 0 8px 24px rgba(7, 65, 57, 0.25);
}

.primary-btn:hover:not(:disabled) {
  background: #052e28;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(7, 65, 57, 0.35);
}

.primary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-arrow {
  transition: transform 0.2s ease;
}

.primary-btn:hover:not(:disabled) .btn-arrow {
  transform: translateX(4px);
}

.full-width {
  width: 100%;
}

.text-link {
  background: transparent;
  border: none;
  color: #074139;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  text-align: center;
  margin-top: 6px;
  transition: opacity 0.2s ease;
  text-decoration: underline;
}

.text-link:hover {
  opacity: 0.75;
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.status-icon {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 16px;
}

.success-icon {
  background: #CAEDE5;
  color: #074139;
  border: 2px solid #074139;
  box-shadow: 0 0 20px rgba(7, 65, 57, 0.15);
}

.state-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #074139;
  margin-bottom: 10px;
  letter-spacing: 0.02em;
}

.state-desc {
  font-size: 0.95rem;
  color: #526361;
  margin-bottom: 24px;
  line-height: 1.5;
}
</style>
