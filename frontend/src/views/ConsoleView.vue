<template>
  <div class="console-container">
    <!-- Minimal Application Header (Full-width sticky Obrive header) -->
    <header class="console-navbar">
      <div class="nav-left">
        <router-link to="/" class="brand-link" title="Return to Brain Home">
          <img src="../assets/icons/obrive-white-logo.svg" alt="Brain Logo" class="brand-logo-img" />
          <span class="brand-name font-microgramma">BRAIN</span>
          <span class="console-tag font-microgramma">CONSOLE</span>
        </router-link>

        <nav class="console-nav-links">
          <a href="#history" class="console-nav-link font-microgramma" @click.prevent="scrollToHistory">Simulation History</a>
          <router-link
            v-if="authStore.isAdmin.value"
            to="/admin/wishlist"
            class="console-nav-link font-microgramma text-amber-400 hover:text-amber-300"
            style="color: #F59E0B;"
          >
            📋 Wishlist Leads
          </router-link>
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
        <button v-else class="console-signin-btn font-microgramma" @click="authStore.openAuthModal('login')">
          Sign In
        </button>

        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="link-obrive font-microgramma">
          Explore Obrive <span class="arrow">↗</span>
        </a>
      </div>
    </header>

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
            <span class="font-microgramma">■ SYSTEM READY // PREDICTIVE CONSOLE</span>
          </div>

          <h1 class="panel-heading font-microgramma">System Ready</h1>
          <p class="panel-sub">
            BRAIN is primed to explore possibilities, stress-test variables, and simulate potential strategic outcomes.
          </p>
          <p class="panel-sub-desc">
            Deploy multi-agent simulation swarms, upload reality seed documents, and stress-test strategic hypotheses before real-world execution.
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

            <!-- Plan / usage status bar -->
            <div
              class="plan-status-card"
              :class="{ 'has-plan': billingStore.isPaid.value, 'limit-reached': !billingStore.canStart.value }"
              @click="openPlanSettings"
              title="View plans and usage"
            >
              <div class="plan-card-left">
                <span class="plan-card-icon">{{ planIcon }}</span>
                <div class="plan-card-info">
                  <div class="plan-card-title font-microgramma">{{ planTitle }}</div>
                  <div class="plan-card-sub">{{ planSubtitle }}</div>
                </div>
              </div>
              <button type="button" class="plan-card-btn font-microgramma">
                {{ plan.unlimited ? 'ADMIN' : (billingStore.canStart.value ? 'MANAGE' : 'VIEW PLANS →') }}
              </button>
            </div>

            <!-- Launch Button Section matching MiroFish start-engine-btn -->
            <div class="console-section launch-section">
              <button 
                class="start-engine-btn font-microgramma"
                @click="handleStartEngine"
                :disabled="loading"
              >
                <span v-if="!loading" class="btn-text-content">
                  <span class="btn-label">Start Engine</span>
                </span>
                <span v-else class="btn-text-content">
                  <span>Initializing Swarm...</span>
                </span>
                <span class="btn-arrow">→</span>
              </button>
              <router-link to="/demo" class="demo-link font-microgramma">
                FIRST TIME? EXPLORE THE SAMPLE REPORT →
              </router-link>
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
import authStore from '../store/auth'
import authApi from '../api/auth'
import billingStore from '../store/billing'
import { savePendingUpload, getPendingUpload } from '../utils/pendingUpload.js'

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
const resumeAfterPurchase = ref(false)

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
  if (authStore.isAuthenticated.value) {
    billingStore.refresh()
  }
})

// Resume the interrupted Start Engine flow immediately after a plan is bound.
watch(
  () => billingStore.state.purchaseVersion,
  () => {
    if (!resumeAfterPurchase.value) return
    resumeAfterPurchase.value = false
    if (billingStore.canStart.value) handleStartEngine()
  }
)

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

const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim().length > 0
})

const plan = computed(() => billingStore.entitlement.value)

const planIcon = computed(() => {
  if (plan.value.unlimited) return '∞'
  return plan.value.plan === 'free' ? '◇' : '◆'
})

