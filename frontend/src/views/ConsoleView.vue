<template>
  <div class="console-container">
    <!-- Console Top Navbar -->
    <header class="console-navbar">
      <div class="nav-left">
        <router-link to="/" class="brand-link" title="Return to ObMind Home">
          <img src="../assets/logo/obrive-white-logo.svg" alt="ObMind Logo" class="brand-logo-img" />
          <span class="brand-name">OBMIND</span>
          <span class="console-tag">CONSOLE</span>
        </router-link>

        <nav class="console-nav-links">
          <router-link to="/" class="console-nav-link">← Landing Page</router-link>
          <a href="#history" class="console-nav-link" @click.prevent="scrollToHistory">Simulation History</a>
        </nav>
      </div>

      <div class="nav-right">
        <!-- BYOK Key Status Badge -->
        <div class="byok-badge" @click="openByokSettings" title="Configure Custom LLM API Key">
          <span class="byok-dot"></span>
          <span class="byok-text">BYOK {{ hasCustomKey ? 'ACTIVE' : 'DEFAULT' }}</span>
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
        <button v-else class="btn-signin" @click="authStore.openAuthModal('login')">
          Sign In
        </button>

        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="link-obrive">
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
          Your email <strong>{{ authStore.user.value?.email }}</strong> is not verified yet. Please check your Brevo inbox to enable engine simulation runs.
        </span>
        <button class="banner-btn" @click="authStore.openProfileModal">View Profile</button>
      </div>

      <!-- Double Panel Console Layout -->
      <div class="console-grid">
        <!-- Left Panel: System Ready & Workflow Steps from docx -->
        <div class="left-panel">
          <div class="panel-badge">
            <span class="live-dot"></span> SYSTEM READY
          </div>

          <h1 class="panel-heading">System Ready</h1>
          <p class="panel-sub">
            OBMIND is ready to explore possibilities and simulate potential outcomes.
          </p>

          <!-- Metrics Row -->
          <div class="metrics-row">
            <div class="metric-card">
              <span class="metric-val">LOW COST</span>
              <span class="metric-desc">High token efficiency & edge caching</span>
            </div>
            <div class="metric-card">
              <span class="metric-val">HIGH AVAIL</span>
              <span class="metric-desc">Autonomous multi-agent cluster</span>
            </div>
          </div>

          <!-- Workflow Steps (01 to 05) from docx -->
          <div class="workflow-box">
            <div class="workflow-header">
              <span class="diamond-icon">◇</span>
              <span class="workflow-title">Workflow Steps</span>
            </div>

            <div class="workflow-steps-list">
              <div 
                v-for="(step, idx) in consoleSteps" 
                :key="step.number"
                class="console-step-item"
              >
                <span class="step-idx">{{ step.number }}</span>
                <div class="step-meta">
                  <h4 class="step-name">{{ step.title }}</h4>
                  <p class="step-detail">{{ step.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel: Interaction Console -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Upload Section -->
            <div class="console-section">
              <div class="section-label-bar">
                <span class="label-title">REALITY SEED</span>
                <span class="label-hint">PDF, MD, TXT (up to 50MB)</span>
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
                  accept=".pdf,.md,.txt"
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
                <span class="label-title">SIMULATION REQUIREMENT & HYPOTHESIS</span>
                <span class="label-hint">Natural language prompt</span>
              </div>

              <div class="textarea-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="scenario-input"
                  placeholder="Describe what you want to explore, key stakeholders, or the critical decision you need to make..."
                  rows="6"
                  :disabled="loading"
                ></textarea>

                <div class="engine-badge-pill">
                  <span class="badge-dot"></span>
                  <span>OB-SWARM INTELLIGENCE</span>
                </div>
              </div>
            </div>

            <!-- Launch Button Section with Auth Gate -->
            <div class="console-section launch-section">
              <button 
                class="btn-start-engine"
                :class="{ 'btn-ready': canSubmit }"
                @click="handleStartEngine"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading" class="btn-text-content">
                  <span>Start Engine</span>
                  <span class="btn-arrow">→</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import authStore from '../store/auth'
import { setPendingUpload, getPendingUpload } from '../store/pendingUpload.js'

const router = useRouter()

// Form Data & Files
const formData = ref({
  simulationRequirement: ''
})
const files = ref([])
const loading = ref(false)
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

const addFiles = (newFiles) => {
  const valid = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
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
  background-color: #070b0e;
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.console-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  background: rgba(12, 18, 22, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 50;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 28px;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #fff;
}

.brand-logo-img {
  height: 24px;
  width: auto;
}

.brand-name {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  letter-spacing: 2px;
}

.console-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  padding: 2px 8px;
  background: rgba(0, 229, 163, 0.15);
  border: 1px solid rgba(0, 229, 163, 0.3);
  color: #00E5A3;
  border-radius: 4px;
  letter-spacing: 1px;
}

.console-nav-links {
  display: flex;
  gap: 18px;
}

.console-nav-link {
  color: #94a3b8;
  font-size: 0.85rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.console-nav-link:hover {
  color: #00E5A3;
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
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.byok-badge:hover {
  border-color: #00E5A3;
}

.byok-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
  box-shadow: 0 0 6px #00E5A3;
}

.byok-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #cbd5e1;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  cursor: pointer;
}

.user-pill:hover {
  border-color: #00E5A3;
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #074139;
  color: #00E5A3;
  font-size: 0.72rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 0.85rem;
  color: #e2e8f0;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.verified {
  background: #00E5A3;
  box-shadow: 0 0 6px #00E5A3;
}

.status-dot.unverified {
  background: #f59e0b;
}

.btn-signin {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e2e8f0;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-signin:hover {
  border-color: #00E5A3;
  color: #00E5A3;
}

.link-obrive {
  color: #94a3b8;
  font-size: 0.85rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
}

.link-obrive:hover {
  color: #fff;
}

/* Main */
.console-main {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 24px 80px;
  flex: 1;
}

.verify-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  padding: 12px 18px;
  border-radius: 10px;
  margin-bottom: 24px;
  color: #fde68a;
  font-size: 0.9rem;
}

.banner-btn {
  margin-left: auto;
  background: #f59e0b;
  border: none;
  color: #070b0e;
  padding: 5px 12px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

/* Console Grid */
.console-grid {
  display: grid;
  grid-template-columns: 1fr 1.25fr;
  gap: 32px;
  margin-bottom: 60px;
}

/* Left Panel */
.left-panel {
  background: rgba(12, 18, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 32px;
  backdrop-filter: blur(14px);
}

.panel-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  background: rgba(7, 65, 57, 0.3);
  border: 1px solid rgba(0, 229, 163, 0.25);
  border-radius: 9999px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: #00E5A3;
  margin-bottom: 20px;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
  box-shadow: 0 0 8px #00E5A3;
}

.panel-heading {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #ffffff;
}

.panel-sub {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0 0 24px 0;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 32px;
}

.metric-card {
  background: rgba(7, 11, 14, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 16px;
}

.metric-val {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  font-weight: 700;
  color: #00E5A3;
  margin-bottom: 4px;
}

.metric-desc {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.4;
}

.workflow-box {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 24px;
}

.workflow-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.diamond-icon {
  color: #00E5A3;
}

.workflow-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #cbd5e1;
  text-transform: uppercase;
}

.workflow-steps-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.console-step-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.step-idx {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1rem;
  font-weight: 700;
  color: #00E5A3;
  background: rgba(7, 65, 57, 0.3);
  padding: 4px 8px;
  border-radius: 6px;
}

.step-meta {
  flex: 1;
}

.step-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 4px 0;
}

.step-detail {
  font-size: 0.82rem;
  line-height: 1.5;
  color: #94a3b8;
  margin: 0;
}

/* Right Panel */
.right-panel {
  display: flex;
  flex-direction: column;
}

.console-box {
  background: rgba(12, 18, 22, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
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
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #cbd5e1;
}

.label-hint {
  font-size: 0.75rem;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

.upload-dropzone {
  min-height: 160px;
  border: 2px dashed rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  cursor: pointer;
  background: rgba(7, 11, 14, 0.4);
  transition: all 0.25s ease;
}

.upload-dropzone:hover,
.upload-dropzone.drag-over {
  border-color: #00E5A3;
  background: rgba(0, 229, 163, 0.04);
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
  background: rgba(7, 65, 57, 0.4);
  border: 1px solid rgba(0, 229, 163, 0.3);
  color: #00E5A3;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 12px;
}

.upload-text-bold {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.upload-text-sub {
  font-size: 0.8rem;
  color: #64748b;
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
  padding: 8px 12px;
  background: rgba(7, 65, 57, 0.35);
  border: 1px solid rgba(0, 229, 163, 0.25);
  border-radius: 8px;
  font-size: 0.85rem;
  color: #ffffff;
}

.chip-name {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chip-remove {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0 2px;
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
  background: rgba(7, 11, 14, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px;
  padding-bottom: 44px;
  color: #ffffff;
  font-family: inherit;
  font-size: 0.95rem;
  line-height: 1.6;
  outline: none;
  resize: vertical;
  transition: border-color 0.2s ease;
}

.scenario-input:focus {
  border-color: #00E5A3;
  box-shadow: 0 0 15px rgba(0, 229, 163, 0.15);
}

.engine-badge-pill {
  position: absolute;
  bottom: 12px;
  right: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: #00E5A3;
}

.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #00E5A3;
}

.launch-section {
  padding-top: 8px;
}

.btn-start-engine {
  width: 100%;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #64748b;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: not-allowed;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-start-engine.btn-ready {
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  border-color: #00E5A3;
  color: #070b0e;
  cursor: pointer;
  box-shadow: 0 8px 25px rgba(0, 229, 163, 0.3);
}

.btn-start-engine.btn-ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 229, 163, 0.5);
}

.btn-text-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-arrow {
  transition: transform 0.2s ease;
}

.btn-start-engine.btn-ready:hover .btn-arrow {
  transform: translateX(4px);
}

/* History */
.history-wrapper {
  margin-top: 40px;
}

@media (max-width: 960px) {
  .console-grid {
    grid-template-columns: 1fr;
  }
}
</style>
