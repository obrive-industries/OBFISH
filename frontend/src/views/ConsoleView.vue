<template>
  <div class="console-container">
    <!-- Minimal Application Header (Full-width sticky Obrive header) -->
    <header class="console-navbar">
      <div class="nav-left">
        <router-link to="/" class="brand-link" title="Return to Brain Home">
          <img src="../assets/icons/obrive-logo.svg" alt="Brain Logo" class="brand-logo-img" />
          <span class="brand-name font-microgramma">BRAIN</span>
          <span class="console-tag font-microgramma">CONSOLE</span>
        </router-link>

        <nav class="console-nav-links">
          <a href="#history" class="console-nav-link font-microgramma" @click.prevent="scrollToHistory">Simulation History</a>
        </nav>
      </div>

      <div class="nav-right">
        <!-- User Profile Pill (Only shown when authenticated) -->
        <div v-if="authStore.isAuthenticated.value" class="user-pill" @click="authStore.openProfileModal" title="Account & Settings">
          <div class="avatar">{{ userInitials }}</div>
          <span class="user-name">{{ authStore.user.value?.full_name || 'My Account' }}</span>
          <span v-if="authStore.isVerified.value" class="status-dot verified" title="Email Verified"></span>
          <span v-else class="status-dot unverified" title="Verification Pending"></span>
        </div>

        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="link-obrive font-microgramma">
          Explore Obrive <span class="arrow">↗</span>
        </a>
      </div>
    </header>

    <!-- Obrive Signature Mint Accent Gradient Hero Section (Clean & uncluttered, matching Landing Page Hero) -->
    <section class="console-hero">
      <div class="hero-container">
        <!-- Category Badge Pill with Official RoundedBallIcon -->
        <div class="brand-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-michroma">Predictive Console</span>
        </div>

        <!-- Main Title matching Landing Page Hero -->
        <h1 class="hero-title font-microgramma">
          Predictive Console
        </h1>

        <!-- Subtitle matching Landing Page Hero typography -->
        <p class="hero-subtitle font-michroma">
          Deploy multi-agent simulation swarms, upload reality seed documents, and stress-test strategic hypotheses before real-world execution.
        </p>
      </div>
    </section>

    <!-- Main Workspace -->
    <main class="console-main">
      <!-- Status Banner if email not verified -->
      <div v-if="authStore.isAuthenticated.value && !authStore.isVerified.value" class="verify-banner">
        <span class="banner-icon">⚠️</span>
        <span class="banner-text">
          Your email <strong>{{ authStore.user.value?.email }}</strong> is not verified yet. Enter the 6-digit code sent to your email to enable engine simulation runs.
        </span>
        <div class="banner-actions">
          <button class="banner-btn" @click="openOtpModal">Enter Code</button>
          <button class="banner-btn-secondary" @click="handleResendVerification" :disabled="resending">
            {{ resending ? 'Sending...' : 'Resend Code' }}
          </button>
        </div>
      </div>

      <!-- Double Panel Console Layout -->
      <div class="console-grid">
        <!-- Left Panel: System Ready & 5 Workflow Steps -->
        <div class="left-panel obrive-card">
          <div class="panel-badge">
            <span class="live-dot"></span>
            <span class="font-microgramma">SYSTEM READY</span>
          </div>

          <h2 class="panel-heading font-microgramma">System Ready</h2>
          <p class="panel-sub">
            BRAIN is primed to explore possibilities, stress-test variables, and simulate potential strategic outcomes.
          </p>

          <!-- System Readiness Metrics Row -->
          <div class="metrics-row">
            <div class="metric-card">
              <span class="metric-value font-microgramma">LOW COST</span>
              <span class="metric-label">High token efficiency & edge caching</span>
            </div>
            <div class="metric-card">
              <span class="metric-value font-microgramma">HIGH AVAIL</span>
              <span class="metric-label">Autonomous swarm cluster</span>
            </div>
            <div class="metric-card">
              <span class="metric-value font-microgramma">DETERMINISTIC</span>
              <span class="metric-label">Consensus verification</span>
            </div>
          </div>

          <!-- Workflow Steps (01 to 05) from docx -->
          <div class="workflow-box">
            <div class="workflow-header">
              <span class="diamond-icon">◇</span>
              <span class="workflow-title font-microgramma">Workflow Architecture</span>
            </div>

            <div class="workflow-steps-list">
              <div 
                v-for="step in consoleSteps" 
                :key="step.number"
                class="console-step-item"
              >
                <span class="step-idx font-microgramma">{{ step.number }}</span>
                <div class="step-meta">
                  <h4 class="step-name font-microgramma">{{ step.title }}</h4>
                  <p class="step-detail">{{ step.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel: Interaction Console Workspace -->
        <div class="right-panel">
          <div class="console-box obrive-card">
            <!-- Upload Section -->
            <div class="console-section">
              <div class="section-label-bar">
                <span class="label-title font-microgramma">REALITY SEED</span>
                <span class="label-hint">PDF, DOCX, MD, TXT (Optional, up to 50MB)</span>
              </div>

              <div 
                class="upload-dropzone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.docx,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />

                <div v-if="files.length === 0" class="upload-empty">
                  <div class="upload-icon-circle">↑</div>
                  <span class="upload-text-bold">Drag and drop documents here (optional)</span>
                  <span class="upload-text-sub">or enter text hypothesis below</span>
                </div>

                <div v-else class="file-chips-grid">
                  <div v-for="(file, index) in files" :key="index" class="file-chip">
                    <span class="chip-icon">📄</span>
                    <span class="chip-name" :title="file.name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="chip-remove" title="Remove file">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Parameters Section -->
            <div class="console-section input-section">
              <div class="section-label-bar">
                <span class="label-title font-microgramma">SIMULATION REQUIREMENT & HYPOTHESIS</span>
                <span class="label-hint">Natural language prompt</span>
              </div>

              <div class="textarea-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="scenario-input"
                  placeholder="Describe the scenario, market situation, key stakeholder dynamics, or critical decision you need to simulate..."
                  rows="6"
                  :disabled="loading"
                ></textarea>

                <div class="engine-badge-pill">
                  <span class="badge-dot"></span>
                  <span class="font-microgramma">OB-SWARM INTELLIGENCE</span>
                </div>
              </div>
            </div>

            <!-- BYOK Key Status Bar -->
            <div 
              class="byok-status-card"
              :class="{ 'has-key': authStore.user.value?.has_custom_api_key }"
              @click="openByokSettings"
              title="Click to configure Bring-Your-Own-Key (BYOK) settings"
            >
              <div class="byok-card-left">
                <span class="byok-card-icon">{{ authStore.user.value?.has_custom_api_key ? '🔑' : '⚡' }}</span>
                <div class="byok-card-info">
                  <div class="byok-card-title font-microgramma">
                    {{ authStore.user.value?.has_custom_api_key ? 'LLM KEY CONFIGURED (BYOK)' : 'LLM API KEY REQUIRED (BYOK)' }}
                  </div>
                  <div class="byok-card-sub">
                    {{ authStore.user.value?.has_custom_api_key 
                      ? (authStore.user.value?.custom_llm_model_name ? `Dedicated model: ${authStore.user.value.custom_llm_model_name}` : 'Using personal provider key')
                      : 'Click to add your OpenAI, DeepSeek, or Groq API key' }}
                  </div>
                </div>
              </div>
              <button type="button" class="byok-card-btn font-microgramma">
                {{ authStore.user.value?.has_custom_api_key ? 'EDIT' : 'CONNECT KEY →' }}
              </button>
            </div>

            <!-- Launch Button Section with Obrive Animated Button styling -->
            <div class="console-section launch-section">
              <button 
                class="btn-start-engine font-microgramma"
                :class="{ 'btn-ready': !loading }"
                @click="handleStartEngine"
                :disabled="loading"
              >
                <span v-if="!loading" class="btn-text-content">
                  <span class="btn-label">Start Engine</span>
                  <span class="btn-arrow-wrap">
                    <RightAnimateIcon color="primary" :size="16" />
                  </span>
                </span>
                <span v-else class="btn-text-content">
                  <span>Initializing Swarm...</span>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- History Database Section -->
      <section id="history" class="history-wrapper">
        <HistoryDatabase />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import RightAnimateIcon from '../components/common/RightAnimateIcon.vue'
import RoundedBallIcon from '../components/common/RoundedBallIcon.vue'
import authStore from '../store/auth'
import authApi from '../api/auth'
import { savePendingUpload, setPendingUpload, getPendingUpload } from '../utils/pendingUpload.js'

const router = useRouter()

// Form Data & Files
const formData = ref({
  simulationRequirement: ''
})
const files = ref([])
const loading = ref(false)
const resending = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)

// 5 Workflow Steps directly from docx paragraphs 101-116
const consoleSteps = [
  {
    number: '01',
    title: 'Scenario & Context Building',
    description: 'Ingest source materials and data as a structured foundation for simulation.'
  },
  {
    number: '02',
    title: 'Entity & Behaviour Modelling',
    description: 'Map key entities, relationships, and stakeholder personas.'
  },
  {
    number: '03',
    title: 'Run Simulation',
    description: 'Deploy multi-agent debates and social interactions across rounds.'
  },
  {
    number: '04',
    title: 'Insights & Report Generation',
    description: 'Synthesize predictive reports highlighting risks and emerging patterns.'
  },
  {
    number: '05',
    title: 'Explore & Refine',
    description: 'Deep interactive interviews with personas to test strategic hypotheses.'
  }
]

onMounted(async () => {
  // Check if there was pending upload saved before auth
  const pending = await getPendingUpload()
  if (pending && pending.isPending) {
    if (pending.simulationRequirement) {
      formData.value.simulationRequirement = pending.simulationRequirement
    }
    if (pending.files && pending.files.length > 0) {
      files.value = pending.files
    }
  }
})

// Watch auth state to restore pending dossier if login happened in-place
watch(() => authStore.isAuthenticated.value, async (isAuth) => {
  if (isAuth) {
    const pending = await getPendingUpload()
    if (pending && pending.isPending) {
      if (pending.simulationRequirement && !formData.value.simulationRequirement) {
        formData.value.simulationRequirement = pending.simulationRequirement
      }
      if (pending.files && pending.files.length > 0 && files.value.length === 0) {
        files.value = pending.files
      }
    }
  }
})

const openOtpModal = () => {
  authStore.openAuthModal(
    'verify-otp',
    'Enter the 6-digit verification code sent to your email.',
    authStore.user.value?.email
  )
}

const handleResendVerification = async () => {
  if (!authStore.user.value?.email) return
  resending.value = true
  try {
    await authApi.resendVerification(authStore.user.value.email)
    openOtpModal()
  } catch (err) {
    alert(err.message || 'Failed to resend verification code.')
  } finally {
    resending.value = false
  }
}

const userInitials = computed(() => {
  const name = authStore.user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const hasCustomKey = computed(() => {
  const customKey = localStorage.getItem('brain_custom_llm_key') || localStorage.getItem('obmind_custom_llm_key')
  return Boolean(customKey && customKey.trim().length > 5)
})

const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim().length > 0
})

const openByokSettings = () => {
  if (authStore.isAuthenticated.value) {
    authStore.openProfileModal()
  } else {
    authStore.openAuthModal('login', 'Sign in to configure your personal Bring-Your-Own-Key (BYOK) LLM provider.')
  }
}

const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (e) => {
  const selected = Array.from(e.target.files)
  addFiles(selected)
}

const handleDragOver = () => {
  if (!loading.value) isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  const dropped = Array.from(e.dataTransfer.files)
  addFiles(dropped)
}

const MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024 // 50MB
const addFiles = (newFiles) => {
  const valid = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    const isFormatOk = ['pdf', 'docx', 'md', 'txt'].includes(ext)
    const isSizeOk = file.size <= MAX_FILE_SIZE_BYTES
    if (!isSizeOk) {
      alert(`File "${file.name}" exceeds the 50MB size limit.`)
    }
    return isFormatOk && isSizeOk
  })
  files.value.push(...valid)
}