const planTitle = computed(() => {
  if (plan.value.unlimited) return 'ADMIN ACCESS — UNLIMITED RUNS'
  if (plan.value.plan === 'free') {
    const used = plan.value.runs_used || 0
    const limit = plan.value.runs_limit || 1
    if (used < limit) {
      return 'FREE DEMO — 1 LIVE RUN AVAILABLE'
    }
    return 'FREE DEMO COMPLETED — PLAN REQUIRED'
  }
  const remaining = Math.max(0, (plan.value.runs_limit || 0) - (plan.value.runs_used || 0))
  return `${plan.value.plan_name.toUpperCase()} PLAN — ${remaining} RUN${remaining === 1 ? '' : 'S'} LEFT`
})

const planSubtitle = computed(() => {
  if (plan.value.unlimited) return 'All simulation limits bypassed'
  if (plan.value.plan === 'free') {
    const used = plan.value.runs_used || 0
    const limit = plan.value.runs_limit || 1
    if (used < limit) {
      return 'Run your first live scenario (up to 10 rounds) for free'
    }
    return 'Choose a plan to continue running simulations'
  }
  const rounds = plan.value.max_rounds ? `${plan.value.max_rounds} rounds per run` : 'Unlimited rounds'
  const renews = plan.value.renews_at ? new Date(plan.value.renews_at).toLocaleDateString() : ''
  return renews ? `${rounds} · renews ${renews}` : rounds
})

const openPlanSettings = () => {
  if (!authStore.isAuthenticated.value) {
    authStore.openAuthModal('login', 'Sign in to view plans and start your own simulation.')
    return
  }
  resumeAfterPurchase.value = true
  billingStore.openPricing({ resume: true })
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

  // 3. Plan Gate Check: free accounts only get the sample report
  await billingStore.refresh()
  if (!billingStore.canStart.value) {
    await savePendingUpload(files.value, formData.value.simulationRequirement)
    resumeAfterPurchase.value = true
    billingStore.openPricing({ resume: true })
    return
  }

  // 4. Scenario & Hypothesis Check
  if (!formData.value.simulationRequirement?.trim()) {
    alert('Please describe your simulation scenario, requirement, or hypothesis to start the engine.')
    return
  }

  // Cache user's inputs in IndexedDB pending store immediately so nothing is lost
  await savePendingUpload(files.value, formData.value.simulationRequirement)

  // 5. Authenticated, Verified & Plan Active -> Navigate to Process View
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
  background-color: #FFFFFF;
  color: #000000;
  display: flex;
  flex-direction: column;
  font-family: var(--font-sans, "Space Grotesk", system-ui, sans-serif);
}

/* Minimal Application Header (MiroFish 60px black bar) */
.console-navbar {
  height: 60px;
  background: #000000;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
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
  color: #FFFFFF;
}

.brand-logo-img {
  height: 24px;
  width: auto;
}

.brand-name {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: 0.05em;
  color: #FFFFFF;
}

.console-tag {
  font-family: var(--font-mono, monospace);
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #FFFFFF;
  border-radius: 4px;
  letter-spacing: 0.08em;
}

.console-nav-links {
  display: flex;
  gap: 20px;
  margin-left: 8px;
}

.console-nav-link {
  font-family: var(--font-mono, monospace);
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
  letter-spacing: 0.04em;
}

.console-nav-link:hover {
  color: #FFFFFF;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px 4px 5px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-pill:hover {
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(255, 255, 255, 0.35);
}

