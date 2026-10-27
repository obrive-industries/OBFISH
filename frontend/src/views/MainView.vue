<template>
  <div class="main-view">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <div class="brand font-microgramma" @click="router.push('/console')" title="Return to Brain Console">
          <img src="../assets/icons/obrive-logo.svg" alt="Brain Logo" class="brand-header-icon" />
          <span>BRAIN</span>
        </div>
      </div>
      
      <div class="header-center">
        <div class="view-switcher">
          <button 
            v-for="mode in ['graph', 'split', 'workbench']" 
            :key="mode"
            class="switch-btn"
            :class="{ active: viewMode === mode }"
            @click="viewMode = mode"
          >
            {{ { graph: $t('main.layoutGraph'), split: $t('main.layoutSplit'), workbench: $t('main.layoutWorkbench') }[mode] }}
          </button>
        </div>
      </div>

      <div class="header-right">
        <div class="workflow-step">
          <span class="step-num">Step 1/4</span>
          <span class="step-name">{{ pipelineSteps[0] }}</span>
        </div>
        <div class="step-divider"></div>
        <span class="status-indicator" :class="statusClass">
          <span class="dot"></span>
          {{ statusText }}
        </span>
        <div class="step-divider"></div>
        <div v-if="authStore.isAuthenticated.value" class="user-pill-dark" @click="authStore.openProfileModal">
          <div class="user-avatar-tiny">{{ userInitials }}</div>
          <span class="user-pill-name">{{ authStore.user.value?.full_name || 'Account' }}</span>
        </div>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="content-area">
      <!-- Left Panel: Graph -->
      <div class="panel-wrapper left" :style="leftPanelStyle">
        <GraphPanel 
          :graphData="graphData"
          :loading="graphLoading"
          :currentPhase="currentPhase"
          @refresh="refreshGraph"
          @toggle-maximize="toggleMaximize('graph')"
        />
      </div>

      <!-- Right Panel: Step 1 Scenario / Upload & Graph Build -->
      <div class="panel-wrapper right" :style="rightPanelStyle">
        <Step1GraphBuild 
          :currentPhase="currentPhase"
          :projectData="projectData"
          :ontologyProgress="ontologyProgress"
          :buildProgress="buildProgress"
          :graphData="graphData"
          :systemLogs="systemLogs"
          @next-step="handleNextStep"
        />
      </div>
    </main>

    <!-- User-Friendly Error Modal -->
    <Teleport to="body">
      <div v-if="errorModalOpen" class="error-modal-backdrop" @click.self="clearError">
        <div class="error-modal-box">
          <div class="error-modal-header">
            <div class="error-badge-icon">
              <span>⚠️</span>
            </div>
            <div class="error-title-wrap">
              <h3 class="error-dialog-title font-microgramma">{{ errorTitle }}</h3>
              <p class="error-dialog-subtitle">{{ errorSubtitle }}</p>
            </div>
            <button class="error-close-btn" @click="clearError" title="Dismiss">×</button>
          </div>

          <div class="error-modal-content">
            <div class="error-raw-card">
              <span class="raw-label">SYSTEM DETAILS</span>
              <p class="raw-message">{{ error }}</p>
            </div>

            <div class="error-instructions-card">
              <h4 class="instruction-header font-microgramma">HOW TO PROCEED</h4>
              <ul class="instruction-list">
                <li v-for="(tip, i) in errorTips" :key="i">
                  <span class="bullet-dot">•</span>
                  <span>{{ tip }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="error-modal-footer">
            <button class="btn-error-ghost font-microgramma" @click="clearError">
              Dismiss
            </button>
            <button class="btn-error-action font-microgramma" @click="handleErrorAction">
              {{ errorActionLabel }} →
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import GraphPanel from '../components/GraphPanel.vue'
import Step1GraphBuild from '../components/Step1GraphBuild.vue'
import { generateOntology, getProject, buildGraph, getTaskStatus, getGraphData } from '../api/graph'
import { getPendingUpload, clearPendingUpload } from '../store/pendingUpload'
import authStore from '../store/auth'
import billingStore from '../store/billing'

const route = useRoute()
const router = useRouter()
const { t, tm } = useI18n()

const userInitials = computed(() => {
  const name = authStore.user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

// Layout State
const viewMode = ref('split') // graph | split | workbench

// Step State: 4-Step Simulation Pipeline
const pipelineSteps = [
  'Scenario / Upload',
  'Simulation & Agents',
  'Insights & Report',
  'Exploration / Dialogue'
]
const currentStep = ref(1)
const stepNames = computed(() => tm('main.stepNames') || pipelineSteps)

// Data State
const currentProjectId = ref(route.params.projectId)
const loading = ref(false)
const graphLoading = ref(false)
const error = ref('')
const errorModalOpen = ref(false)
const projectData = ref(null)
const graphData = ref(null)
const currentPhase = ref(-1) // -1: Upload, 0: Ontology, 1: Build, 2: Complete
const ontologyProgress = ref(null)
const buildProgress = ref(null)
const systemLogs = ref([])

// Error Modal Helpers
const triggerError = (msg) => {
  error.value = msg || 'An unexpected simulation error occurred'
  errorModalOpen.value = true
}

const clearError = () => {
  errorModalOpen.value = false
}

const errorTitle = computed(() => {
  const err = (error.value || '').toLowerCase()
  if (err.includes('simulation requirement') || err.includes('simulation_requirement') || err.includes('requirement')) {
    return 'Scenario Requirement Needed'
  }
  if (err.includes('token') || err.includes('auth') || err.includes('login') || err.includes('401')) {
    return 'Authentication Required'
  }
  if (err.includes('plan') || err.includes('limit') || err.includes('402')) {
    return 'Subscription Plan Required'
  }
  if (err.includes('network') || err.includes('timeout') || err.includes('failed to fetch')) {
    return 'Network Connection Error'
  }
  return 'Simulation Engine Notice'
})

const errorSubtitle = computed(() => {
  const err = (error.value || '').toLowerCase()
  if (err.includes('simulation requirement') || err.includes('simulation_requirement') || err.includes('requirement')) {
    return 'The swarm intelligence engine needs a concrete scenario or hypothesis to simulate.'
  }
  if (err.includes('token') || err.includes('auth') || err.includes('login') || err.includes('401')) {
    return 'Please sign in to access your simulation workspaces.'
  }
  if (err.includes('plan') || err.includes('limit') || err.includes('402')) {
    return 'You have reached your current simulation run limit.'
  }
  return 'The simulation workflow encountered an issue during processing.'
})

const errorTips = computed(() => {
  const err = (error.value || '').toLowerCase()
  if (err.includes('simulation requirement') || err.includes('simulation_requirement') || err.includes('requirement')) {
    return [
      'Enter a clear prompt describing what you want to simulate (e.g. "Simulate market adoption and competitor reaction").',
      'Attach source documents (PDF, DOCX, TXT, MD) containing background facts, metrics, and policies.',
      'Return to Console to quickly review and launch your scenario.'
    ]
  }
  if (err.includes('token') || err.includes('auth') || err.includes('login') || err.includes('401')) {
    return [
      'Click the button below to sign in or register your account.',
      'Your uploaded materials and inputs will be preserved.'
    ]
  }
  if (err.includes('plan') || err.includes('limit') || err.includes('402')) {
    return [
      'Choose a Starter, Pro, or Premium subscription to unlock more simulation capacity.',
      'All plans support deep persona modeling and multi-round agent debates.'
    ]
  }
  return [
    'Check your internet connection and verify that the backend engine is running.',
    'You can return to the Console to re-verify your documents and try again.'
  ]
})

const errorActionLabel = computed(() => {
  const err = (error.value || '').toLowerCase()
  if (err.includes('simulation requirement') || err.includes('simulation_requirement') || err.includes('requirement')) {
    return 'Return to Console & Add Scenario'
  }
  if (err.includes('token') || err.includes('auth') || err.includes('login') || err.includes('401')) {
    return 'Sign In to Brain'
  }
  if (err.includes('plan') || err.includes('limit') || err.includes('402')) {
    return 'View Subscription Plans'
  }
  return 'Return to Console'
})

const handleErrorAction = () => {
  const err = (error.value || '').toLowerCase()
  clearError()
  if (err.includes('token') || err.includes('auth') || err.includes('login') || err.includes('401')) {
    authStore.openAuthModal('login', 'Please sign in to continue your simulation.')
    return
  }
  if (err.includes('plan') || err.includes('limit') || err.includes('402')) {
    billingStore.openPricing({ resume: false })
    return
  }
  router.push('/console')
}

// Polling timers
let pollTimer = null
let graphPollTimer = null

// --- Computed Layout Styles ---
const leftPanelStyle = computed(() => {
  if (viewMode.value === 'graph') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'workbench') return { width: '0%', opacity: 0, transform: 'translateX(-20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

const rightPanelStyle = computed(() => {
  if (viewMode.value === 'workbench') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'graph') return { width: '0%', opacity: 0, transform: 'translateX(20px)' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

// --- Status Computed ---
const statusClass = computed(() => {
  if (error.value) return 'error'
  if (currentPhase.value >= 2) return 'completed'
  return 'processing'
})

const statusText = computed(() => {
  if (error.value) return 'Error'
  if (currentPhase.value >= 2) return 'Ready'
  if (currentPhase.value === 1) return 'Building Graph'
  if (currentPhase.value === 0) return 'Generating Ontology'
  return 'Initializing'
})

// --- Helpers ---
const addLog = (msg) => {
  const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }) + '.' + new Date().getMilliseconds().toString().padStart(3, '0')
  systemLogs.value.push({ time, msg })
  // Keep last 100 logs
  if (systemLogs.value.length > 100) {
    systemLogs.value.shift()
  }
}

// --- Layout Methods ---
const toggleMaximize = (target) => {
  if (viewMode.value === target) {
    viewMode.value = 'split'
  } else {
    viewMode.value = target
  }
}

const handleNextStep = (params = {}) => {
  if (currentStep.value < 5) {
    currentStep.value++
    addLog(t('log.enterStep', { step: currentStep.value, name: stepNames.value[currentStep.value - 1] }))
    
    // 如果是从 Step 2 进入 Step 3，记录模拟轮数配置
    if (currentStep.value === 3 && params.maxRounds) {
      addLog(t('log.customSimRounds', { rounds: params.maxRounds }))
    }
  }
}

const handleGoBack = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    addLog(t('log.returnToStep', { step: currentStep.value, name: stepNames.value[currentStep.value - 1] }))
  }
}

// --- Data Logic ---

const initProject = async () => {
  addLog('Project view initialized.')
  if (currentProjectId.value === 'new') {
    await handleNewProject()
  } else {
    await loadProject()
  }
}

const handleNewProject = async () => {
  const pending = await getPendingUpload()
  const hasFiles = Boolean(pending && pending.files && pending.files.length > 0)
  const hasHypothesis = Boolean(pending && pending.simulationRequirement && pending.simulationRequirement.trim().length > 0)

  if (!hasFiles && !hasHypothesis) {
    addLog('No pending dossier found; returning to console.')
    router.replace('/console')
    return
  }

  try {
    loading.value = true
    currentPhase.value = 0
    ontologyProgress.value = { 
      message: hasFiles ? 'Uploading and analyzing docs...' : 'Ingesting scenario hypothesis...' 
    }
    addLog(hasFiles ? 'Starting ontology generation: Uploading files...' : 'Starting ontology generation from hypothesis text...')
    
    const formData = new FormData()
    if (hasFiles) {
      pending.files.forEach(f => formData.append('files', f))
    }
    const reqText = (pending.simulationRequirement || '').trim() ||
      (hasFiles ? `Simulate key stakeholder dynamics, strategic outcomes, and emerging risks based on ${pending.files[0]?.name || 'uploaded dossier'}.` : '')
    formData.append('simulation_requirement', reqText)
    
    const res = await generateOntology(formData)
    if (res.success) {
      await clearPendingUpload()
      currentProjectId.value = res.data.project_id
      projectData.value = res.data
      
      router.replace({ name: 'Process', params: { projectId: res.data.project_id } })
      ontologyProgress.value = null
      addLog(`Ontology generated successfully for project ${res.data.project_id}`)
      await startBuildGraph()
    } else {
      triggerError(res.error || 'Ontology generation failed')
      addLog(`Error generating ontology: ${error.value}`)
      ontologyProgress.value = null
    }
  } catch (err) {
    triggerError(err.message)
    addLog(`Exception in handleNewProject: ${err.message}`)
    ontologyProgress.value = null
    if (String(err.code || '').startsWith('PLAN_') || err.status === 402) {
      billingStore.openPricing({ resume: false })
    }
  } finally {
    loading.value = false
    ontologyProgress.value = null
  }
}

const loadProject = async () => {
  try {
    loading.value = true
    addLog(`Loading project ${currentProjectId.value}...`)
    const res = await getProject(currentProjectId.value)
    if (res.success) {
      projectData.value = res.data
      updatePhaseByStatus(res.data.status)
      addLog(`Project loaded. Status: ${res.data.status}`)
      
      if (res.data.status === 'ontology_generated' && !res.data.graph_id) {
        await startBuildGraph()
      } else if (res.data.status === 'graph_building' && res.data.graph_build_task_id) {
        currentPhase.value = 1
        startPollingTask(res.data.graph_build_task_id)
      } else if (res.data.status === 'graph_completed' && res.data.graph_id) {
        currentPhase.value = 2
        await loadGraph(res.data.graph_id)
      }
    } else {
      triggerError(res.error || 'Failed to load project')
      addLog(`Error loading project: ${res.error}`)
    }
  } catch (err) {
    triggerError(err.message)
    addLog(`Exception in loadProject: ${err.message}`)
  } finally {
    loading.value = false
  }
}

const updatePhaseByStatus = (status) => {
  switch (status) {
    case 'created':
    case 'ontology_generated': currentPhase.value = 0; break;
    case 'graph_building': currentPhase.value = 1; break;
    case 'graph_completed': currentPhase.value = 2; break;
    case 'failed': triggerError('Project build failed'); break;
  }
}

const startBuildGraph = async () => {
  try {
    currentPhase.value = 1
    buildProgress.value = { progress: 0, message: 'Starting build...' }
    addLog('Initiating graph build...')
    
    const res = await buildGraph({ project_id: currentProjectId.value })
    if (res.success) {
      if (res.data.reused && res.data.graph_id) {
        currentPhase.value = 2
        buildProgress.value = null
        const projectRes = await getProject(currentProjectId.value)
        if (projectRes.success) {
          projectData.value = projectRes.data
        }
        await loadGraph(res.data.graph_id)
        return
      }

      addLog(`Graph build task started. Task ID: ${res.data.task_id}`)
      startPollingTask(res.data.task_id)
    } else {
      triggerError(res.error || 'Failed to initiate graph build')
      addLog(`Error starting build: ${res.error}`)
    }
  } catch (err) {
    triggerError(err.message)
    addLog(`Exception in startBuildGraph: ${err.message}`)
  }
}

const startGraphPolling = () => {
  addLog('Started polling for graph data...')
  fetchGraphData()
  graphPollTimer = setInterval(fetchGraphData, 10000)
}

const fetchGraphData = async () => {
  try {
    // Refresh project info to check for graph_id
    const projRes = await getProject(currentProjectId.value)
    if (projRes.success && projRes.data.graph_id) {
      const gRes = await getGraphData(projRes.data.graph_id)
      if (gRes.success) {
        graphData.value = gRes.data
        const nodeCount = gRes.data.node_count || gRes.data.nodes?.length || 0
        const edgeCount = gRes.data.edge_count || gRes.data.edges?.length || 0
        addLog(`Graph data refreshed. Nodes: ${nodeCount}, Edges: ${edgeCount}`)
      }
    }
  } catch (err) {
    console.warn('Graph fetch error:', err)
  }
}

const startPollingTask = (taskId) => {
  pollTaskStatus(taskId)
  pollTimer = setInterval(() => pollTaskStatus(taskId), 2000)
}

const pollTaskStatus = async (taskId) => {
  try {
    const res = await getTaskStatus(taskId)
    if (res.success) {
      const task = res.data
      
      // Log progress message if it changed
      if (task.message && task.message !== buildProgress.value?.message) {
        addLog(task.message)
      }
      
      buildProgress.value = { progress: task.progress || 0, message: task.message }
      
      if (task.status === 'completed') {
        addLog('Graph build task completed.')
        stopPolling()
        stopGraphPolling() // Stop polling, do final load
        currentPhase.value = 2
        
        // Final load
        const projRes = await getProject(currentProjectId.value)
        if (projRes.success && projRes.data.graph_id) {
            projectData.value = projRes.data
            await loadGraph(projRes.data.graph_id)
        }
      } else if (task.status === 'failed') {
        stopPolling()
        triggerError(task.error || 'Graph construction task failed')
        addLog(`Graph build task failed: ${task.error}`)
      }
    }
  } catch (e) {
    console.error(e)
  }
}

const loadGraph = async (graphId) => {
  graphLoading.value = true
  addLog(`Loading full graph data: ${graphId}`)
  try {
    const res = await getGraphData(graphId)
    if (res.success) {
      graphData.value = res.data
      addLog('Graph data loaded successfully.')
    } else {
      addLog(`Failed to load graph data: ${res.error}`)
    }
  } catch (e) {
    addLog(`Exception loading graph: ${e.message}`)
  } finally {
    graphLoading.value = false
  }
}

const refreshGraph = () => {
  if (projectData.value?.graph_id) {
    addLog('Manual graph refresh triggered.')
    loadGraph(projectData.value.graph_id)
  }
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const stopGraphPolling = () => {
  if (graphPollTimer) {
    clearInterval(graphPollTimer)
    graphPollTimer = null
    addLog('Graph polling stopped.')
  }
}

onMounted(() => {
  initProject()
})

onUnmounted(() => {
  stopPolling()
  stopGraphPolling()
})
</script>

<style scoped>
.main-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  overflow: hidden;
  font-family: var(--font-sans, "Space Grotesk", system-ui, sans-serif);
}

/* Header (MiroFish 60px Header) */
.app-header {
  height: 60px;
  border-bottom: 1px solid #EAEAEA;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #FFFFFF;
  z-index: 100;
  position: relative;
}

.header-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.brand {
  font-family: var(--font-display, "Space Grotesk", sans-serif) !important;
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 0.05em;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #000000;
}

.brand-header-icon {
  height: 24px;
  width: auto;
}

.view-switcher {
  display: flex;
  background: #F5F5F5;
  padding: 4px;
  border-radius: 6px;
  gap: 4px;
}

.switch-btn {
  border: none;
  background: transparent;
  padding: 6px 16px;
  font-family: var(--font-mono, monospace);
  font-size: 12px;
  font-weight: 600;
  color: #666666;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.switch-btn.active {
  background: #FFFFFF;
  color: #000000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono, monospace);
  font-size: 12px;
  color: #666666;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.step-num {
  font-family: var(--font-mono, monospace);
  font-weight: 700;
  color: #999999;
}

.step-name {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-weight: 700;
  font-size: 13px;
  color: #000000;
  letter-spacing: 0.02em;
}

.step-divider {
  width: 1px;
  height: 14px;
  background-color: #E0E0E0;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #CCCCCC;
}

.status-indicator.processing .dot { background: #FF4500; animation: pulse 1s infinite; }
.status-indicator.completed .dot { background: #10B981; }
.status-indicator.error .dot { background: #EF4444; }

@keyframes pulse { 50% { opacity: 0.5; } }

/* Content */
.content-area {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
}

.panel-wrapper {
  height: 100%;
  overflow: hidden;
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease, transform 0.3s ease;
  will-change: width, opacity, transform;
}

.panel-wrapper.left {
  border-right: 1px solid #EAEAEA;
}

.user-pill-dark {
  display: flex;
  align-items: center;
  gap: 7px;
  background: #F5F5F5;
  border: 1px solid #E0E0E0;
  border-radius: 9999px;
  padding: 3px 10px 3px 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-pill-dark:hover {
  background: #EAEAEA;
  border-color: #CCCCCC;
}

.user-avatar-tiny {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #000000;
  color: #FFFFFF;
  font-family: var(--font-mono, monospace);
  font-size: 0.65rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-pill-name {
  font-family: var(--font-mono, monospace);
  font-size: 0.78rem;
  font-weight: 600;
  color: #000000;
  max-width: 110px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sign-in-btn-header {
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  border-radius: 9999px;
  padding: 5px 16px;
  font-family: var(--font-mono, monospace);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sign-in-btn-header:hover {
  background: #FF4500;
  border-color: #FF4500;
}

/* User-Friendly Error Modal Styles */
.error-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(7, 57, 51, 0.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.error-modal-box {
  background: #FFFFFF;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 20px;
  box-shadow: 0 24px 60px rgba(7, 57, 51, 0.25);
  width: 100%;
  max-width: 540px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.error-modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 24px 28px 18px;
  border-bottom: 1px solid rgba(7, 57, 51, 0.08);
}

.error-badge-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #FEF3C7;
  border: 1px solid #FDE68A;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.error-title-wrap {
  flex: 1;
}

.error-dialog-title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: #073933;
  letter-spacing: -0.01em;
}

.error-dialog-subtitle {
  margin: 4px 0 0;
  font-size: 13px;
  color: #2D554C;
  line-height: 1.45;
}

.error-close-btn {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #6B7280;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  transition: color 0.2s;
}

.error-close-btn:hover {
  color: #111827;
}

.error-modal-content {
  padding: 20px 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error-raw-card {
  background: #FFFBEB;
  border: 1px solid #FCD34D;
  border-radius: 12px;
  padding: 12px 16px;
}

.raw-label {
  display: block;
  font-size: 9px;
  font-weight: 800;
  color: #92400E;
  letter-spacing: 0.1em;
  margin-bottom: 4px;
}

.raw-message {
  margin: 0;
  font-family: var(--font-mono, monospace);
  font-size: 12.5px;
  color: #78350F;
  word-break: break-word;
  line-height: 1.45;
}

.error-instructions-card {
  background: #F8FAFA;
  border: 1px solid rgba(7, 57, 51, 0.1);
  border-radius: 12px;
  padding: 14px 18px;
}

.instruction-header {
  margin: 0 0 10px;
  font-size: 11px;
  font-weight: 700;
  color: #073933;
  letter-spacing: 0.08em;
}

.instruction-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.instruction-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: #1F2937;
  line-height: 1.45;
}

.bullet-dot {
  color: #073933;
  font-weight: 800;
}

.error-modal-footer {
  padding: 16px 28px 22px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: #FAFAFA;
  border-top: 1px solid rgba(7, 57, 51, 0.08);
}

.btn-error-ghost {
  background: transparent;
  border: 1px solid rgba(7, 57, 51, 0.2);
  color: #2D554C;
  border-radius: 999px;
  padding: 8px 18px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-error-ghost:hover {
  background: rgba(7, 57, 51, 0.05);
  color: #073933;
}

.btn-error-action {
  background: #073933;
  border: 1px solid #073933;
  color: #FFFFFF;
  border-radius: 999px;
  padding: 8px 22px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.25);
  transition: all 0.2s;
}

.btn-error-action:hover {
  background: #032420;
  border-color: #032420;
  transform: translateY(-1px);
}
</style>