const removeFile = (idx) => {
  files.value.splice(idx, 1)
}

const scrollToHistory = () => {
  const el = document.getElementById('history')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

// Start Engine with Authentication Interception Gate
const handleStartEngine = async () => {
  if (loading.value) return

  // 1. Authentication Gate Check: If not signed in, open Sign In / Register popup
  if (!authStore.isAuthenticated.value) {
    if (formData.value.simulationRequirement?.trim() || files.value.length > 0) {
      await savePendingUpload(files.value, formData.value.simulationRequirement)
    }
    authStore.openAuthModal(
      'login',
      'Please sign in or create an account to start your simulation engine.'
    )
    return
  }

  // 2. Email Verification Check -> Direct OTP code prompt
  if (!authStore.isVerified.value) {
    authStore.openAuthModal(
      'verify-otp',
      'Please enter the 6-digit verification code sent to your email to activate and start the engine.',
      authStore.user.value?.email
    )
    return
  }

  // 3. Scenario & Hypothesis Check
  if (!formData.value.simulationRequirement?.trim()) {
    alert('Please describe your simulation scenario, requirement, or hypothesis to start the engine.')
    return
  }

  // 4. Bring Your Own Key (BYOK) Gate Check
  if (!authStore.user.value?.has_custom_api_key) {
    await savePendingUpload(files.value, formData.value.simulationRequirement)
    authStore.openProfileModal()
    return
  }

  // Cache user's inputs in IndexedDB pending store immediately so nothing is lost
  await savePendingUpload(files.value, formData.value.simulationRequirement)

  // 5. Authenticated, Verified & BYOK Key Configured -> Navigate to Process View
  loading.value = true
  router.push({
    name: 'Process',
    params: { projectId: 'new' }
  })
}
</script>

<style scoped>
.console-container {
  min-height: 100vh;
  background-color: #F8FCFA;
  color: #074139;
  display: flex;
  flex-direction: column;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Minimal Application Header (Full-width sticky) */
.console-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 32px;
  background: rgba(255, 255, 255, 0.94);
  border-bottom: 1px solid rgba(7, 65, 57, 0.12);
  backdrop-filter: blur(14px);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 2px 12px rgba(7, 65, 57, 0.04);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #074139;
}

.brand-logo-img {
  height: 28px;
  width: auto;
}

.brand-name {
  font-weight: 800;
  font-size: 1.15rem;
  letter-spacing: 0.05em;
  color: #074139;
}

.console-tag {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 3px 8px;
  background: rgba(162, 241, 223, 0.4);
  border: 1px solid rgba(7, 65, 57, 0.22);
  color: #074139;
  border-radius: 6px;
  letter-spacing: 0.08em;
}

.console-nav-links {
  display: flex;
  gap: 20px;
  margin-left: 8px;
}

.console-nav-link {
  color: #526361;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
  letter-spacing: 0.04em;
}

.console-nav-link:hover {
  color: #074139;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.byok-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(7, 65, 57, 0.05);
  border: 1px solid rgba(7, 65, 57, 0.16);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.byok-badge:hover {
  border-color: #074139;
  background: rgba(162, 241, 223, 0.25);
}

.byok-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #074139;
  box-shadow: 0 0 6px rgba(7, 65, 57, 0.5);
}

.byok-text {
  font-size: 0.68rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.06em;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px 5px 6px;
  background: rgba(7, 65, 57, 0.05);
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-pill:hover {
  border-color: #074139;
  background: rgba(7, 65, 57, 0.08);
}

.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #074139;
  color: #CAEDE5;
  font-size: 0.72rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #074139;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.verified {
  background: #074139;
  box-shadow: 0 0 6px rgba(7, 65, 57, 0.4);
}

.status-dot.unverified {
  background: #f59e0b;
}

.btn-signin {
  background: transparent;
  border: 1px solid #074139;
  color: #074139;
  padding: 7px 16px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-signin:hover {
  background: #074139;
  color: #CAEDE5;
}

.link-obrive {
  color: #074139;
  font-size: 0.75rem;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 9999px;
  background: rgba(162, 241, 223, 0.35);
  transition: all 0.2s ease;
}

.link-obrive:hover {
  background: #074139;
  color: #CAEDE5;
}

/* Obrive Mint Accent Gradient Hero Section (Clean & spacious, matching Landing Page Hero) */
.console-hero {
  position: relative;
  background: linear-gradient(
    90deg,
    #caede5 0%,
    #beeee3 25%,
    #b2f0e1 50%,
    #a5f1df 75%,
    #98f2dd 100%
  );
  padding: 76px 24px 68px;
  border-bottom: 1px solid rgba(7, 65, 57, 0.12);
  overflow: hidden;
}

.hero-container {
  max-width: 920px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  margin-bottom: 22px;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 10px rgba(7, 65, 57, 0.05);
}

.pill-text {
  font-family: 'Michroma', sans-serif !important;
  font-size: 0.72rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.hero-title {
  font-family: 'Microgramma', 'Microgramma Bold', 'Michroma', sans-serif !important;
  font-size: clamp(2.25rem, 4.2vw, 3.5rem);
  font-weight: 800;
  line-height: 1.16;
  color: #074139;
  margin: 0 0 20px 0;
  letter-spacing: -0.01em;
  text-transform: none;
}

.hero-subtitle {
  font-family: 'Michroma', sans-serif !important;
  font-size: clamp(0.875rem, 1.1vw, 1rem);
  line-height: 1.75;
  color: #074139;
  opacity: 0.88;
  max-width: 820px;
  margin: 0 auto;
  font-weight: 400;
  letter-spacing: 0.01em;
  text-align: center;
  text-wrap: balance;
}

/* System Readiness Metrics inside Left Panel */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 28px;
}

.metric-card {
  background: rgba(7, 65, 57, 0.035);
  border: 1px solid rgba(7, 65, 57, 0.12);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s ease;
}

.metric-card:hover {
  background: rgba(7, 65, 57, 0.06);
  border-color: rgba(7, 65, 57, 0.24);
}

.metric-value {
  font-size: 0.75rem;
  font-weight: 800;
  color: #074139;
  letter-spacing: 0.04em;
}

.metric-label {
  font-size: 0.7rem;
  color: #526361;
  line-height: 1.4;
  font-weight: 500;
}

/* Main Workspace */
.console-main {
  max-width: 1320px;
  width: 100%;
  margin: 0 auto;
  padding: 44px 24px 80px;
  flex: 1;
}

/* Email Verification Banner */
.verify-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FFFBEB;
  border: 1px solid #FCD34D;
  padding: 14px 20px;
  border-radius: 12px;
  margin-bottom: 28px;
  color: #92400E;
  font-size: 0.9rem;
}

.banner-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.banner-btn-secondary {
  background: #FEF3C7;
  border: 1px solid #F59E0B;
  color: #B45309;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.banner-btn-secondary:hover:not(:disabled) {
  background: #FDE68A;
}

.banner-btn {
  background: #074139;
  border: none;
  color: #CAEDE5;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.banner-btn:hover {
  background: #0d5c52;
}

/* Console Grid */
.console-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  align-items: stretch;
  margin-bottom: 60px;
}

