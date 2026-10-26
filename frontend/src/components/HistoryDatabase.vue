<template>
  <div 
    class="history-database"
    :class="{ 'no-projects': projects.length === 0 && !loading }"
    ref="historyContainer"
  >
    <!-- Top signature Obrive gradient accent bar -->
    <div class="top-accent-bar"></div>

    <!-- Subtle technical grid background (smoothly masked into white) -->
    <div v-if="projects.length > 0 || loading" class="tech-grid-bg">
      <div class="grid-pattern"></div>
    </div>

    <!-- Obrive Signature Section Header -->
    <div class="history-header">
      <div class="brand-pill">
        <RoundedBallIcon :width="13" :height="18" />
        <span class="pill-text font-microgramma">SIMULATION REPOSITORY // ARCHIVE</span>
      </div>
      <h2 class="history-title font-microgramma">
        {{ $t('history.title') }}
      </h2>
      <p class="history-subtitle">
        Review previous multi-agent simulations, inspect consensus graph outputs, and revisit strategic reports.
      </p>
    </div>

    <!-- Project Cards Grid -->
    <div 
      v-if="projects.length > 0" 
      class="cards-grid" 
      :class="{ 'single-card': projects.length === 1 }"
    >
      <div 
        v-for="project in projects" 
        :key="project.simulation_id"
        class="project-card"
        @click="navigateToProject(project)"
      >
        <!-- Card Header: ID badge & Stage Availability Chips -->
        <div class="card-header">
          <div class="card-id-badge">
            <span class="card-id font-microgramma">{{ formatSimulationId(project.simulation_id) }}</span>
          </div>

          <div class="card-status-steps">
            <span 
              class="step-chip" 
              :class="{ active: project.project_id }"
              :title="$t('history.graphBuild')"
            >
              <span class="step-dot"></span>
              <span class="step-name font-microgramma">S1 GRAPH</span>
            </span>
            <span 
              class="step-chip active" 
              :title="$t('history.envSetup')"
            >
              <span class="step-dot"></span>
              <span class="step-name font-microgramma">S2 SWARM</span>
            </span>
            <span 
              class="step-chip" 
              :class="{ active: project.report_id }"
              :title="$t('history.analysisReport')"
            >
              <span class="step-dot"></span>
              <span class="step-name font-microgramma">S4 REPORT</span>
            </span>
          </div>
        </div>

        <!-- Reality Seed Files Box -->
        <div class="card-files-wrapper">
          <div class="files-list" v-if="project.files && project.files.length > 0">
            <div 
              v-for="(file, fileIndex) in project.files.slice(0, 2)" 
              :key="fileIndex"
              class="file-item"
            >
              <span class="file-tag" :class="getFileType(file.filename)">{{ getFileTypeLabel(file.filename) }}</span>
              <span class="file-name" :title="file.filename">{{ truncateFilename(file.filename, 32) }}</span>
            </div>
            <div v-if="project.files.length > 2" class="files-more font-microgramma">
              {{ $t('history.moreFiles', { count: project.files.length - 2 }) }}
            </div>
          </div>
          <div class="files-empty" v-else>
            <span class="empty-file-icon">📄</span>
            <span class="empty-file-text">{{ $t('history.noFiles') }}</span>
          </div>
        </div>

        <!-- Card Title -->
        <h3 class="card-title">{{ getSimulationTitle(project.simulation_requirement) }}</h3>

        <!-- Card Description Preview -->
        <p class="card-desc">{{ truncateText(project.simulation_requirement, 110) }}</p>

        <!-- Card Footer -->
        <div class="card-footer">
          <div class="card-datetime">
            <span class="card-date">{{ formatDate(project.created_at) }}</span>
            <span class="card-time-dot">•</span>
            <span class="card-time">{{ formatTime(project.created_at) }}</span>
          </div>
          
          <div class="card-footer-right">
            <span class="card-progress-pill" :class="getProgressClass(project)">
              <span class="status-dot"></span>
              <span>{{ formatRounds(project) }}</span>
            </span>
            <span class="card-action-arrow font-microgramma">↗</span>
          </div>
        </div>

        <!-- Bottom hover accent line -->
        <div class="card-bottom-line"></div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <span class="loading-spinner"></span>
      <span class="loading-text font-microgramma">{{ $t('history.loadingText') }}</span>
    </div>

    <!-- Empty State -->
    <!-- Empty State for Unauthenticated User -->
    <div v-if="!authStore.isAuthenticated.value && !loading" class="empty-state">
      <div class="empty-icon-wrap">
        <RoundedBallIcon :width="20" :height="26" />
      </div>
      <h4 class="empty-title font-microgramma">SIGN IN TO ACCESS HISTORY</h4>
      <p class="empty-text">
        Simulation history is private to your account. Please sign in to view your past simulation runs, agent logs, and intelligence reports.
      </p>
      <button class="sign-in-history-btn font-microgramma" @click="authStore.openAuthModal('login')">
        Sign In
      </button>
    </div>

    <!-- Empty State for Authenticated User with 0 simulations -->
    <div v-else-if="projects.length === 0 && !loading" class="empty-state">
      <div class="empty-icon-wrap">
        <RoundedBallIcon :width="20" :height="26" />
      </div>
      <h4 class="empty-title font-microgramma">NO RECENT SIMULATIONS</h4>
      <p class="empty-text">
        Upload reality seed documents or enter a hypothesis scenario above to launch your first multi-agent simulation.
      </p>
    </div>

    <!-- Simulation Replay Detail Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedProject" class="modal-overlay" @click.self="closeModal">
          <div class="modal-content">
            <!-- Modal Header -->
            <div class="modal-header">
              <div class="modal-title-section">
                <span class="modal-id font-microgramma">{{ formatSimulationId(selectedProject.simulation_id) }}</span>
                <span class="modal-progress" :class="getProgressClass(selectedProject)">
                  <span class="status-dot">●</span> {{ formatRounds(selectedProject) }}
                </span>
                <span class="modal-create-time">{{ formatDate(selectedProject.created_at) }} • {{ formatTime(selectedProject.created_at) }}</span>
              </div>
              <button class="modal-close" @click="closeModal" title="Close">×</button>
            </div>

            <!-- Modal Body -->
            <div class="modal-body">
              <!-- Simulation Requirement -->
              <div class="modal-section">
                <div class="modal-label font-microgramma">{{ $t('history.simRequirement') }}</div>
                <div class="modal-requirement">{{ selectedProject.simulation_requirement || $t('common.none') }}</div>
              </div>

              <!-- Related Files -->
              <div class="modal-section">
                <div class="modal-label font-microgramma">{{ $t('history.relatedFiles') }}</div>
                <div class="modal-files" v-if="selectedProject.files && selectedProject.files.length > 0">
                  <div v-for="(file, index) in selectedProject.files" :key="index" class="modal-file-item">
                    <span class="file-tag" :class="getFileType(file.filename)">{{ getFileTypeLabel(file.filename) }}</span>
                    <span class="modal-file-name">{{ file.filename }}</span>
                  </div>
                </div>
                <div class="modal-empty" v-else>{{ $t('history.noRelatedFiles') }}</div>
              </div>
            </div>

            <!-- Modal Pipeline Replay Divider -->
            <div class="modal-divider">
              <span class="divider-line"></span>
              <span class="divider-text font-microgramma">{{ $t('history.replayTitle') }}</span>
              <span class="divider-line"></span>
            </div>

            <!-- Navigation Actions -->
            <div class="modal-actions">
              <button 
                class="modal-btn btn-project" 
                @click="goToProject"
                :disabled="!selectedProject.project_id"
              >
                <span class="btn-step font-microgramma">Step 01</span>
                <span class="btn-icon">◇</span>
                <span class="btn-text font-microgramma">{{ $t('history.step1Button') }}</span>
              </button>
              <button 
                class="modal-btn btn-simulation" 
                @click="goToSimulation"
              >
                <span class="btn-step font-microgramma">Step 02</span>
                <span class="btn-icon">◈</span>
                <span class="btn-text font-microgramma">{{ $t('history.step2Button') }}</span>
              </button>
              <button 
                class="modal-btn btn-report" 
                @click="goToReport"
                :disabled="!selectedProject.report_id"
              >
                <span class="btn-step font-microgramma">Step 04</span>
                <span class="btn-icon">◆</span>
                <span class="btn-text font-microgramma">{{ $t('history.step4Button') }}</span>
              </button>
            </div>

            <!-- Replay Hint -->
            <div class="modal-playback-hint">
              <span class="hint-text">{{ $t('history.replayHint') }}</span>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getSimulationHistory } from '../api/simulation'