.console-signin-btn {
  padding: 6px 16px;
  background: #FFFFFF;
  color: #000000;
  border: none;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.console-signin-btn:hover {
  background: #A2F1DF;
  box-shadow: 0 0 16px rgba(162, 241, 223, 0.4);
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #FFFFFF;
  color: #000000;
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-family: var(--font-mono, monospace);
  font-size: 0.8rem;
  font-weight: 600;
  color: #FFFFFF;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.verified {
  background: #00E5A3;
  box-shadow: 0 0 6px rgba(0, 229, 163, 0.6);
}

.status-dot.unverified {
  background: #FF4500;
}

.link-obrive {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #FFFFFF;
  color: #000000;
  text-decoration: none;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.link-obrive:hover {
  background: #E5E5E5;
}

.link-obrive .arrow {
  font-family: sans-serif;
  font-size: 0.75rem;
  opacity: 0.6;
}

.panel-sub-desc {
  font-size: 0.88rem;
  line-height: 1.55;
  color: #888888;
  margin-bottom: 24px;
}

/* Main Workspace */
.console-main {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 36px 32px 80px;
  flex: 1;
}

/* Email Verification Banner */
.verify-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FFFDF0;
  border: 1px solid #F0E4B0;
  padding: 14px 20px;
  border-radius: 8px;
  margin-bottom: 28px;
  color: #A08940;
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
}

.banner-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.banner-btn-secondary {
  background: #FFFFFF;
  border: 1px solid #E5E5E5;
  color: #666666;
  padding: 6px 14px;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.banner-btn-secondary:hover:not(:disabled) {
  background: #F5F5F5;
  color: #000000;
}

.banner-btn {
  background: #000000;
  border: 1px solid #000000;
  color: #FFFFFF;
  padding: 6px 14px;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.banner-btn:hover {
  background: #FF4500;
  border-color: #FF4500;
}

/* Console Grid */
.console-grid {
  display: grid;
  grid-template-columns: 0.88fr 1.12fr;
  gap: 36px;
  align-items: start;
  margin-bottom: 60px;
}

/* Obrive Cards */
.obrive-card {
  background: #FFFFFF;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

/* Left Panel */
.left-panel {
  padding: 28px 26px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.panel-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 700;
  color: #999999;
  margin-bottom: 16px;
  width: fit-content;
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #FF4500;
  box-shadow: 0 0 6px rgba(255, 69, 0, 0.5);
}

.panel-heading {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.85rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #000000;
  letter-spacing: -0.01em;
}

.panel-sub {
  font-size: 0.92rem;
  line-height: 1.6;
  color: #666666;
  margin: 0 0 24px 0;
}

/* System Readiness Metrics inside Left Panel */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 24px;
}

.metric-card {
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s ease;
}

.metric-card:hover {
  border-color: #000000;
  background: #FFFFFF;
}

.metric-value {
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.04em;
}

.metric-label {
  font-size: 0.7rem;
  color: #666666;
  line-height: 1.4;
  font-weight: 450;
}

.workflow-box {
  border: 1px solid #E5E5E5;
  border-radius: 10px;
  padding: 24px;
  background: #FAFAFA;
}

.workflow-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-family: var(--font-mono, monospace);
  font-size: 0.8rem;
  color: #999999;
}

.diamond-icon {
  color: #000000;
  font-size: 0.95rem;
  line-height: 1;
}

.workflow-title {
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.workflow-steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.console-step-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 0;
  background: transparent;
  border: none;
}

.step-idx {
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 700;
  color: #000000;
  opacity: 0.35;
  padding: 0;
  line-height: 1.2;
}

.step-meta {
  flex: 1;
}

.step-name {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 0.92rem;
  font-weight: 600;
  color: #000000;
  margin: 0 0 2px 0;
  letter-spacing: -0.01em;
}

.step-detail {
  font-size: 0.78rem;
  line-height: 1.45;
  color: #666666;
  margin: 0;
}

/* Right Panel */
.right-panel {
  display: flex;
  flex-direction: column;
}

.console-box {
  border: 1px solid #CCCCCC;
  padding: 12px;
  background: #FFFFFF;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.console-section {
  padding: 12px 12px 0;
  display: flex;
  flex-direction: column;
}

.section-label-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.label-title {
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #666666;
}

.label-hint {
  font-size: 0.72rem;
  color: #999999;
  font-family: var(--font-mono, monospace);
}

.upload-dropzone {
  min-height: 80px;
  border: 1px dashed #CCCCCC;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px 20px;
  cursor: pointer;
  background: #FAFAFA;
  transition: all 0.2s ease;
}

.upload-dropzone:hover,
.upload-dropzone.drag-over {
  border-color: #000000;
  background: #F5F5F5;
}

.upload-empty {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  text-align: left;
}

.upload-icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #000000;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.upload-dropzone:hover .upload-icon-circle {
  transform: translateY(-2px);
}

.upload-text-bold {
  font-size: 0.85rem;
  font-weight: 600;
  color: #000000;
  margin-bottom: 2px;
}

.upload-text-sub {
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  color: #666666;
}

.file-chips-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}