/* Obrive Cards */
.obrive-card {
  background: #FFFFFF;
  border: 1.5px solid rgba(7, 65, 57, 0.16);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(7, 65, 57, 0.05);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.obrive-card:hover {
  border-color: rgba(7, 65, 57, 0.35);
  box-shadow: 0 8px 30px rgba(7, 65, 57, 0.08);
}

/* Left Panel */
.left-panel {
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-sizing: border-box;
}

.panel-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  background: rgba(162, 241, 223, 0.4);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  font-size: 0.68rem;
  font-weight: 700;
  color: #074139;
  margin-bottom: 20px;
  width: fit-content;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #074139;
  box-shadow: 0 0 6px rgba(7, 65, 57, 0.4);
}

.panel-heading {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0 0 10px 0;
  color: #074139;
  letter-spacing: 0.02em;
}

.panel-sub {
  font-size: 0.92rem;
  line-height: 1.6;
  color: #526361;
  margin: 0 0 28px 0;
}

.workflow-box {
  border-top: 1.5px solid rgba(7, 65, 57, 0.12);
  padding-top: 24px;
}

.workflow-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.diamond-icon {
  color: #074139;
  font-size: 0.85rem;
  font-weight: 800;
}

.workflow-title {
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #074139;
  text-transform: uppercase;
}

