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

        <!-- Current Key Status Badge -->
        <div v-if="user?.has_custom_api_key" class="current-key-badge">
          <div class="key-status-left">
            <span class="key-dot"></span>
            <span class="key-status-text">Personal LLM API Key Configured</span>
          </div>
          <button type="button" class="remove-key-btn" @click="handleClearKey" :disabled="saving">
            {{ saving ? 'Removing...' : 'Remove Key' }}
          </button>
        </div>

        <!-- Quick Provider Presets -->
        <div class="provider-preset-row">
          <span class="preset-label font-microgramma">PROVIDER:</span>
          <div class="preset-buttons">
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'auto' }"
              @click="applyPreset('auto')"
            >
              Auto-Detect
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'openrouter' }"
              @click="applyPreset('openrouter')"
            >
              OpenRouter
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'nvidia' }"
              @click="applyPreset('nvidia')"
            >
              NVIDIA NIM
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'alibaba' }"
              @click="applyPreset('alibaba')"
            >
              Alibaba Cloud
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'groq' }"
              @click="applyPreset('groq')"
            >
              Groq
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'openai' }"
              @click="applyPreset('openai')"
            >
              OpenAI
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'deepseek' }"
              @click="applyPreset('deepseek')"
            >
              DeepSeek
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'gemini' }"
              @click="applyPreset('gemini')"
            >
              Gemini
            </button>
            <button 
              type="button" 
              class="preset-btn" 
              :class="{ active: selectedPreset === 'custom' }"
              @click="applyPreset('custom')"
            >
              Custom
            </button>
          </div>
        </div>

        <form @submit.prevent="saveByokSettings" class="settings-form">
          <div class="form-group">
            <label class="form-label">API Key (Any Provider)</label>
            <div class="password-wrapper">
              <input
                v-model="byokForm.apiKey"
                :type="showKey ? 'text' : 'password'"
                placeholder="Paste your API key (OpenRouter, NVIDIA, Alibaba, Groq, OpenAI...)"
                class="input-field"
                @input="handleKeyInput"
              />
              <button type="button" class="toggle-btn" @click="showKey = !showKey">
                {{ showKey ? 'Hide' : 'Show' }}
              </button>
            </div>
            <!-- Auto-detection badge -->
            <div v-if="detectedBadge" class="auto-detected-badge">
              <span class="badge-dot"></span>
              <span class="badge-text">{{ detectedBadge }}</span>
            </div>
          </div>

          <!-- Collapsible Advanced Settings -->
          <div class="advanced-section">
            <button type="button" class="advanced-toggle" @click="showAdvanced = !showAdvanced">
              <span>⚙️ Advanced Settings (Base URL & Model Override)</span>
              <span class="toggle-arrow">{{ showAdvanced ? '▲' : '▼' }}</span>
            </button>

            <div v-if="showAdvanced" class="advanced-body">
              <div class="form-group">
                <label class="form-label">API Base URL</label>
                <input
                  v-model="byokForm.baseUrl"
                  type="text"
                  placeholder="https://api.openai.com/v1"
                  class="input-field"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Model Selection</label>
                <select v-model="selectedModelOption" @change="onModelSelectChange" class="input-field select-field">
                  <option v-for="opt in currentProviderModels" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
                <input
                  v-if="selectedModelOption === 'custom'"
                  v-model="byokForm.modelName"
                  type="text"
                  placeholder="e.g. meta/llama-3.1-8b-instruct, qwen-plus"
                  class="input-field custom-model-input"
                  style="margin-top: 8px;"
                />
              </div>
            </div>
          </div>

          <div class="byok-actions">
            <button 
              type="button" 
              class="test-probe-btn" 
              :disabled="probing || !byokForm.apiKey.trim()"
              @click="testAndVerifyKey"
            >
              {{ probing ? 'Verifying...' : '⚡ Test Connection' }}
            </button>
            <button type="submit" class="primary-btn" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save API Key Settings' }}
            </button>
          </div>
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

const selectedPreset = ref('auto')
const selectedModelOption = ref('gpt-4o-mini')
const showAdvanced = ref(false)
const probing = ref(false)
const detectedBadge = ref('')

