<template>
  <div class="step1-upload-card obrive-card">
    <!-- Header -->
    <div class="card-header-bar">
      <div class="header-left">
        <span class="badge-num font-microgramma">01</span>
        <h3 class="header-title font-microgramma">{{ title || 'Scenario & Context Ingestion' }}</h3>
      </div>
      <div class="header-status">
        <span v-if="files.length > 0" class="status-pill docs-pill">
          📄 {{ files.length }} Document{{ files.length > 1 ? 's' : '' }} Attached
        </span>
        <span v-else-if="formData.simulationRequirement.trim().length > 0" class="status-pill text-pill">
          ✍️ Text Hypothesis Mode
        </span>
        <span v-else class="status-pill ready-pill">
          Waiting for Input
        </span>
      </div>
    </div>

    <!-- Description -->
    <p class="section-description">
      Upload reality seed documents (PDF, DOCX, MD, TXT) or enter a natural language scenario hypothesis below. Physical files are optional—the engine can simulate directly from your prompt.
    </p>

    <!-- Upload Dropzone (Optional) -->
    <div class="upload-zone-wrapper">
      <div class="section-subheading">
        <span class="subheading-title font-microgramma">REALITY SEED DOCUMENTS</span>
        <span class="subheading-hint">Optional · PDF, DOCX, MD, TXT up to 50MB</span>
      </div>

      <div 
        class="dropzone-area"
        :class="{ 'is-dragging': isDragging, 'has-files': files.length > 0 }"
        @dragover.prevent="onDragOver"
        @dragleave.prevent="onDragLeave"
        @drop.prevent="onDrop"
        @click="openFilePicker"
      >
        <input 
          ref="fileInputRef"
          type="file"
          multiple
          accept=".pdf,.docx,.md,.txt"
          class="hidden-file-input"
          @change="onFilesSelected"
        />

        <div v-if="files.length === 0" class="dropzone-prompt">
          <div class="dropzone-icon">↑</div>
          <span class="prompt-main">Drag & drop source documents here (optional)</span>
          <span class="prompt-sub">or click to browse from device · DOCX, PDF, MD, TXT</span>
        </div>

        <div v-else class="file-badges-container">
          <div 
            v-for="(file, idx) in files" 
            :key="idx" 
            class="file-badge-pill"
            @click.stop
          >
            <span class="badge-icon">📄</span>
            <span class="badge-filename" :title="file.name">{{ file.name }}</span>
            <span class="badge-size">({{ formatFileSize(file.size) }})</span>
            <button 
              type="button" 
              class="badge-remove-btn" 
              title="Remove file"
              @click.stop="removeFile(idx)"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Hypothesis / Scenario Prompt -->
    <div class="hypothesis-wrapper">
      <div class="section-subheading">
        <span class="subheading-title font-microgramma">SIMULATION REQUIREMENT & HYPOTHESIS</span>
        <span class="subheading-hint">Natural language prompt · Required</span>
      </div>

      <div class="textarea-container">
        <textarea
          v-model="formData.simulationRequirement"
          class="hypothesis-textarea"
          rows="5"
          placeholder="Describe your scenario, strategic dilemma, market hypothesis, or stakeholder debate. If no files are attached, this text will serve directly as the seed document..."
          :disabled="loading"
        ></textarea>
        
        <div class="textarea-footer">
          <span class="char-count">{{ formData.simulationRequirement.length }} chars</span>
          <div class="mode-indicator">
            <span class="mode-dot" :class="{ 'active': canProceed }"></span>
            <span class="mode-text">{{ files.length > 0 ? 'Document-grounded mode' : 'Prompt-only hypothesis mode' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="card-action-bar">
      <button 
        type="button"
        class="btn-submit font-microgramma"
        :class="{ 'btn-enabled': canProceed && !loading }"
        :disabled="!canProceed || loading"
        @click="handleSubmit"
      >
        <span v-if="!loading">
          {{ submitLabel || 'Start Engine & Construct Graph' }} →
        </span>
        <span v-else>
          Processing Scenario...
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authStore from '../store/auth'
import { savePendingUpload, getPendingUpload } from '../utils/pendingUpload.js'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  submitLabel: {
    type: String,
    default: ''
  },
  autoNavigate: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['submit', 'files-changed', 'requirement-changed'])

const router = useRouter()
const fileInputRef = ref(null)
const isDragging = ref(false)
const loading = ref(false)

const formData = ref({
  simulationRequirement: ''
})
const files = ref([])

const canProceed = computed(() => {
  return formData.value.simulationRequirement.trim().length > 0
})

onMounted(async () => {
  try {
    const pending = await getPendingUpload()
    if (pending && pending.isPending) {
      if (pending.simulationRequirement) {
        formData.value.simulationRequirement = pending.simulationRequirement
      }
      if (pending.files && pending.files.length > 0) {
        files.value = pending.files
      }
    }
  } catch (e) {
    console.warn('Failed to restore pending upload in Step1Upload:', e)
  }
})

const openFilePicker = () => {
  if (!loading.value) {
    fileInputRef.value?.click()
  }
}

const onFilesSelected = (e) => {
  const selected = Array.from(e.target.files)
  addValidFiles(selected)
}

const onDragOver = () => {
  if (!loading.value) isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}

const onDrop = (e) => {
  isDragging.value = false
  if (loading.value) return
  const dropped = Array.from(e.dataTransfer.files)
  addValidFiles(dropped)
}

const MAX_SIZE = 50 * 1024 * 1024 // 50MB
const addValidFiles = (newFiles) => {
  const valid = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    const isAllowed = ['pdf', 'docx', 'md', 'txt'].includes(ext)
    const isUnderLimit = file.size <= MAX_SIZE
    if (!isUnderLimit) {
      alert(`File "${file.name}" exceeds the 50MB limit.`)
    }
    return isAllowed && isUnderLimit
  })
  files.value.push(...valid)
  emit('files-changed', files.value)
}

