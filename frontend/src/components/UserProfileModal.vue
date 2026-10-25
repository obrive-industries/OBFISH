<template>
  <div v-if="authStore.state.profileModalOpen" class="modal-backdrop" @click.self="authStore.closeProfileModal">
    <div class="modal-card">
      <button class="close-btn" @click="authStore.closeProfileModal">×</button>

      <!-- Header -->
      <div class="profile-header">
        <div class="avatar-circle">
          {{ userInitials }}
        </div>
        <div class="profile-info">
          <div class="name-row">
            <h3 class="user-name">{{ user?.full_name || 'Brain User' }}</h3>
            <span v-if="user?.is_verified" class="badge verified-badge">✓ Verified</span>
            <span v-else class="badge unverified-badge">! Unverified</span>
          </div>
          <p class="user-email">{{ user?.email }}</p>
        </div>
      </div>

      <!-- Resend Verification Banner if unverified -->
      <div v-if="!user?.is_verified" class="unverified-banner">
        <div class="banner-text">
          <strong>Email not verified.</strong> Simulation runs require email confirmation.
        </div>
        <button class="resend-action-btn" @click="handleResendVerification" :disabled="resending">
          {{ resending ? 'Sending...' : 'Resend Email' }}
        </button>
      </div>
      <div v-if="resendSuccessMsg" class="alert success-alert">
        {{ resendSuccessMsg }}
      </div>

      <!-- Tabs / Sections -->
      <div class="settings-tabs">
        <button
          :class="['tab-item', { active: activeTab === 'plan' }]"
          @click="activeTab = 'plan'"
        >
          ◇ Plan &amp; Usage
        </button>
        <button
          :class="['tab-item', { active: activeTab === 'security' }]"
          @click="activeTab = 'security'"
        >
          🔒 Security
        </button>
      </div>

      <!-- Alert -->
      <div v-if="errorMsg" class="alert error-alert">
        {{ errorMsg }}
      </div>
      <div v-if="successMsg" class="alert success-alert">
        {{ successMsg }}
      </div>

      <!-- 1. PLAN & USAGE TAB -->
      <div v-if="activeTab === 'plan'" class="tab-content plan-tab">
        <p class="section-hint">
          Your plan sets how many simulations you can run and how many rounds each run may simulate.
        </p>

        <div class="plan-summary" :class="{ 'is-paid': plan.plan !== 'free' }">
          <div>
            <div class="plan-summary-name">{{ planTitle }}</div>
            <div class="plan-summary-meta">{{ planMeta }}</div>
          </div>
          <span class="plan-status-badge">{{ planBadge }}</span>
        </div>

        <div v-if="!plan.unlimited" class="usage-block">
          <div class="usage-row">
            <span>Simulation runs</span>
            <span>{{ plan.runs_used }} / {{ plan.runs_limit }} used</span>
          </div>
          <div class="usage-track">
            <div class="usage-fill" :style="{ width: usagePercent + '%' }"></div>
          </div>
          <div class="usage-foot">
            <span>{{ remainingRuns }} remaining this period</span>
            <span v-if="plan.max_rounds">{{ plan.max_rounds }} rounds max per run</span>
          </div>
        </div>

        <div v-else class="unlimited-note">
          Unlimited simulations and uncapped rounds.
        </div>

        <div class="plan-actions">
          <button type="button" class="primary-btn" :disabled="!plan.configured && plan.plan === 'free'" @click="openPlans">
            {{ plan.plan === 'free' ? 'Choose a plan' : 'Change plan' }}
          </button>
          <button
            v-if="canCancel"
            type="button"
            class="secondary-plan-btn"
            :disabled="cancelling"
            @click="handleCancelPlan"
          >
            {{ cancelling ? 'Cancelling...' : 'Cancel subscription' }}
          </button>
        </div>

        <p v-if="plan.cancel_at_period_end" class="plan-note">
          Your subscription ends on {{ formatDate(plan.period_end) }}. You keep access until then.
        </p>
        <p v-else-if="!plan.configured && plan.plan === 'free'" class="plan-note">
          Card checkout is not configured on this deployment yet.
        </p>
      </div>

      <!-- 2. SECURITY (CHANGE PASSWORD) TAB -->
      <div v-else-if="activeTab === 'security'" class="tab-content">
        <form @submit.prevent="handleChangePassword" class="settings-form">
          <div class="form-group">
            <label class="form-label">Current Password</label>
            <input
              v-model="passForm.currentPassword"
              type="password"
              placeholder="••••••••"
              class="input-field"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">New Password (min 8 chars)</label>
            <input
              v-model="passForm.newPassword"
              type="password"
              placeholder="••••••••"
              class="input-field"
              required
              minlength="8"
            />
          </div>

          <button type="submit" class="primary-btn" :disabled="saving">
            {{ saving ? 'Updating...' : 'Update Password' }}
          </button>
        </form>
      </div>

      <!-- Footer: Log out & Admin Submissions -->
      <div class="modal-footer">
        <button
          v-if="authStore.isAdmin.value"
          type="button"
          class="admin-wishlist-pill"
          @click="openWishlistAdmin"
        >
          📋 Wishlist Submissions
        </button>
        <button class="logout-btn" @click="handleLogout">
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import authStore from '../store/auth'
import authApi from '../api/auth'
import billingStore from '../store/billing'

