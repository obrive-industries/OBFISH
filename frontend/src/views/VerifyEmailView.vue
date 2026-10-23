<template>
  <div class="verify-page">
    <div class="verify-card">
      <!-- Brand Header -->
      <div class="verify-header">
        <router-link to="/" class="brand-link" title="Return to ObMind Home">
          <img src="../assets/icons/obrive-logo.svg" alt="ObMind Logo" class="brand-logo" />
        </router-link>
        <h1 class="brand-title font-microgramma">OBMIND</h1>
        <p class="brand-sub font-microgramma">Predictive Intelligence Platform</p>
      </div>

      <!-- State: Loading -->
      <div v-if="loading" class="state-container">
        <div class="spinner"></div>
        <h2 class="state-title font-microgramma">Verifying your email...</h2>
        <p class="state-desc">Please wait while we confirm your account with ObMind.</p>
      </div>

      <!-- State: Success -->
      <div v-else-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title font-microgramma">Email Verified!</h2>
        <p class="state-desc">{{ message || 'Your ObMind account is now fully active.' }}</p>
        <button class="primary-btn font-microgramma" @click="goToDashboard">
          <span>Launch ObMind Platform</span>
          <span class="btn-arrow">→</span>
        </button>
      </div>

      <!-- State: Error -->
      <div v-else class="state-container">
        <div class="status-icon error-icon">!</div>
        <h2 class="state-title font-microgramma">Verification Failed</h2>
        <p class="error-desc">{{ errorMessage }}</p>

        <!-- Resend Section -->
        <div class="resend-box">
          <p class="resend-label font-microgramma">Need a new verification link?</p>
          <div class="resend-form">
            <input
              v-model="resendEmail"
              type="email"
              placeholder="Enter your email address"
              class="input-field"
              :disabled="resending"
            />
            <button
              class="secondary-btn font-microgramma"
              @click="handleResend"
              :disabled="resending || !resendEmail"
            >
              {{ resending ? 'Sending...' : 'Resend Link' }}
            </button>
          </div>
          <p v-if="resendSuccess" class="resend-success-msg font-microgramma">
            ✓ A new verification link has been sent to your email.
          </p>
        </div>

        <button class="text-link font-microgramma" @click="goToDashboard">
          ← Return to Console
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

.verify-card {
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(7, 65, 57, 0.12);
  width: 100%;
  max-width: 500px;
  padding: 44px 40px;
  text-align: center;
  border: 1.5px solid rgba(7, 65, 57, 0.18);
}

.verify-header {
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
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 20px;
}

.success-icon {
  background: #CAEDE5;
  color: #074139;
  border: 2px solid #074139;
  box-shadow: 0 0 20px rgba(7, 65, 57, 0.15);
}

.error-icon {
  background: #FEE2E2;
  color: #DC2626;
  border: 2px solid #EF4444;
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
  line-height: 1.5;
  margin-bottom: 28px;
}

.error-desc {
  font-size: 0.92rem;
  color: #991B1B;
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 24px;
  width: 100%;
}

.primary-btn {
  background: #074139;
  color: #CAEDE5;
  border: none;
  border-radius: 12px;
  padding: 14px 32px;
  font-size: 0.95rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  box-shadow: 0 8px 24px rgba(7, 65, 57, 0.25);
}

.primary-btn:hover {
  background: #052e28;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(7, 65, 57, 0.35);
}

.btn-arrow {
  transition: transform 0.2s ease;
}

.primary-btn:hover .btn-arrow {
  transform: translateX(4px);
}

.resend-box {
  width: 100%;
  background: #F9FCFB;
  border: 1.5px solid rgba(7, 65, 57, 0.16);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
  text-align: left;
}

.resend-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}

.resend-form {
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 10px 14px;
  background: #FFFFFF;
  border: 1.5px solid rgba(7, 65, 57, 0.2);
  border-radius: 8px;
  color: #074139;
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #074139;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.45);
}

.secondary-btn {
  background: #CAEDE5;
  border: 1.5px solid #074139;
  color: #074139;
  border-radius: 8px;
  padding: 10px 18px;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover:not(:disabled) {
  background: #074139;
  color: #CAEDE5;
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.resend-success-msg {
  font-size: 0.8rem;
  font-weight: 600;
  color: #074139;
  margin-top: 10px;
}

.text-link {
  background: transparent;
  border: none;
  color: #074139;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  text-decoration: underline;
  margin-top: 10px;
  transition: opacity 0.2s;
}

.text-link:hover {
  opacity: 0.75;
}
</style>
