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
            <h3 class="user-name">{{ user?.full_name || 'ObMind User' }}</h3>
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
          :class="['tab-item', { active: activeTab === 'byok' }]"
          @click="activeTab = 'byok'"
        >
          🔑 BYOK API Keys
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

      <!-- 1. BYOK SETTINGS TAB -->
      <div v-if="activeTab === 'byok'" class="tab-content">
        <p class="section-hint">
          Supply your own LLM provider API key (OpenAI, Groq, DeepSeek) for dedicated simulation runs.
        </p>

        <form @submit.prevent="saveByokSettings" class="settings-form">
          <div class="form-group">
            <label class="form-label">Custom LLM API Key</label>
            <div class="password-wrapper">
              <input
                v-model="byokForm.apiKey"
                :type="showKey ? 'text' : 'password'"
                placeholder="sk-..."
                class="input-field"
              />
              <button type="button" class="toggle-btn" @click="showKey = !showKey">
                {{ showKey ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">API Base URL (optional)</label>
            <input
              v-model="byokForm.baseUrl"
              type="text"
              placeholder="https://api.openai.com/v1"
              class="input-field"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Model Name (optional)</label>
            <input
              v-model="byokForm.modelName"
              type="text"
              placeholder="e.g. gpt-4o, llama-3.3-70b-versatile"
              class="input-field"
            />
          </div>

          <button type="submit" class="primary-btn" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save API Key Settings' }}
          </button>
        </form>
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

      <!-- Footer: Log out -->
      <div class="modal-footer">
        <button class="logout-btn" @click="handleLogout">
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import authStore from '../store/auth'
import authApi from '../api/auth'

const user = computed(() => authStore.user.value)
const activeTab = ref('byok')
const showKey = ref(false)
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

const byokForm = reactive({
  apiKey: '',
  baseUrl: user.value?.custom_llm_base_url || '',
  modelName: user.value?.custom_llm_model_name || ''
})

const passForm = reactive({
  currentPassword: '',
  newPassword: ''
})

watch(
  () => authStore.state.profileModalOpen,
  (isOpen) => {
    if (isOpen && user.value) {
      byokForm.baseUrl = user.value.custom_llm_base_url || ''
      byokForm.modelName = user.value.custom_llm_model_name || ''
      errorMsg.value = ''
      successMsg.value = ''
      resendSuccessMsg.value = ''
    }
  }
)

const saveByokSettings = async () => {
  saving.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const payload = {
      custom_llm_base_url: byokForm.baseUrl.trim() || null,
      custom_llm_model_name: byokForm.modelName.trim() || null
    }
    if (byokForm.apiKey.trim()) {
      payload.custom_llm_api_key = byokForm.apiKey.trim()
    }

    const res = await authApi.updateProfile(payload)
    if (res.user) {
      authStore.updateUser(res.user)
    }
    successMsg.value = 'BYOK API keys saved successfully!'
    byokForm.apiKey = ''
  } catch (err) {
    errorMsg.value = err.message || 'Failed to save API settings.'
  } finally {
    saving.value = false
  }
}

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
  max-width: 480px;
  padding: 30px;
  box-shadow: 0 20px 45px rgba(7, 65, 57, 0.2);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
  font-size: 1.6rem;
  color: #526361;
  cursor: pointer;
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
  background: #074139;
  color: #A2F1DF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Michroma', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
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
  font-size: 1.15rem;
  font-weight: 700;
  color: #074139;
  margin: 0;
}

.badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 9999px;
  letter-spacing: 0.3px;
}

.verified-badge {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #10B981;
}

.unverified-badge {
  background: #FEF3C7;
  color: #D97706;
  border: 1px solid #F59E0B;
}

.user-email {
  font-size: 0.85rem;
  color: #526361;
  margin: 2px 0 0;
}

.unverified-banner {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  font-size: 0.82rem;
  color: #92400E;
}

.resend-action-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.settings-tabs {
  display: flex;
  border-bottom: 1.5px solid rgba(7, 65, 57, 0.12);
  margin-bottom: 16px;
}

.tab-item {
  flex: 1;
  padding: 9px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 0.88rem;
  font-weight: 600;
  color: #526361;
  cursor: pointer;
  margin-bottom: -1.5px;
}

.tab-item.active {
  color: #074139;
  border-bottom-color: #074139;
}

.section-hint {
  font-size: 0.82rem;
  color: #526361;
  line-height: 1.45;
  margin-bottom: 14px;
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
  font-size: 0.8rem;
  font-weight: 600;
  color: #074139;
}

.input-field {
  padding: 9px 12px;
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 8px;
  font-size: 0.88rem;
  outline: none;
}

.password-wrapper {
  display: flex;
  gap: 8px;
}

.password-wrapper .input-field {
  flex: 1;
}

.toggle-btn {
  background: #F1FDFB;
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 8px;
  padding: 0 12px;
  font-size: 0.8rem;
  color: #074139;
  cursor: pointer;
  font-weight: 600;
}

.primary-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 8px;
  padding: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 6px;
}

.alert {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.82rem;
  margin-bottom: 12px;
}

.error-alert {
  background: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FCA5A5;
}

.success-alert {
  background: #ECFDF5;
  color: #065F46;
  border: 1px solid #6EE7B7;
}

.modal-footer {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
  display: flex;
  justify-content: flex-end;
}

.logout-btn {
  background: transparent;
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #FEF2F2;
}
</style>
