<template>
  <div class="console-container">
    <!-- Minimal Application Header (Full-width sticky Obrive header) -->
    <header class="console-navbar">
      <div class="nav-left">
        <router-link to="/" class="brand-link" title="Return to ObMind Home">
          <img src="../assets/icons/obrive-logo.svg" alt="ObMind Logo" class="brand-logo-img" />
          <span class="brand-name font-microgramma">OBMIND</span>
          <span class="console-tag font-microgramma">CONSOLE</span>
        </router-link>

        <nav class="console-nav-links">
          <router-link to="/" class="console-nav-link font-microgramma">← Landing Page</router-link>
          <a href="#history" class="console-nav-link font-microgramma" @click.prevent="scrollToHistory">Simulation History</a>
        </nav>
      </div>

      <div class="nav-right">
        <!-- BYOK Key Status Badge -->
        <div class="byok-badge" @click="openByokSettings" title="Configure Custom LLM API Key">
          <span class="byok-dot"></span>
          <span class="byok-text font-microgramma">BYOK {{ hasCustomKey ? 'ACTIVE' : 'DEFAULT' }}</span>
        </div>

        <!-- Language Switcher -->
        <LanguageSwitcher />

        <!-- User Profile Pill / Sign In -->
        <div v-if="authStore.isAuthenticated.value" class="user-pill" @click="authStore.openProfileModal">
          <div class="avatar">{{ userInitials }}</div>
          <span class="user-name">{{ authStore.user.value?.full_name || 'My Account' }}</span>
          <span v-if="authStore.isVerified.value" class="status-dot verified" title="Email Verified"></span>
          <span v-else class="status-dot unverified" title="Verification Pending"></span>
        </div>
        <button v-else class="btn-signin font-microgramma" @click="authStore.openAuthModal('login')">
          Sign In
        </button>

        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="link-obrive font-microgramma">
          Explore Obrive <span class="arrow">↗</span>
        </a>
      </div>
    </header>

    <!-- Obrive Signature Mint Accent Gradient Hero Section -->
    <section class="console-hero">
      <div class="hero-container">
        <!-- Category Badge Pill with Official RoundedBallIcon -->
        <div class="brand-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">PREDICTIVE CONSOLE // SYSTEM READY</span>
        </div>

        <!-- Microgramma Bold Main Title -->
        <h1 class="hero-title font-microgramma">
          OBMIND PREDICTIVE CONSOLE
        </h1>

        <!-- Subtitle -->
        <p class="hero-subtitle">
          Deploy multi-agent simulation swarms, upload reality seed documents, and stress-test strategic hypotheses before real-world execution.
        </p>

        <!-- System Readiness Metrics -->
        <div class="hero-metrics">
          <div class="metric-chip">
            <span class="chip-val font-microgramma">LOW COST</span>
            <span class="chip-label">High token efficiency & edge caching</span>
          </div>
          <div class="metric-chip">
            <span class="chip-val font-microgramma">HIGH AVAIL</span>
            <span class="chip-label">Autonomous swarm cluster</span>
          </div>
          <div class="metric-chip">
            <span class="chip-val font-microgramma">DETERMINISTIC</span>
            <span class="chip-label">Multi-agent consensus verification</span>
          </div>
        </div>
      </div>

      <!-- Obrive Brand Divider Line -->
      <div class="hero-divider">
        <div class="divider-inner">
          <div class="divider-badge font-microgramma">SYSTEM READY</div>
          <p class="divider-text font-microgramma">TURNING COMPLEX UNCERTAINTIES INTO PREDICTIVE DECISIONS.</p>
        </div>
      </div>
    </section>

    <!-- Main Workspace -->
    <main class="console-main">
      <!-- Status Banner if email not verified -->
      <div v-if="authStore.isAuthenticated.value && !authStore.isVerified.value" class="verify-banner">
        <span class="banner-icon">⚠️</span>
        <span class="banner-text">
          Your email <strong>{{ authStore.user.value?.email }}</strong> is not verified yet. Please check your Brevo inbox to enable engine simulation runs.
        </span>
        <div class="banner-actions">
          <button class="banner-btn-secondary" @click="handleResendVerification" :disabled="resending">
            {{ resending ? 'Sending...' : 'Resend Link' }}
          </button>
          <button class="banner-btn" @click="authStore.openProfileModal">View Profile</button>
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
            OBMIND is primed to explore possibilities, stress-test variables, and simulate potential strategic outcomes.
          </p>

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
                <span class="label-hint">PDF, DOCX, MD, TXT (up to 50MB)</span>
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
                  <span class="upload-text-bold">Drag and drop documents here</span>
                  <span class="upload-text-sub">or click to browse from device</span>
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
            <div class="console-section">
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

            <!-- Launch Button Section with Obrive Animated Button styling -->
            <div class="console-section launch-section">
              <button 
                class="btn-start-engine font-microgramma"
                :class="{ 'btn-ready': canSubmit && !loading }"
                @click="handleStartEngine"
                :disabled="!canSubmit || loading"
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
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import RightAnimateIcon from '../components/common/RightAnimateIcon.vue'
import RoundedBallIcon from '../components/common/RoundedBallIcon.vue'
import authStore from '../store/auth'
import authApi from '../api/auth'
import { setPendingUpload, getPendingUpload } from '../store/pendingUpload.js'

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
    description: 'Transform source materials, business data, research, or creative ideas into a structured foundation for simulation.'
  },
  {
    number: '02',
    title: 'Entity & Behaviour Modelling',
    description: 'Identify key entities, relationships, stakeholder perspectives, and behavioural factors relevant to your scenario.'
  },
  {
    number: '03',
    title: 'Run Simulation',
    description: 'Explore interactions, test assumptions, introduce variables, and examine how different scenarios may evolve over time.'
  },
  {
    number: '04',
    title: 'Insights & Report Generation',
    description: 'Generate structured reports highlighting potential outcomes, emerging patterns, risks, opportunities, and alternative pathways.'
  },
  {
    number: '05',
    title: 'Explore & Refine',
    description: 'Interact with simulation results, investigate individual perspectives, ask follow-up questions, and refine scenarios to uncover deeper insights.'
  }
]

