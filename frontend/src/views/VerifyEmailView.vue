<template>
  <div class="verify-page">
    <div class="verify-card">
      <!-- Brand Header -->
      <div class="verify-header">
        <router-link to="/" class="brand-link" title="Return to Brain Home">
          <img src="../assets/icons/obrive-logo.svg" alt="Brain Logo" class="brand-logo" />
        </router-link>
        <h1 class="brand-title font-microgramma">BRAIN</h1>
        <p class="brand-sub font-microgramma">Predictive Intelligence Platform</p>
      </div>

      <!-- State: Loading -->
      <div v-if="loading" class="state-container">
        <div class="spinner"></div>
        <h2 class="state-title font-microgramma">Verifying your email...</h2>
        <p class="state-desc">Please wait while we confirm your account with Brain.</p>
      </div>

      <!-- State: Success -->
      <div v-else-if="success" class="state-container">
        <div class="status-icon success-icon">✓</div>
        <h2 class="state-title font-microgramma">Email Verified!</h2>
        <p class="state-desc">{{ message || 'Your Brain account is now fully active.' }}</p>
        <button class="primary-btn font-microgramma" @click="goToDashboard">
          <span>Launch Brain Platform</span>
          <span class="btn-arrow">→</span>
        </button>
      </div>

      <!-- State: Error -->
      <div v-else class="state-container">
        <div class="status-icon error-icon">!</div>
        <h2 class="state-title font-microgramma">Verification Failed</h2>
        <p class="error-desc">{{ errorMessage }}</p>

        <!-- OTP Entry Section -->
        <div class="resend-box" style="margin-bottom: 20px;">
          <p class="resend-label font-microgramma">Enter 6-Digit Verification Code</p>
          <div class="resend-form">
            <input
              v-model="otpInput"
              type="text"
              maxlength="6"
              placeholder="000000"
              class="input-field"
              style="text-align: center; letter-spacing: 6px; font-weight: 800; font-size: 1.1rem;"
              :disabled="otpVerifying"
            />
            <button
              class="secondary-btn font-microgramma"
              @click="handleVerifyOtpManual"
              :disabled="otpVerifying || otpInput.trim().length < 6"
            >
              {{ otpVerifying ? 'Verifying...' : 'Verify Code' }}
            </button>
          </div>
        </div>

        <!-- Resend Section -->
        <div class="resend-box">
          <p class="resend-label font-microgramma">Need a new verification code?</p>
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
              {{ resending ? 'Sending...' : 'Resend Code' }}
            </button>
          </div>
          <p v-if="resendSuccess" class="resend-success-msg font-microgramma">
            ✓ A new 6-digit verification code has been sent to your email.
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
const otpInput = ref('')
const otpVerifying = ref(false)

onMounted(async () => {
  const token = route.query.token || route.query.otp
  if (!token) {
    loading.value = false
    errorMessage.value = 'Please enter your 6-digit verification code below.'
    return
  }

  try {
    const res = await authApi.verifyOtp({ otp: token })
    success.value = true
    message.value = res.message || 'Email verified successfully.'
    if (res.access_token && res.user) {
      authStore.setSession(res.access_token, null, res.user)
    }
  } catch (err) {
    success.value = false
    errorMessage.value = err.message || 'This verification code is invalid or has expired.'
  } finally {
    loading.value = false
  }
})

const handleVerifyOtpManual = async () => {
  const code = otpInput.value.trim()
  if (code.length < 6) return
  otpVerifying.value = true
  errorMessage.value = ''

  try {
    const res = await authApi.verifyOtp({
      email: resendEmail.value.trim() || undefined,
      otp: code
    })
    success.value = true
    message.value = res.message || 'Email verified successfully.'
    if (res.access_token && res.user) {
      authStore.setSession(res.access_token, null, res.user)
    }
  } catch (err) {
    errorMessage.value = err.message || 'Invalid or expired code. Please try again.'
  } finally {
    otpVerifying.value = false
  }
}

const handleResend = async () => {
  if (!resendEmail.value || resending.value) return
  resending.value = true
  resendSuccess.value = false

  try {
    await authApi.resendVerification(resendEmail.value.trim())
    resendSuccess.value = true
  } catch (err) {
    errorMessage.value = err.message || 'Failed to resend verification code.'
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

.verify-card {
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 480px;
  padding: 40px 36px;
  text-align: center;
  border: 1px solid #CCCCCC;
}

.verify-header {
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

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #E5E5E5;
  border-top-color: #000000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 18px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
  margin-bottom: 18px;
}

.success-icon {
  background: #000000;
  color: #FFFFFF;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.error-icon {
  background: #FEE2E2;
  color: #DC2626;
  border: 1px solid #EF4444;
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
  line-height: 1.55;
  margin-bottom: 24px;
}

.error-desc {
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
  color: #991B1B;
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 20px;
  width: 100%;
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
  gap: 10px;
  transition: all 0.2s ease;
}

.primary-btn:hover {
  background: #FF4500;
  border-color: #FF4500;
  transform: translateY(-1px);
}

.btn-arrow {
  transition: transform 0.2s ease;
}

.primary-btn:hover .btn-arrow {
  transform: translateX(4px);
}

.resend-box {
  width: 100%;
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  text-align: left;
}

.resend-label {
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}

.resend-form {
  display: flex;
  gap: 8px;
}

.input-field {
  flex: 1;
  padding: 9px 12px;
  background: #FFFFFF;
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
}

.secondary-btn {
  background: #000000;
  border: 1px solid #000000;
  color: #FFFFFF;
  border-radius: 6px;
  padding: 9px 16px;
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover:not(:disabled) {
  background: #FF4500;
  border-color: #FF4500;
}

.secondary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.resend-success-msg {
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 600;
  color: #2E7D32;
  margin-top: 8px;
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
  text-decoration: underline;
  margin-top: 8px;
  transition: color 0.2s ease;
}

.text-link:hover {
  color: #FF4500;
}
</style>