import RoundedBallIcon from './common/RoundedBallIcon.vue'
import authStore from '../store/auth'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()

// State
const projects = ref([])
const loading = ref(true)
const historyContainer = ref(null)
const selectedProject = ref(null)

// Format simulation_id (first 6 chars capitalized)
const formatSimulationId = (simulationId) => {
  if (!simulationId) return 'SIM_UNKNOWN'
  const prefix = simulationId.replace('sim_', '').slice(0, 6)
  return `SIM_${prefix.toUpperCase()}`
}

// Progress class
const getProgressClass = (simulation) => {
  const current = simulation.current_round || 0
  const total = simulation.total_rounds || 0
  
  if (total === 0 || current === 0) {
    return 'not-started'
  } else if (current >= total) {
    return 'completed'
  } else {
    return 'in-progress'
  }
}

// Date formatter
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  } catch {
    return dateStr?.slice(0, 10) || ''
  }
}

// Time formatter
const formatTime = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  } catch {
    return ''
  }
}

// Truncate text
const truncateText = (text, maxLength) => {
  if (!text) return ''
  const clean = text.replace(/^[#\s]+/, '').replace(/[\r\n]+/g, ' ').trim()
  return clean.length > maxLength ? clean.slice(0, maxLength) + '...' : clean
}

// Clean simulation title (up to 75 characters, wrapped nicely)
const getSimulationTitle = (requirement) => {
  if (!requirement) return t('history.untitledSimulation')
  const clean = requirement.replace(/^[#\s]+/, '').replace(/[\r\n]+/g, ' ').trim()
  return clean.length > 75 ? clean.slice(0, 75) + '...' : clean
}

// Format rounds
const formatRounds = (simulation) => {
  const current = simulation.current_round || 0
  const total = simulation.total_rounds || 0
  if (total === 0) return t('history.notStarted')
  return t('history.roundsProgress', { current, total })
}

// File type detection
const getFileType = (filename) => {
  if (!filename) return 'other'
  const ext = filename.split('.').pop()?.toLowerCase()
  const typeMap = {
    'pdf': 'pdf',
    'doc': 'doc', 'docx': 'doc',
    'xls': 'xls', 'xlsx': 'xls', 'csv': 'xls',
    'ppt': 'ppt', 'pptx': 'ppt',
    'txt': 'txt', 'md': 'md', 'json': 'code',
    'jpg': 'img', 'jpeg': 'img', 'png': 'img', 'gif': 'img',
    'zip': 'zip', 'rar': 'zip', '7z': 'zip'
  }
  return typeMap[ext] || 'other'
}

// File type badge label
const getFileTypeLabel = (filename) => {
  if (!filename) return 'FILE'
  const ext = filename.split('.').pop()?.toUpperCase()
  return ext || 'FILE'
}

// Truncate filename preserving extension
const truncateFilename = (filename, maxLength) => {
  if (!filename) return t('history.unknownFile')
  if (filename.length <= maxLength) return filename
  
  const ext = filename.includes('.') ? '.' + filename.split('.').pop() : ''
  const nameWithoutExt = filename.slice(0, filename.length - ext.length)
  const truncatedName = nameWithoutExt.slice(0, maxLength - ext.length - 3) + '...'
  return truncatedName + ext
}

// Open project detail modal
const navigateToProject = (simulation) => {
  selectedProject.value = simulation
}

// Close modal
const closeModal = () => {
  selectedProject.value = null
}

// Navigate to Step 1: Graph Build
const goToProject = () => {
  if (selectedProject.value?.project_id) {
    router.push({
      name: 'Process',
      params: { projectId: selectedProject.value.project_id }
    })
    closeModal()
  }
}

// Navigate to Step 2: Env / Simulation
const goToSimulation = () => {
  if (selectedProject.value?.simulation_id) {
    router.push({
      name: 'Simulation',
      params: { simulationId: selectedProject.value.simulation_id }
    })
    closeModal()
  }
}

// Navigate to Step 4: Analysis Report
const goToReport = () => {
  if (selectedProject.value?.report_id) {
    router.push({
      name: 'Report',
      params: { reportId: selectedProject.value.report_id }
    })
    closeModal()
  }
}

let inFlightHistory = false
// Load history items
const loadHistory = async () => {
  if (!authStore.isAuthenticated.value) {
    projects.value = []
    loading.value = false
    return
  }
  if (inFlightHistory) return
  inFlightHistory = true
  try {
    loading.value = true
    const response = await getSimulationHistory(20)
    if (response.success) {
      projects.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load simulation history:', error)
  } finally {
    loading.value = false
    inFlightHistory = false
  }
}

watch(() => authStore.isAuthenticated.value, (isAuth) => {
  if (isAuth) {
    loadHistory()
  } else {
    projects.value = []
    loading.value = false
  }
})

watch(() => route.path, (newPath) => {
  if (newPath === '/console' || newPath === '/') {
    loadHistory()
  }
})

onMounted(async () => {
  await nextTick()
  await loadHistory()
})

onActivated(() => {
  loadHistory()
})
</script>

<style scoped>
/* Main Obrive Card Container */
.history-database {
  position: relative;
  width: 100%;
  background: #FFFFFF;
  border: 1px solid rgba(7, 57, 51, 0.14);
  border-radius: 16px;
  padding: 38px 32px 42px;
  box-shadow: 0 8px 30px rgba(7, 57, 51, 0.06);
  overflow: hidden;
  margin-top: 10px;
}

.history-database.no-projects {
  padding: 36px 24px;
}

/* Top Accent Bar */
.top-accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #073933;
}

/* Subtle Technical Grid Background */
.tech-grid-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#E0E0E0 1.2px, transparent 1.2px);
  background-size: 20px 20px;
  background-position: top center;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 25%, black 25%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 25%, black 25%, transparent 75%);
  opacity: 0.85;
}

/* Header Section */
.history-header {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 32px;
}

.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px;
  background: #F4FCF9;
  border: 1px solid rgba(7, 57, 51, 0.25);
  border-radius: 9999px;
  margin-bottom: 12px;
}

.pill-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  font-weight: 700;
  color: #073933;
  letter-spacing: 0.08em;
}