.workflow-steps-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.console-step-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 10px 14px;
  border-radius: 12px;
  background: #F9FCFB;
  border: 1px solid rgba(7, 65, 57, 0.1);
  transition: all 0.25s ease;
}

.console-step-item:hover {
  background: #F0FAF7;
  border-color: rgba(7, 65, 57, 0.28);
  transform: translateX(3px);
}

.step-idx {
  font-size: 0.85rem;
  font-weight: 800;
  color: #074139;
  background: #CAEDE5;
  padding: 4px 8px;
  border-radius: 6px;
  line-height: 1;
}

.step-meta {
  flex: 1;
}

.step-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #074139;
  margin: 0 0 4px 0;
  letter-spacing: 0.02em;
}

.step-detail {
  font-size: 0.8rem;
  line-height: 1.5;
  color: #526361;
  margin: 0;
}

/* Right Panel */
.right-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.console-box {
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
  box-sizing: border-box;
}

.console-section {
  display: flex;
  flex-direction: column;
}

.section-label-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.label-title {
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #074139;
}

.label-hint {
  font-size: 0.72rem;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

.upload-dropzone {
  min-height: 170px;
  border: 2px dashed rgba(7, 65, 57, 0.25);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  cursor: pointer;
  background: #F9FCFB;
  transition: all 0.25s ease;
}

.upload-dropzone:hover,
.upload-dropzone.drag-over {
  border-color: #074139;
  background: rgba(162, 241, 223, 0.25);
}

.upload-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.upload-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #CAEDE5;
  border: 1.5px solid #074139;
  color: #074139;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 12px;
  transition: transform 0.2s ease;
}