const providerModels = {
  auto: [
    { label: 'Auto-Select Best Model (Recommended)', value: 'auto' }
  ],
  openrouter: [
    { label: 'openai/gpt-4o-mini (Recommended - Low Cost & Fast)', value: 'openai/gpt-4o-mini' },
    { label: 'google/gemma-4-26b-a4b-it:free (100% Free Tier - $0)', value: 'google/gemma-4-26b-a4b-it:free' },
    { label: 'google/gemini-2.0-flash-001 (Ultra Fast)', value: 'google/gemini-2.0-flash-001' },
    { label: 'meta-llama/llama-3.3-70b-instruct', value: 'meta-llama/llama-3.3-70b-instruct' },
    { label: 'anthropic/claude-3.5-haiku', value: 'anthropic/claude-3.5-haiku' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  nvidia: [
    { label: 'meta/llama-3.1-8b-instruct (Free Credits - Ultra Fast Default)', value: 'meta/llama-3.1-8b-instruct' },
    { label: 'nvidia/llama-3.1-nemotron-70b-instruct', value: 'nvidia/llama-3.1-nemotron-70b-instruct' },
    { label: 'meta/llama-3.3-70b-instruct', value: 'meta/llama-3.3-70b-instruct' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  alibaba: [
    { label: 'qwen-plus (Free Trial Credits - Balanced Default)', value: 'qwen-plus' },
    { label: 'qwen-turbo (Free Trial Credits - Ultra Fast)', value: 'qwen-turbo' },
    { label: 'qwen-max (Deep Reasoning)', value: 'qwen-max' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  groq: [
    { label: 'openai/gpt-oss-20b (100% Free Tier - Verified Active Default)', value: 'openai/gpt-oss-20b' },
    { label: 'llama-3.1-8b-instant (100% Free Tier - 8B Instant)', value: 'llama-3.1-8b-instant' },
    { label: 'llama-3.3-70b-versatile (100% Free Tier - 70B Tier)', value: 'llama-3.3-70b-versatile' },
    { label: 'mixtral-8x7b-32768 (100% Free Tier - 32k Context)', value: 'mixtral-8x7b-32768' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  openai: [
    { label: 'gpt-4o-mini (Recommended - Low Cost & Fast)', value: 'gpt-4o-mini' },
    { label: 'gpt-4o (High Intelligence)', value: 'gpt-4o' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  deepseek: [
    { label: 'deepseek-chat (V3 - Ultra Low Cost Default)', value: 'deepseek-chat' },
    { label: 'deepseek-reasoner (R1 - Deep Thinking)', value: 'deepseek-reasoner' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  gemini: [
    { label: 'gemini-1.5-flash (100% Free Tier Default - 15 RPM)', value: 'gemini-1.5-flash' },
    { label: 'gemini-2.0-flash (100% Free Tier - Ultra Fast)', value: 'gemini-2.0-flash' },
    { label: 'gemini-1.5-pro (100% Free Tier - High Intelligence)', value: 'gemini-1.5-pro' },
    { label: 'Custom Model...', value: 'custom' }
  ],
  custom: [
    { label: 'Custom Model...', value: 'custom' }
  ]
}

const currentProviderModels = computed(() => {
  return providerModels[selectedPreset.value] || providerModels.custom
})

const detectProviderKey = (key) => {
  const k = (key || '').trim()
  if (!k) return null
  if (k.startsWith('nvapi-')) {
    return {
      preset: 'nvidia',
      name: 'NVIDIA NIM',
      baseUrl: 'https://integrate.api.nvidia.com/v1',
      model: 'meta/llama-3.1-8b-instruct'
    }
  }
  if (k.startsWith('sk-or-v1-') || k.startsWith('sk-or-')) {
    return {
      preset: 'openrouter',
      name: 'OpenRouter',
      baseUrl: 'https://openrouter.ai/api/v1',
      model: 'openai/gpt-4o-mini'
    }
  }
  if (k.startsWith('gsk_')) {
    return {
      preset: 'groq',
      name: 'Groq',
      baseUrl: 'https://api.groq.com/openai/v1',
      model: 'openai/gpt-oss-20b'
    }
  }
  if (k.startsWith('AIzaSy')) {
    return {
      preset: 'gemini',
      name: 'Google Gemini',
      baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai/',
      model: 'gemini-1.5-flash'
    }
  }
  if (k.startsWith('pplx-')) {
    return {
      preset: 'custom',
      name: 'Perplexity',
      baseUrl: 'https://api.perplexity.ai',
      model: 'sonar'
    }
  }
  if (k.startsWith('csk-')) {
    return {
      preset: 'custom',
      name: 'Cerebras',
      baseUrl: 'https://api.cerebras.ai/v1',
      model: 'llama3.1-8b'
    }
  }
  if (k.startsWith('sk-proj-') || k.startsWith('sk-')) {
    return {
      preset: 'openai',
      name: 'OpenAI',
      baseUrl: 'https://api.openai.com/v1',
      model: 'gpt-4o-mini'
    }
  }
  return null
}

const handleKeyInput = () => {
  if (selectedPreset.value === 'auto' || selectedPreset.value === 'custom') {
    const detected = detectProviderKey(byokForm.apiKey)
    if (detected) {
      selectedPreset.value = detected.preset
      byokForm.baseUrl = detected.baseUrl
      byokForm.modelName = detected.model
      selectedModelOption.value = detected.model
      detectedBadge.value = `${detected.name} Detected • Configured ${detected.model}`
    } else {
      detectedBadge.value = ''
    }
  }
}

const onModelSelectChange = () => {
  if (selectedModelOption.value !== 'custom') {
    byokForm.modelName = selectedModelOption.value
  } else {
    byokForm.modelName = ''
  }
}

const applyPreset = (preset) => {
  selectedPreset.value = preset
  detectedBadge.value = ''
  if (preset === 'auto') {
    handleKeyInput()
  } else if (preset === 'openrouter') {
    byokForm.baseUrl = 'https://openrouter.ai/api/v1'
    selectedModelOption.value = 'openai/gpt-4o-mini'
    byokForm.modelName = 'openai/gpt-4o-mini'
  } else if (preset === 'nvidia') {
    byokForm.baseUrl = 'https://integrate.api.nvidia.com/v1'
    selectedModelOption.value = 'meta/llama-3.1-8b-instruct'
    byokForm.modelName = 'meta/llama-3.1-8b-instruct'
  } else if (preset === 'alibaba') {
    byokForm.baseUrl = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
    selectedModelOption.value = 'qwen-plus'
    byokForm.modelName = 'qwen-plus'
  } else if (preset === 'groq') {
    byokForm.baseUrl = 'https://api.groq.com/openai/v1'
    selectedModelOption.value = 'openai/gpt-oss-20b'
    byokForm.modelName = 'openai/gpt-oss-20b'
  } else if (preset === 'openai') {
    byokForm.baseUrl = 'https://api.openai.com/v1'
    selectedModelOption.value = 'gpt-4o-mini'
    byokForm.modelName = 'gpt-4o-mini'
  } else if (preset === 'deepseek') {
    byokForm.baseUrl = 'https://api.deepseek.com/v1'
    selectedModelOption.value = 'deepseek-chat'
    byokForm.modelName = 'deepseek-chat'
  } else if (preset === 'gemini') {
    byokForm.baseUrl = 'https://generativelanguage.googleapis.com/v1beta/openai/'
    selectedModelOption.value = 'gemini-1.5-flash'
    byokForm.modelName = 'gemini-1.5-flash'
  } else if (preset === 'custom') {
    selectedModelOption.value = 'custom'
  }
}

const testAndVerifyKey = async () => {
  if (!byokForm.apiKey.trim()) return
  probing.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    const res = await authApi.probeLlmKey({
      api_key: byokForm.apiKey.trim(),
      base_url: byokForm.baseUrl.trim() || undefined,
      model: byokForm.modelName.trim() || undefined,
      hint_provider: selectedPreset.value !== 'auto' ? selectedPreset.value : undefined
    })
    const data = (res && res.data) ? res.data : res
    if (data?.success) {
      successMsg.value = data.message || `✓ Verified active with ${data.provider_name}!`
      if (data.base_url) byokForm.baseUrl = data.base_url
      if (data.model) {
        byokForm.modelName = data.model
        selectedModelOption.value = data.model
      }
      if (data.provider) selectedPreset.value = data.provider
      detectedBadge.value = `${data.provider_name} Live Verified • Model: ${data.model}`
    } else {
      errorMsg.value = data?.error || 'Verification failed. Please check the key.'
    }
  } catch (err) {
    errorMsg.value = err.message || err.response?.data?.error || 'Key probe connection failed.'
  } finally {
    probing.value = false
  }
}

const byokForm = reactive({
  apiKey: '',
  baseUrl: user.value?.custom_llm_base_url || 'https://api.openai.com/v1',
  modelName: user.value?.custom_llm_model_name || 'gpt-4o-mini'
})

const passForm = reactive({
  currentPassword: '',
  newPassword: ''
})

watch(
  () => authStore.state.profileModalOpen,
  (isOpen) => {
    if (isOpen && user.value) {
      byokForm.baseUrl = user.value.custom_llm_base_url || 'https://api.openai.com/v1'
      byokForm.modelName = user.value.custom_llm_model_name || 'gpt-4o-mini'
      if (user.value.custom_llm_base_url?.includes('groq.com')) {
        selectedPreset.value = 'groq'
      } else if (user.value.custom_llm_base_url?.includes('deepseek.com')) {
        selectedPreset.value = 'deepseek'
      } else {
        selectedPreset.value = 'openai'
      }
      const allKnown = Object.values(providerModels).flat().map(m => m.value)
      if (allKnown.includes(byokForm.modelName)) {
        selectedModelOption.value = byokForm.modelName
      } else {
        selectedModelOption.value = 'custom'
      }
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

const handleClearKey = async () => {
  saving.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const res = await authApi.updateProfile({
      custom_llm_api_key: ''
    })
    if (res.user) {
      authStore.updateUser(res.user)
    }
    successMsg.value = 'Custom API key removed. Using platform defaults.'
    byokForm.apiKey = ''
  } catch (err) {
    errorMsg.value = err.message || 'Failed to remove API key.'
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
  font-family: 'Microgramma', sans-serif;
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

.current-key-badge {
  background: #F0FDF4;
  border: 1px solid #86EFAC;
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
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #16A34A;
}

.key-status-text {
  font-size: 0.8rem;
  font-weight: 600;
  color: #166534;
}

.remove-key-btn {
  background: transparent;
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 5px;
  padding: 3px 8px;
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
  font-size: 0.68rem;
  letter-spacing: 0.05em;
  color: #526361;
  margin-bottom: 6px;
  font-weight: 700;
}

.preset-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-btn {
  background: #F4F6F6;
  border: 1px solid rgba(7, 65, 57, 0.15);
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #2D3E3B;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-btn:hover {
  background: #E8ECEB;
  border-color: #074139;
}

.preset-btn.active {
  background: #074139;
  color: #A2F1DF;
  border-color: #074139;
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

.auto-detected-badge {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 6px;
  padding: 6px 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
  flex-shrink: 0;
}

.badge-text {
  font-size: 0.78rem;
  font-weight: 600;
  color: #065F46;
}

.advanced-section {
  border: 1px dashed rgba(7, 65, 57, 0.2);
  border-radius: 8px;
  padding: 8px 12px;
  background: #FAFDFB;
  margin-top: 4px;
}

.advanced-toggle {
  background: transparent;
  border: none;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 600;
  color: #074139;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.15s ease;
}

.advanced-toggle:hover {
  color: #0B6E60;
}

.toggle-arrow {
  font-size: 0.7rem;
  color: #526361;
}

.advanced-body {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid rgba(7, 65, 57, 0.1);
}

.select-field {
  background: #FFFFFF;
  cursor: pointer;
}

.byok-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 8px;
}

.test-probe-btn {
  background: transparent;
  border: 1px solid #074139;
  color: #074139;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.test-probe-btn:hover:not(:disabled) {
  background: rgba(7, 65, 57, 0.08);
}

.test-probe-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.byok-actions .primary-btn {
  flex: 1;
  margin-top: 0;
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
  transition: opacity 0.15s ease;
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