const removeFile = (idx) => {
  files.value.splice(idx, 1)
  emit('files-changed', files.value)
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const handleSubmit = async () => {
  if (!canProceed.value || loading.value) return

  // Persist directly to IndexedDB
  await savePendingUpload(files.value, formData.value.simulationRequirement)

  emit('submit', {
    files: files.value,
    simulationRequirement: formData.value.simulationRequirement
  })

  if (props.autoNavigate) {
    if (!authStore.isAuthenticated.value) {
      authStore.openAuthModal('login', 'Please sign in to construct knowledge graph and start simulation.')
      return
    }

    loading.value = true
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  }
}
</script>

<style scoped>
.step1-upload-card {
  background: #FFFFFF;
  border: 1px solid rgba(7, 65, 57, 0.12);
  border-radius: 16px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 0 4px 20px rgba(7, 65, 57, 0.04);
}

.card-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(7, 65, 57, 0.08);
  padding-bottom: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.badge-num {
  font-size: 13px;
  font-weight: 700;
  color: #074139;
  background: #E0F7F2;
  padding: 4px 10px;
  border-radius: 20px;
  letter-spacing: 0.05em;
}

.header-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #074139;
}

.status-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
}

.docs-pill {
  background: #E0F7F2;
  color: #074139;
}

.text-pill {
  background: #F1F8F6;
  color: #0d5c52;
  border: 1px solid #A2F1DF;
}

.ready-pill {
  background: #F4F4F4;
  color: #888888;
}

.section-description {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #4a5568;
}

.section-subheading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.subheading-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
}

.subheading-hint {
  font-size: 11px;
  color: #718096;
}

.dropzone-area {
  border: 2px dashed rgba(7, 65, 57, 0.2);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  background: #FAFCFB;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropzone-area:hover,
.dropzone-area.is-dragging {
  border-color: #074139;
  background: #F0FAF6;
}

.dropzone-area.has-files {
  padding: 16px;
  text-align: left;
}

.hidden-file-input {
  display: none;
}

.dropzone-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.dropzone-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #E0F7F2;
  color: #074139;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}

.prompt-main {
  font-size: 14px;
  font-weight: 600;
  color: #074139;
}

.prompt-sub {
  font-size: 12px;
  color: #718096;
}

.file-badges-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.file-badge-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid rgba(7, 65, 57, 0.2);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  color: #074139;
}

.badge-filename {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.badge-size {
  color: #718096;
  font-size: 11px;
}

.badge-remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #A0AEC0;
  font-size: 16px;
  line-height: 1;
  padding: 0 2px;
}

.badge-remove-btn:hover {
  color: #E53E3E;
}

.hypothesis-wrapper {
  display: flex;
  flex-direction: column;
}

.textarea-container {
  position: relative;
  display: flex;
  flex-direction: column;
}

.hypothesis-textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 14px 16px;
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: #074139;
  background: #FAFCFB;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.hypothesis-textarea:focus {
  border-color: #074139;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.35);
}

.textarea-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  padding: 0 4px;
  font-size: 11px;
  color: #718096;
}

.mode-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
}

.mode-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #CBD5E0;
}

.mode-dot.active {
  background: #38A169;
}

.card-action-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.btn-submit {
  padding: 12px 24px;
  border-radius: 12px;
  border: none;
  background: #CBD5E0;
  color: #718096;
  font-size: 13px;
  font-weight: 700;
  cursor: not-allowed;
  transition: all 0.2s ease;
}

.btn-submit.btn-enabled {
  background: #074139;
  color: #A2F1DF;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(7, 65, 57, 0.2);
}

.btn-submit.btn-enabled:hover {
  background: #052e28;
  transform: translateY(-1px);
}
</style>