.upload-dropzone:hover .upload-icon-circle {
  transform: translateY(-2px);
}

.upload-text-bold {
  font-size: 0.95rem;
  font-weight: 700;
  color: #074139;
  margin-bottom: 4px;
}

.upload-text-sub {
  font-size: 0.8rem;
  color: #526361;
}

.file-chips-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
}

.file-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #EBF7F4;
  border: 1.5px solid rgba(7, 65, 57, 0.25);
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #074139;
}

.chip-name {
  max-width: 220px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chip-remove {
  background: none;
  border: none;
  color: #526361;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 2px;
  line-height: 1;
}

.chip-remove:hover {
  color: #ef4444;
}

.console-section.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.console-section.input-section .textarea-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.scenario-input {
  width: 100%;
  flex: 1;
  min-height: 200px;
  box-sizing: border-box;
  background: #F9FCFB;
  border: 1.5px solid rgba(7, 65, 57, 0.2);
  border-radius: 14px;
  padding: 16px;
  padding-bottom: 48px;
  color: #074139;
  font-family: inherit;
  font-size: 0.95rem;
  line-height: 1.6;
  outline: none;
  resize: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.scenario-input:focus {
  border-color: #074139;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.45);
  background: #FFFFFF;
}

.engine-badge-pill {
  position: absolute;
  bottom: 12px;
  right: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(7, 65, 57, 0.08);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 20px;
  font-size: 0.65rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.05em;
}

.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #074139;
}

/* BYOK Status Card */
.byok-status-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 12px 18px;
  background: #FFFBEB;
  border: 1.5px solid #FDE68A;
  border-radius: 12px;
  margin-top: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.byok-status-card:hover {
  background: #FEF3C7;
  border-color: #F59E0B;
}

.byok-status-card.has-key {
  background: #ECFDF5;
  border-color: #A7F3D0;
}

.byok-status-card.has-key:hover {
  background: #D1FAE5;
  border-color: #10B981;
}

.byok-card-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.byok-card-icon {
  font-size: 1.3rem;
  line-height: 1;
}

.byok-card-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.byok-card-title {
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #92400E;
}

.byok-status-card.has-key .byok-card-title {
  color: #065F46;
}

.byok-card-sub {
  font-size: 0.78rem;
  color: #78350F;
}

.byok-status-card.has-key .byok-card-sub {
  color: #047857;
}

.byok-card-btn {
  background: #074139;
  color: #A2F1DF;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.byok-card-btn:hover {
  background: #052e28;
}

.launch-section {
  margin-top: auto;
  padding-top: 10px;
}

/* Obrive Official Animated Button Design for Start Engine */
.btn-start-engine {
  width: 100%;
  padding: 16px 28px;
  background: rgba(7, 65, 57, 0.12);
  border: 1.5px solid rgba(7, 65, 57, 0.18);
  border-radius: 14px;
  color: #7a8d8a;
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  cursor: not-allowed;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
}

.btn-start-engine.btn-ready {
  background: #074139;
  border-color: #074139;
  color: #CAEDE5;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(7, 65, 57, 0.25);
}

.btn-start-engine.btn-ready:hover {
  background: #052e28;
  box-shadow: 0 12px 30px rgba(7, 65, 57, 0.35);
  transform: translateY(-2px);
}

.btn-text-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.btn-arrow-wrap {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.btn-start-engine.btn-ready:hover .btn-arrow-wrap {
  transform: translateX(4px);
}

/* History */
.history-wrapper {
  margin-top: 36px;
  scroll-margin-top: 80px;
}

@media (max-width: 960px) {
  .console-grid {
    grid-template-columns: 1fr;
  }

  .console-hero {
    padding: 56px 16px 48px;
  }

  .hero-title {
    font-size: 1.85rem;
  }
}

@media (max-width: 640px) {
  .metrics-row {
    grid-template-columns: 1fr;
  }
}
</style>
