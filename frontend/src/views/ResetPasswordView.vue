<template>
  <div class="reset-page">
    <div class="reset-card">
      <div class="reset-header">
        <router-link to="/" class="brand-link" title="Return to Brain Home">
          <img src="../assets/icons/obrive-logo.svg" alt="Brain Logo" class="brand-logo" />
        </router-link>
        <h1 class="brand-title font-microgramma">BRAIN</h1>
        <p class="brand-sub font-microgramma">Reset Your Password</p>
      </div>

      <!-- Success State -->
      <div v-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title font-microgramma">Password Reset Complete!</h2>
        <p class="state-desc">Your password has been securely updated. You can now log in.</p>
        <AnimatedButton
          variant="primary"
          size="default"
          :iconSize="13"
          @click="openLogin"
          customClass="font-microgramma"
        >
          Log In to Brain
        </AnimatedButton>
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

        <AnimatedButton
          type="submit"
          variant="primary"
          size="default"
          :disabled="loading || !newPassword || !confirmPassword"
          :iconSize="13"
          customClass="full-width font-microgramma"
        >
          {{ loading ? 'Updating Password...' : 'Save New Password' }}
        </AnimatedButton>

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
import AnimatedButton from '../components/common/AnimatedButton.vue'

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
  background: #000000;
  background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1.2px, transparent 1.2px);
  background-size: 24px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: var(--font-sans, "Space Grotesk", system-ui, sans-serif);
  color: #000000;
}

.reset-card {
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 480px;
  padding: 40px 36px;
  border: 1px solid #CCCCCC;
}

.reset-header {
  text-align: center;
  margin-bottom: 24px;
}

.brand-link {
  display: inline-block;
  text-decoration: none;
}

.brand-logo {
  height: 38px;
  margin-bottom: 10px;
}

.brand-title {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.55rem;
  letter-spacing: -0.01em;
  color: #000000;
  margin: 0;
  font-weight: 700;
}

.brand-sub {
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  font-weight: 600;
  color: #666666;
  letter-spacing: 0.06em;
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
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.04em;
}

.input-field {
  padding: 10px 14px;
  background: #FAFAFA;
  border: 1px solid #DDDDDD;
  border-radius: 6px;
  color: #000000;
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #000000;
  background: #FFFFFF;
}

.error-banner {
  background: #FEF2F2;
  color: #991B1B;
  padding: 12px 14px;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  border: 1px solid #FCA5A5;
}

.primary-btn {
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  border-radius: 6px;
  padding: 12px 28px;
  font-family: var(--font-mono, monospace);
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.2s ease;
}

.primary-btn:hover:not(:disabled) {
  background: #FF4500;
  border-color: #FF4500;
  transform: translateY(-1px);
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
  color: #000000;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  text-align: center;
  margin-top: 6px;
  transition: color 0.2s ease;
  text-decoration: underline;
}

.text-link:hover {
  color: #FF4500;
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
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 16px;
}

.success-icon {
  background: #000000;
  color: #FFFFFF;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.state-title {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.35rem;
  font-weight: 700;
  color: #000000;
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.state-desc {
  font-size: 0.92rem;
  color: #666666;
  margin-bottom: 24px;
  line-height: 1.5;
}
</style>