const router = useRouter()
const user = computed(() => authStore.user.value)
const activeTab = ref('plan')

const openWishlistAdmin = () => {
  authStore.closeProfileModal()
  router.push('/admin/wishlist')
}
const saving = ref(false)
const resending = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const resendSuccessMsg = ref('')

const userInitials = computed(() => {
  const name = user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const plan = computed(() => billingStore.entitlement.value)
const cancelling = ref(false)

const passForm = reactive({
  currentPassword: '',
  newPassword: ''
})

const planTitle = computed(() => {
  if (plan.value.unlimited) return 'Admin access'
  return plan.value.plan_name || 'Free demo'
})

const planBadge = computed(() => {
  if (plan.value.unlimited) return 'UNLIMITED'
  if (plan.value.status === 'pending' || plan.value.status === 'halted') return 'PAYMENT ISSUE'
  if (plan.value.plan === 'free') return 'FREE'
  if (plan.value.cancel_at_period_end) return 'CANCELLING'
  return 'ACTIVE'
})

const planMeta = computed(() => {
  if (plan.value.unlimited) return 'All simulation limits bypassed'
  if (plan.value.plan === 'free') return 'Sample report access only'
  const interval = plan.value.interval === 'annual' ? 'Annual' : 'Monthly'
  if (plan.value.cancel_at_period_end) {
    return `${interval} plan · access ends ${formatDate(plan.value.period_end)}`
  }
  const renewal = plan.value.period_end ? ` · renews ${formatDate(plan.value.period_end)}` : ''
  return `${interval} plan${renewal}`
})

const remainingRuns = computed(() => {
  return Math.max(0, (plan.value.runs_limit || 0) - (plan.value.runs_used || 0))
})

const usagePercent = computed(() => {
  if (!plan.value.runs_limit) return 0
  return Math.min(100, Math.round((plan.value.runs_used / plan.value.runs_limit) * 100))
})

const canCancel = computed(() => {
  return ['starter', 'pro', 'premium'].includes(plan.value.plan)
    && plan.value.status === 'active'
    && !plan.value.cancel_at_period_end
})

const formatDate = (value) => {
  if (!value) return '-'
  return new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const openPlans = () => {
  authStore.closeProfileModal()
  billingStore.openPricing({ resume: false })
}

const handleCancelPlan = async () => {
  if (!window.confirm('Cancel your subscription? You will keep access until the end of the paid period.')) return
  cancelling.value = true
  errorMsg.value = ''
  const ok = await billingStore.cancel()
  if (ok) {
    successMsg.value = 'Subscription cancelled. Access continues until the period ends.'
  } else {
    errorMsg.value = billingStore.state.error || 'Could not cancel the subscription.'
  }
  cancelling.value = false
}

watch(
  () => authStore.state.profileModalOpen,
  (isOpen) => {
    if (!isOpen) return
    activeTab.value = 'plan'
    errorMsg.value = ''
    successMsg.value = ''
    resendSuccessMsg.value = ''
    if (authStore.isAuthenticated.value) {
      billingStore.refresh()
    }
  }
)

const handleChangePassword = async () => {
  saving.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    await authApi.changePassword({
      current_password: passForm.currentPassword,
      new_password: passForm.newPassword
    })
    successMsg.value = 'Password updated successfully!'
    passForm.currentPassword = ''
    passForm.newPassword = ''
  } catch (err) {
    errorMsg.value = err.message || 'Failed to update password.'
  } finally {
    saving.value = false
  }
}

const handleResendVerification = async () => {
  if (!user.value?.email) return
  resending.value = true
  resendSuccessMsg.value = ''
  errorMsg.value = ''

  try {
    await authApi.resendVerification(user.value.email)
    resendSuccessMsg.value = 'Verification link sent to your email.'
  } catch (err) {
    errorMsg.value = err.message || 'Failed to resend verification link.'
  } finally {
    resending.value = false
  }
}

const handleLogout = () => {
  authStore.clearSession()
  authStore.closeProfileModal()
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
  border: 1px solid #CCCCCC;
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  padding: 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  font-family: var(--font-sans, "Space Grotesk", system-ui, sans-serif);
  animation: modalEnter 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalEnter {
  from { opacity: 0; transform: scale(0.96) translateY(8px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 18px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #888888;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #000000;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.avatar-circle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #000000;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono, monospace);
  font-weight: 700;
  font-size: 1.15rem;
}

.profile-info {
  flex: 1;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #000000;
  margin: 0;
  letter-spacing: -0.01em;
}

.badge {
  font-family: var(--font-mono, monospace);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.verified-badge {
  background: #F0FFF4;
  color: #2E7D32;
  border: 1px solid #B8E8C4;
}

.unverified-badge {
  background: #FFFDF0;
  color: #A08940;
  border: 1px solid #F0E4B0;
}

.user-email {
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  color: #666666;
  margin: 4px 0 0;
}

.unverified-banner {
  background: #FFFDF0;
  border: 1px solid #F0E4B0;
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-size: 0.82rem;
  color: #A08940;
}

.resend-action-btn {
  background: #000000;
  color: #FFFFFF;
  border: none;
  border-radius: 4px;
  padding: 5px 12px;
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.resend-action-btn:hover:not(:disabled) {
  background: #FF4500;
}

.settings-tabs {
  display: flex;
  border-bottom: 1px solid #E5E5E5;
  margin-bottom: 16px;
}

.tab-item {
  flex: 1;
  padding: 9px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
  font-weight: 700;
  color: #888888;
  cursor: pointer;
  margin-bottom: -1px;
  transition: all 0.2s ease;
}

.tab-item.active {
  color: #000000;
  border-bottom-color: #000000;
}

.section-hint {
  font-size: 0.82rem;
  color: #666666;
  line-height: 1.45;
  margin-bottom: 14px;
}

.current-key-badge {
  background: #F0FFF4;
  border: 1px solid #B8E8C4;
  border-radius: 8px;
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.key-status-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.key-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2E7D32;
}

.key-status-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 600;
  color: #2E7D32;
}

.remove-key-btn {
  background: transparent;
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 4px;
  padding: 3px 8px;
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.remove-key-btn:hover {
  background: #FEE2E2;
}

.provider-preset-row {
  margin-bottom: 14px;
}

.preset-label {
  display: block;
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  letter-spacing: 0.05em;
  color: #666666;
  margin-bottom: 6px;
  font-weight: 700;
}

.preset-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.preset-btn {
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  padding: 5px 12px;
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 600;
  color: #000000;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-btn:hover {
  background: #F0F0F0;
  border-color: #000000;
}

.preset-btn.active {
  background: #000000;
  color: #FFFFFF;
  border-color: #000000;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-label {
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 700;
  color: #000000;
}

.input-field {
  padding: 9px 12px;
  background: #FAFAFA;
  border: 1px solid #DDDDDD;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #000000;
  background: #FFFFFF;
}

.password-wrapper {
  display: flex;
  gap: 8px;
}

.password-wrapper .input-field {
  flex: 1;
}

.toggle-btn {
  background: #FAFAFA;
  border: 1px solid #DDDDDD;
  border-radius: 6px;
  padding: 0 12px;
  font-family: var(--font-mono, monospace);
  font-size: 0.8rem;
  color: #000000;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background: #E5E5E5;
}

.auto-detected-badge {
  background: #F0FFF4;
  border: 1px solid #B8E8C4;
  border-radius: 6px;
  padding: 6px 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.badge-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2E7D32;
  flex-shrink: 0;
}

.badge-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 600;
  color: #2E7D32;
}

.advanced-section {
  border: 1px dashed #CCCCCC;
  border-radius: 8px;
  padding: 8px 12px;
  background: #FAFAFA;
  margin-top: 4px;
}

.advanced-toggle {
  background: transparent;
  border: none;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 600;
  color: #000000;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.15s ease;
}

.primary-btn {
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  border-radius: 6px;
  padding: 10px;
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 6px;
  transition: all 0.2s ease;
}

.primary-btn:hover:not(:disabled) {
  background: #FF4500;
  border-color: #FF4500;
}

.primary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.alert {
  padding: 8px 12px;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.8rem;
  margin-bottom: 12px;
}

.error-alert {
  background: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FCA5A5;
}

.success-alert {
  background: #F0FFF4;
  color: #2E7D32;
  border: 1px solid #B8E8C4;
}

.modal-footer {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #E5E5E5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.admin-wishlist-pill {
  background: #000000;
  color: #ffffff;
  border: 1px solid #000000;
  border-radius: 6px;
  padding: 6px 14px;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.admin-wishlist-pill:hover {
  background: #333333;
}

.logout-btn {
  background: transparent;
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 6px;
  padding: 6px 14px;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #FEF2F2;
}

/* Plan & usage tab */
.plan-tab .section-hint {
  margin-bottom: 14px;
}

.plan-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  background: #fafafa;
}

.plan-summary.is-paid {
  border-color: #c9e8d3;
  background: #f4fbf6;
}

.plan-summary-name {
  font-family: var(--font-display, 'Space Grotesk', sans-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: #111111;
}

.plan-summary-meta {
  margin-top: 3px;
  color: #777777;
  font-size: 0.78rem;
}

.plan-status-badge {
  flex-shrink: 0;
  padding: 4px 9px;
  border: 1px solid #dddddd;
  border-radius: 999px;
  background: #ffffff;
  color: #555555;
  font-family: var(--font-mono, monospace);
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.usage-block {
  margin-top: 20px;
}

.usage-row,
.usage-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #555555;
  font-size: 0.76rem;
}

.usage-track {
  height: 7px;
  margin: 8px 0;
  overflow: hidden;
  border-radius: 999px;
  background: #eeeeee;
}

.usage-fill {
  height: 100%;
  border-radius: 999px;
  background: #111111;
  transition: width 0.3s ease;
}

.usage-foot {
  color: #888888;
  font-size: 0.7rem;
}

.unlimited-note {
  margin-top: 20px;
  padding: 12px 14px;
  border: 1px dashed #cccccc;
  border-radius: 8px;
  color: #555555;
  font-size: 0.78rem;
}

.plan-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 22px;
}

.plan-actions .primary-btn {
  width: 100%;
}

.plan-actions .primary-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.secondary-plan-btn {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #dddddd;
  border-radius: 8px;
  background: #ffffff;
  color: #555555;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}

.secondary-plan-btn:hover {
  border-color: #999999;
  color: #111111;
}

.plan-note {
  margin: 14px 0 0;
  color: #888888;
  font-size: 0.72rem;
  line-height: 1.5;
}
</style>