.history-title {
  font-family: microgrammaBold, "microgrammaBold Fallback", var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.65rem;
  font-weight: 800;
  color: #000000;
  letter-spacing: -0.01em;
  margin: 0 0 8px 0;
}

.history-subtitle {
  font-size: 0.88rem;
  color: #2d554c;
  max-width: 620px;
  line-height: 1.5;
  margin: 0;
  font-weight: 500;
}

/* Responsive Cards Grid */
.cards-grid {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
  gap: 20px;
  width: 100%;
}

/* If only 1 card, give it a prominent centered container */
.cards-grid.single-card {
  max-width: 480px;
  margin: 0 auto;
}

/* Project Card */
.project-card {
  position: relative;
  background: #FFFFFF;
  border: 1px solid rgba(7, 57, 51, 0.14);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.04);
  transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.project-card:hover {
  border-color: #073933;
  box-shadow: 0 10px 28px rgba(7, 57, 51, 0.1);
  transform: translateY(-3px);
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(7, 57, 51, 0.1);
}

.card-id-badge {
  display: inline-flex;
  align-items: center;
  background: #073933;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid #073933;
}

.card-id {
  font-family: var(--font-mono, monospace);
  font-size: 0.72rem;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: 0.06em;
}

/* Card Pipeline Stage Availability Chips */
.card-status-steps {
  display: flex;
  align-items: center;
  gap: 6px;
}

