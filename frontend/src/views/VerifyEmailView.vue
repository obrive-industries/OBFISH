<template>
  <div class="verify-page">
    <div class="verify-card">
      <!-- Brand Header -->
      <div class="verify-header">
        <img src="../assets/logo/obrive-white-logo.svg" alt="ObMind Logo" class="brand-logo" />
        <h1 class="brand-title">OBMIND</h1>
        <p class="brand-sub">Predictive Intelligence Platform</p>
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
  router.push('/console')
}
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  background: #070b0e;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #ffffff;
}

.verify-card {
  background: rgba(12, 18, 22, 0.85);
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
  width: 100%;
  max-width: 500px;
  padding: 40px;
  text-align: center;
  border: 1px solid rgba(0, 229, 163, 0.25);
  backdrop-filter: blur(16px);
}

.verify-header {
  margin-bottom: 30px;
}

.brand-logo {
  height: 38px;
  margin-bottom: 12px;
}

.brand-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.6rem;
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

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3.5px solid rgba(0, 229, 163, 0.15);
  border-top-color: #00E5A3;
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
  background: rgba(0, 229, 163, 0.15);
  color: #00E5A3;
  border: 2px solid #00E5A3;
  box-shadow: 0 0 20px rgba(0, 229, 163, 0.3);
}

.error-icon {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 2px solid #ef4444;
}

.state-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 10px;
}

.state-desc {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.5;
  margin-bottom: 25px;
}

.error-desc {
  font-size: 0.92rem;
  color: #f87171;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  width: 100%;
}

.primary-btn {
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  color: #070b0e;
  border: none;
  border-radius: 10px;
  padding: 13px 32px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 6px 20px rgba(0, 229, 163, 0.35);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 229, 163, 0.5);
  color: #000;
}

.resend-box {
  width: 100%;
  background: rgba(7, 11, 14, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 20px;
  text-align: left;
}

.resend-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 8px;
}

.resend-form {
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #fff;
  font-size: 0.88rem;
  outline: none;
}

.input-field:focus {
  border-color: #00E5A3;
}

.secondary-btn {
  background: #074139;
  border: 1px solid rgba(0, 229, 163, 0.4);
  color: #00E5A3;
  border-radius: 8px;
  padding: 10px 18px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover:not(:disabled) {
  background: #00E5A3;
  color: #070b0e;
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.resend-success-msg {
  font-size: 0.82rem;
  color: #00E5A3;
  margin-top: 8px;
}

.text-link {
  background: transparent;
  border: none;
  color: #00E5A3;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  margin-top: 8px;
}
</style>
