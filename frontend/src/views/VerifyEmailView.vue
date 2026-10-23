<template>
  <div class="verify-page">
    <div class="verify-card">
      <!-- Brand Header -->
      <div class="verify-header">
        <img src="../assets/logo/obrive-logo.svg" alt="ObMind Logo" class="brand-logo" />
        <h1 class="brand-title">OBMIND</h1>
        <p class="brand-sub">Swarm Intelligence Platform</p>
      </div>

      <!-- State: Loading -->
      <div v-if="loading" class="state-container">
        <div class="spinner"></div>
        <h2 class="state-title">Verifying your email...</h2>
        <p class="state-desc">Please wait while we confirm your account with ObMind.</p>
      </div>

      <!-- State: Success -->
      <div v-else-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title">Email Verified!</h2>
        <p class="state-desc">{{ message || 'Your ObMind account is now fully active.' }}</p>
        <button class="primary-btn" @click="goToDashboard">
          Launch ObMind Platform →
        </button>
      </div>

      <!-- State: Error -->
      <div v-else class="state-container">
        <div class="status-icon error-icon">!</div>
        <h2 class="state-title">Verification Failed</h2>
        <p class="error-desc">{{ errorMessage }}</p>

        <!-- Resend Section -->
        <div class="resend-box">
          <p class="resend-label">Need a new verification link?</p>
          <div class="resend-form">
            <input
              v-model="resendEmail"
              type="email"
              placeholder="Enter your email address"
              class="input-field"
              :disabled="resending"
            />
            <button
              class="secondary-btn"
              @click="handleResend"
              :disabled="resending || !resendEmail"
            >
              {{ resending ? 'Sending...' : 'Resend Link' }}
            </button>
          </div>
          <p v-if="resendSuccess" class="resend-success-msg">
            ✓ A new verification link has been sent to your email.
          </p>
        </div>

        <button class="text-link" @click="goToDashboard">
          ← Back to Homepage
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import authApi from '../api/auth'
import authStore from '../store/auth'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const success = ref(false)
const message = ref('')
const errorMessage = ref('')
const resendEmail = ref('')
const resending = ref(false)
const resendSuccess = ref(false)

onMounted(async () => {
  const token = route.query.token
  if (!token) {
    loading.value = false
    errorMessage.value = 'Verification token is missing from the link.'
    return
  }

  try {
    const res = await authApi.verifyEmail(token)
    success.value = true
    message.value = res.message || 'Email verified successfully.'
    if (res.access_token && res.user) {
      authStore.setSession(res.access_token, null, res.user)
    }
  } catch (err) {
    success.value = false
    errorMessage.value = err.message || 'This verification link is invalid or has expired.'
  } finally {
    loading.value = false
  }
})

const handleResend = async () => {
  if (!resendEmail.value || resending.value) return
  resending.value = true
  resendSuccess.value = false

  try {
    await authApi.resendVerification(resendEmail.value.trim())
    resendSuccess.value = true
  } catch (err) {
    errorMessage.value = err.message || 'Failed to resend verification email.'
  } finally {
    resending.value = false
  }
}

const goToDashboard = () => {
  router.push('/')
}
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  background: #A2F1DF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.verify-card {
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(7, 65, 57, 0.12);
  width: 100%;
  max-width: 500px;
  padding: 40px;
  text-align: center;
  border: 1px solid rgba(7, 65, 57, 0.12);
}

.verify-header {
  margin-bottom: 30px;
}

.brand-logo {
  height: 38px;
  margin-bottom: 12px;
}

.brand-title {
  font-family: 'Michroma', sans-serif;
  font-size: 1.6rem;
  letter-spacing: 2px;
  color: #074139;
  margin: 0;
}

.brand-sub {
  font-size: 0.82rem;
  color: #526361;
  margin-top: 4px;
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3.5px solid rgba(7, 65, 57, 0.15);
  border-top-color: #074139;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.status-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.success-icon {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
  border: 2px solid #10B981;
}

.error-icon {
  background: rgba(239, 68, 68, 0.12);
  color: #DC2626;
  border: 2px solid #EF4444;
}

.state-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #074139;
  margin-bottom: 10px;
}

.state-desc {
  font-size: 0.95rem;
  color: #526361;
  line-height: 1.5;
  margin-bottom: 25px;
}

.error-desc {
  font-size: 0.92rem;
  color: #B91C1C;
  background: #FEF2F2;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  width: 100%;
}

.primary-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 8px;
  padding: 12px 28px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(7, 65, 57, 0.2);
}

.primary-btn:hover {
  background: #052e28;
  transform: translateY(-1px);
}

.resend-box {
  width: 100%;
  background: #F8FDFC;
  border: 1px solid rgba(7, 65, 57, 0.14);
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 20px;
  text-align: left;
}

.resend-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #074139;
  margin-bottom: 8px;
}

.resend-form {
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 9px 12px;
  border: 1px solid rgba(7, 65, 57, 0.25);
  border-radius: 6px;
  font-size: 0.88rem;
  outline: none;
}

.input-field:focus {
  border-color: #074139;
}

.secondary-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 6px;
  padding: 9px 16px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.resend-success-msg {
  font-size: 0.82rem;
  color: #059669;
  margin-top: 8px;
}

.text-link {
  background: transparent;
  border: none;
  color: #074139;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  margin-top: 8px;
}
</style>