.step-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 7px;
  border-radius: 4px;
  background: #F4FCF9;
  border: 1px solid rgba(7, 57, 51, 0.16);
  opacity: 0.55;
  transition: all 0.2s ease;
}

.step-chip.active {
  opacity: 1;
  background: #073933;
  border-color: #073933;
}

.step-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #CCCCCC;
}

.step-chip.active .step-dot {
  background: #00E5A3;
  box-shadow: 0 0 4px #00E5A3;
}

.step-name {
  font-family: var(--font-mono, monospace);
  font-size: 0.62rem;
  font-weight: 700;
  color: #2d554c;
  letter-spacing: 0.04em;
}

.step-chip.active .step-name {
  color: #FFFFFF;
}

/* Reality Seed Files Box */
.card-files-wrapper {
  background: #F7FDFB;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 14px;
  min-height: 42px;
  display: flex;
  align-items: center;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.file-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 18px;
  padding: 0 5px;
  border-radius: 3px;
  font-family: var(--font-mono, monospace);
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  flex-shrink: 0;
  background: #000000;
  color: #FFFFFF;
}

.file-tag.md, .file-tag.txt { background: #000000; color: #FFFFFF; }
.file-tag.pdf { background: #E53935; color: #FFFFFF; }
.file-tag.doc { background: #1E88E5; color: #FFFFFF; }

.file-name {
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  color: #073933;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.files-more {
  font-family: var(--font-mono, monospace);
  font-size: 0.6rem;
  font-weight: 700;
  color: #2d554c;
  padding-left: 2px;
}

.files-empty {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #2d554c;
  font-family: var(--font-mono, monospace);
  font-size: 0.72rem;
}

/* Card Title */
.card-title {
  font-family: microgrammaBold, "microgrammaBold Fallback", var(--font-display, "Space Grotesk", sans-serif);
  font-size: 0.98rem;
  font-weight: 700;
  color: #000000;
  margin: 0 0 6px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.project-card:hover .card-title {
  color: #073933;
}

/* Card Description */
.card-desc {
  font-size: 0.82rem;
  color: #2d554c;
  margin: 0 0 16px 0;
  line-height: 1.5;
  height: 36px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  font-weight: 450;
}

/* Card Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(7, 57, 51, 0.1);
  margin-top: auto;
}

.card-datetime {
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  color: #2d554c;
  font-weight: 500;
}

.card-time-dot {
  opacity: 0.4;
}

.card-footer-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-progress-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono, monospace);
  font-size: 0.66rem;
  font-weight: 600;
  background: #F5F5F5;
  border: 1px solid #E5E5E5;
  color: #000000;
}

.card-progress-pill .status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #000000;
}

.card-progress-pill.completed {
  background: #F0FFF4;
  border-color: #B8E8C4;
  color: #2E7D32;
}
.card-progress-pill.completed .status-dot {
  background: #2E7D32;
}

.card-progress-pill.in-progress {
  background: #FFFDF0;
  border-color: #F0E4B0;
  color: #A08940;
}
.card-progress-pill.in-progress .status-dot {
  background: #073933;
}

.card-progress-pill.not-started {
  background: #FAFAFA;
  border-color: #EEEEEE;
  color: #888888;
}
.card-progress-pill.not-started .status-dot {
  background: #CCCCCC;
}

.card-action-arrow {
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  color: #000000;
  opacity: 0.4;
  transition: all 0.2s ease;
}

.project-card:hover .card-action-arrow {
  opacity: 1;
  color: #073933;
  transform: translate(2px, -2px);
}

/* Bottom hover accent line */
.card-bottom-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 0;
  background: #073933;
  transition: width 0.3s cubic-bezier(0.19, 1, 0.22, 1);
}

.project-card:hover .card-bottom-line {
  width: 100%;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px;
  color: #2d554c;
}

.loading-spinner {
  width: 26px;
  height: 26px;
  border: 2px solid rgba(7, 57, 51, 0.16);
  border-top-color: #073933;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #073933;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 36px 20px;
}

.empty-icon-wrap {
  margin-bottom: 12px;
  opacity: 0.8;
}

.empty-title {
  font-family: microgrammaBold, "microgrammaBold Fallback", var(--font-mono, monospace);
  font-size: 0.88rem;
  font-weight: 800;
  color: #000000;
  letter-spacing: 0.06em;
  margin: 0 0 6px 0;
}

.empty-text {
  font-size: 0.84rem;
  color: #2d554c;
  max-width: 440px;
  line-height: 1.5;
  margin: 0;
  font-weight: 500;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background: #FFFFFF;
  width: 580px;
  max-width: 92vw;
  max-height: 85vh;
  overflow-y: auto;
  border: 1px solid #CCCCCC;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #EEEEEE;
  background: #FFFFFF;
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.modal-id {
  font-family: var(--font-mono, monospace);
  font-size: 0.95rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.05em;
}

.modal-progress {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono, monospace);
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  background: #F5F5F5;
  border: 1px solid #E5E5E5;
  color: #000000;
}

.modal-create-time {
  font-family: var(--font-mono, monospace);
  font-size: 0.72rem;
  color: #888888;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: 1px solid #E5E5E5;
  background: #FAFAFA;
  font-size: 1.3rem;
  color: #000000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #000000;
  color: #FFFFFF;
  border-color: #000000;
}

.modal-body {
  padding: 24px;
}

.modal-section {
  margin-bottom: 20px;
}

.modal-section:last-child {
  margin-bottom: 0;
}

.modal-label {
  font-family: var(--font-mono, monospace);
  font-size: 0.72rem;
  font-weight: 700;
  color: #666666;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

.modal-requirement {
  font-family: var(--font-mono, monospace);
  font-size: 0.88rem;
  color: #000000;
  line-height: 1.6;
  padding: 14px 16px;
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  max-height: 220px;
  overflow-y: auto;
}

.modal-files {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 160px;
  overflow-y: auto;
}

.modal-file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #FAFAFA;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
}

.modal-file-name {
  font-family: var(--font-mono, monospace);
  font-size: 0.82rem;
  color: #000000;
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.modal-empty {
  font-family: var(--font-mono, monospace);
  font-size: 0.8rem;
  color: #888888;
  padding: 14px;
  background: #FAFAFA;
  border: 1px dashed #DDDDDD;
  border-radius: 6px;
  text-align: center;
}

.modal-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 24px 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: #EEEEEE;
}

.divider-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  font-weight: 700;
  color: #999999;
  letter-spacing: 0.08em;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 18px 24px;
}

.modal-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 10px;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-btn:hover:not(:disabled) {
  border-color: #000000;
  background: #FAFAFA;
  transform: translateY(-2px);
}

.modal-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  background: #F9FAFB;
}

.modal-btn.btn-report:not(:disabled) {
  background: #000000;
  border-color: #000000;
}

.modal-btn.btn-report:not(:disabled) .btn-step,
.modal-btn.btn-report:not(:disabled) .btn-icon,
.modal-btn.btn-report:not(:disabled) .btn-text {
  color: #FFFFFF;
}

.modal-btn.btn-report:not(:disabled):hover {
  background: #FF4500;
  border-color: #FF4500;
}

.btn-step {
  font-family: var(--font-mono, monospace);
  font-size: 0.6rem;
  font-weight: 700;
  color: #888888;
  letter-spacing: 0.05em;
}

.btn-icon {
  font-size: 1.2rem;
  line-height: 1;
  color: #000000;
}

.btn-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.74rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.04em;
}

.modal-playback-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px 18px;
}

.hint-text {
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  color: #888888;
  text-align: center;
  line-height: 1.4;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .history-database {
    padding: 28px 18px 32px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }
}

.sign-in-history-btn {
  margin-top: 14px;
  background: #000000;
  color: #A2F1DF;
  border: 1px solid #000000;
  padding: 8px 22px;
  border-radius: 9999px;
  font-family: microgrammaBold, "microgrammaBold Fallback", var(--font-mono, monospace);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.2s ease;
}

.sign-in-history-btn:hover {
  background: #073933;
  color: #FFFFFF;
  border-color: #073933;
  transform: translateY(-1px);
}
</style>