onMounted(() => {
  // Check if there was pending upload saved before auth
  const pending = getPendingUpload()
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
watch(() => authStore.isAuthenticated.value, (isAuth) => {
  if (isAuth) {
    const pending = getPendingUpload()
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

const handleResendVerification = async () => {
  if (!authStore.user.value?.email) return
  resending.value = true
  try {
    await authApi.resendVerification(authStore.user.value.email)
    alert('A new verification email has been sent via Brevo. Please check your inbox.')
  } catch (err) {
    alert(err.message || 'Failed to resend verification link.')
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
  const customKey = localStorage.getItem('obmind_custom_llm_key')
  return Boolean(customKey && customKey.trim().length > 5)
})

const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim().length > 0 && files.value.length > 0
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
const handleStartEngine = () => {
  if (!canSubmit.value || loading.value) return

  // Cache user's inputs in pending store immediately so nothing is lost
  setPendingUpload(files.value, formData.value.simulationRequirement)

  // Authentication Gate Check
  if (!authStore.isAuthenticated.value) {
    authStore.openAuthModal(
      'login',
      'Please sign in to launch your simulation engine. Your scenario and documents have been saved.'
    )
    return
  }

  // Email Verification Check
  if (!authStore.isVerified.value) {
    alert('Please verify your email address via the link sent to your inbox before launching simulations.')
    return
  }

  // Authenticated & Verified -> Navigate to Process View
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

/* Obrive Mint Accent Gradient Hero Section */
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
  padding: 56px 24px 0;
  border-bottom: 1px solid rgba(7, 65, 57, 0.15);
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
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
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  margin-bottom: 20px;
  backdrop-filter: blur(8px);
}

.pill-text {
  font-size: 0.72rem;
  font-weight: 800;
  color: #074139;
  letter-spacing: 0.08em;
}

.hero-title {
  font-size: 2.3rem;
  font-weight: 800;
  line-height: 1.2;
  color: #074139;
  margin-bottom: 16px;
  letter-spacing: 0.02em;
}

.hero-subtitle {
  font-size: 0.95rem;
  line-height: 1.6;
  max-width: 780px;
  color: #074139;
  opacity: 0.88;
  margin-bottom: 32px;
  font-weight: 500;
}

.hero-metrics {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-bottom: 36px;
}

.metric-chip {
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 14px;
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 200px;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 15px rgba(7, 65, 57, 0.05);
}

.chip-val {
  font-size: 0.82rem;
  font-weight: 800;
  color: #074139;
  letter-spacing: 0.06em;
}

.chip-label {
  font-size: 0.72rem;
  color: #3f5451;
  font-weight: 500;
}

/* Obrive Brand Divider Line */
.hero-divider {
  width: 100%;
  border-top: 1.5px solid rgba(7, 65, 57, 0.22);
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.35);
}

.divider-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.divider-badge {
  background: #074139;
  color: #CAEDE5;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: 0.08em;
}

.divider-text {
  font-size: 0.72rem;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.06em;
  text-align: right;
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
  grid-template-columns: 1fr 1.28fr;
  gap: 32px;
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
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
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
  gap: 16px;
}

.console-step-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 12px 14px;
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
}

.console-box {
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
  gap: 28px;
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

.textarea-wrapper {
  position: relative;
}

.scenario-input {
  width: 100%;
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
  resize: vertical;
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

.launch-section {
  padding-top: 8px;
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
  margin-top: 20px;
}

@media (max-width: 960px) {
  .console-grid {
    grid-template-columns: 1fr;
  }

  .divider-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .divider-text {
    text-align: left;
  }

  .console-hero {
    padding: 36px 16px 0;
  }

  .hero-title {
    font-size: 1.75rem;
  }
}
</style>