.file-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: #F0F0F0;
  border: 1px solid #DDDDDD;
  border-radius: 6px;
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  font-weight: 600;
  color: #000000;
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
  color: #666666;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 2px;
  line-height: 1;
}

.chip-remove:hover {
  color: #FF4500;
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
  border: 1px solid #DDDDDD;
  background: #FAFAFA;
  border-radius: 8px;
  overflow: hidden;
}

.scenario-input {
  width: 100%;
  flex: 1;
  min-height: 110px;
  box-sizing: border-box;
  background: transparent;
  border: none;
  padding: 14px 18px 40px;
  color: #000000;
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  line-height: 1.6;
  outline: none;
  resize: none;
}

.scenario-input:focus {
  background: #FFFFFF;
}

.engine-badge-pill {
  position: absolute;
  bottom: 10px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  background: #FFFFFF;
  border: 1px solid #E5E5E5;
  border-radius: 4px;
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  font-weight: 600;
  color: #999999;
}

.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #FF4500;
}

/* Plan / usage status card */
.plan-status-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 12px 16px;
  background: #FFFDF0;
  border: 1px solid #F0E4B0;
  border-radius: 8px;
  margin: 12px 12px 0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.plan-status-card:hover {
  border-color: #E0CE80;
}

.plan-status-card.has-plan {
  background: #F0FFF4;
  border-color: #B8E8C4;
}

.plan-status-card.has-plan:hover {
  border-color: #8FD8A0;
}

.plan-card-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.plan-card-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.plan-card-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.plan-card-title {
  font-family: var(--font-mono, monospace);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #A08940;
}

.plan-status-card.has-plan .plan-card-title {
  color: #2E7D32;
}

.plan-card-sub {
  font-size: 0.78rem;
  color: #A08940;
}

.plan-status-card.has-plan .plan-card-sub {
  color: #388E3C;
}

.plan-card-btn {
  background: #000000;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.plan-card-btn:hover {
  background: #FF4500;
}

.demo-link {
  display: block;
  margin-top: 14px;
  text-align: center;
  color: #737373;
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  text-decoration: none;
  transition: color 0.2s ease;
}

.demo-link:hover {
  color: #000000;
}

.launch-section {
  padding: 12px;
}

/* MiroFish Pulsing Start Engine Button */
.start-engine-btn {
  width: 100%;
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  padding: 18px 24px;
  font-family: var(--font-mono, monospace);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: #FF4500;
  border-color: #FF4500;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 69, 0, 0.35);
}

.start-engine-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  animation: none;
}

@keyframes pulse-border {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.25);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(0, 0, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
}

.btn-text-content {
  display: flex;
  align-items: center;
}

.btn-label {
  letter-spacing: 0.06em;
}

.btn-arrow {
  font-size: 1.25rem;
  font-weight: 700;
  transition: transform 0.2s ease;
}

.start-engine-btn:hover:not(:disabled) .btn-arrow {
  transform: translateX(4px);
}

/* History */
.history-wrapper {
  margin-top: 40px;
  scroll-margin-top: 80px;
}

@media (max-width: 1024px) {
  .console-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .console-hero {
    padding: 44px 16px 36px;
  }

  .hero-title {
    font-size: 1.85rem;
  }

  .console-main {
    padding: 32px 16px 60px;
  }
}

@media (max-width: 640px) {
  .metrics-row {
    grid-template-columns: 1fr;
  }
}
</style>
