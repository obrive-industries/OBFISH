<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-brand-container">
        <img src="../assets/logo/obrive-logo.svg" alt="Brain Logo" class="brand-logo-img" />
        <span class="nav-brand">BRAIN<span class="brand-tm">TM</span></span>
      </div>
      <div class="nav-links">
        <!-- Auth Button / User Pill -->
        <div v-if="authStore.isAuthenticated.value" class="user-nav-pill" @click="authStore.openProfileModal">
          <div class="user-avatar-small">{{ userInitials }}</div>
          <span class="user-nav-name">{{ authStore.user.value?.full_name || 'My Account' }}</span>
          <span v-if="authStore.isVerified.value" class="user-status-dot verified" title="Email Verified">●</span>
          <span v-else class="user-status-dot unverified" title="Email Not Verified">●</span>
        </div>

        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="website-link">
          {{ $t('nav.visitWebsite') }} <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- 上半部分：Hero 区域 -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="obrive-tag">{{ $t('home.tagline') }}</span>
            <span class="version-text">{{ $t('home.version') }}</span>
          </div>
          
          <h1 class="main-title">
            {{ $t('home.heroTitle1') }}<br>
            <span class="gradient-text">{{ $t('home.heroTitle2') }}</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <i18n-t keypath="home.heroDesc" tag="span">
                <template #brand><span class="highlight-bold">{{ $t('home.heroDescBrand') }}</span></template>
                <template #agentScale><span class="highlight-brand">{{ $t('home.heroDescAgentScale') }}</span></template>
                <template #optimalSolution><span class="highlight-code">{{ $t('home.heroDescOptimalSolution') }}</span></template>
              </i18n-t>
            </p>
            <p class="slogan-text">
              {{ $t('home.slogan') }}<span class="blinking-cursor">_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Mascot & Brand Showcase directly embedded into Hero -->
          <div class="hero-brand-embedded">
            <div class="mascot-frame">
              <img src="../assets/logo/obfish-mascot.png" alt="Brain Swarm Mascot" class="hero-mascot-img" />
            </div>
            <div class="hero-brand-name">BRAIN</div>
            <div class="hero-brand-desc">Swarm Intelligence Simulation Platform</div>
            <div class="hero-brand-pill">
              <span class="pill-dot"></span> Powered by Obrive AI
            </div>
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- 下半部分：双栏布局 -->
      <section class="dashboard-section">
        <!-- 左栏：状态与步骤 -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> {{ $t('home.systemStatus') }}
          </div>
          
          <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
          <p class="section-desc">
            {{ $t('home.systemReadyDesc') }}
          </p>
          
          <!-- 数据指标卡片 -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
              <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
              <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
            </div>
          </div>

          <!-- 项目模拟步骤介绍 (新增区域) -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step01Title') }}</div>
                  <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step02Title') }}</div>
                  <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step03Title') }}</div>
                  <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step04Title') }}</div>
                  <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step05Title') }}</div>
                  <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右栏：交互控制台 -->
        <div class="right-panel">
          <div class="console-box">
            <!-- 上传区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.realitySeed') }}</span>
                <span class="console-meta">{{ $t('home.supportedFormats') }}</span>
              </div>
              
              <div 
                class="upload-zone"
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
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                  <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 分割线 -->
            <div class="console-divider">
              <span>{{ $t('home.inputParams') }}</span>
            </div>

            <!-- 输入区域 -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  :placeholder="$t('home.promptPlaceholder')"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">{{ $t('home.engineBadge') }}</div>
              </div>
            </div>

            <!-- 启动按钮 -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                <span v-else>{{ $t('home.initializing') }}</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 历史项目数据库 -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import authStore from '../store/auth'

const router = useRouter()

const userInitials = computed(() => {
  const name = authStore.user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

// 表单数据
const formData = ref({
  simulationRequirement: ''
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// 文件输入引用
const fileInput = ref(null)

// 计算属性:是否可以提交
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== ''
})

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'docx', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = async () => {
  if (!canSubmit.value || loading.value) return
  
  // 存储待上传的数据到 IndexedDB
  const { savePendingUpload } = await import('../utils/pendingUpload.js')
  await savePendingUpload(files.value, formData.value.simulationRequirement)

  if (!authStore.isAuthenticated.value) {
    authStore.openAuthModal('login')
    return
  }

  // 立即跳转到Process页面（使用特殊标识表示新建项目）
  router.push({
    name: 'Process',
    params: { projectId: 'new' }
  })
}
</script>

<style scoped>
/* 全局变量与重置 */
:root {
  --black: #074139;
  --white: #A2F1DF;
  --card-bg: #FFFFFF;
  --obrive-primary: #074139;
  --obrive-primary-dark: #052e28;
  --obrive-primary-light: #0d5c52;
  --obrive-accent: #a2f1df;
  --orange: #074139;
  --gray-light: #E0F7F2;
  --gray-text: #083c34;
  --border: rgba(7, 65, 57, 0.2);
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: #A2F1DF;
  font-family: var(--font-sans);
  color: var(--black);
}

/* 顶部导航 */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 64px;
  background: rgba(162, 241, 223, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #074139;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid rgba(7, 65, 57, 0.12);
  box-shadow: 0 2px 10px rgba(7, 65, 57, 0.05);
}

.nav-brand-container {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.brand-logo-img {
  height: 28px;
  width: auto;
}

.nav-brand {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-weight: 700;
  -webkit-text-stroke: 0.6px #074139;
  paint-order: stroke fill;
  letter-spacing: 2.5px;
  font-size: 1.32rem;
  color: #074139;
  display: inline-flex;
  align-items: flex-start;
  line-height: 1;
}

.brand-tm {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 0.52rem;
  font-weight: 700;
  -webkit-text-stroke: 0.25px #074139;
  margin-left: 3px;
  margin-top: -2px;
  opacity: 0.9;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 14px;
}

.sign-in-btn {
  background: #074139;
  color: #A2F1DF;
  border: 1px solid #074139;
  border-radius: 9999px;
  padding: 6px 18px;
  font-size: 0.86rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.3px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(7, 65, 57, 0.15);
}

.sign-in-btn:hover {
  background: #052e28;
  transform: translateY(-1px);
}

.user-nav-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(7, 65, 57, 0.25);
  border-radius: 9999px;
  padding: 4px 12px 4px 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(7, 65, 57, 0.08);
}

.user-nav-pill:hover {
  background: #FFFFFF;
  border-color: #074139;
  box-shadow: 0 3px 10px rgba(7, 65, 57, 0.15);
}

.user-avatar-small {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #074139;
  color: #A2F1DF;
  font-size: 0.72rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-nav-name {
  font-size: 0.84rem;
  font-weight: 600;
  color: #074139;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-status-dot {
  font-size: 0.6rem;
  line-height: 1;
}

.user-status-dot.verified {
  color: #10B981;
}

.user-status-dot.unverified {
  color: #F59E0B;
}

.website-link {
  color: #074139;
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.88rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border: 1px solid rgba(7, 65, 57, 0.25);
  border-radius: 9999px;
  background: rgba(7, 65, 57, 0.06);
  transition: all 0.2s ease;
}

.website-link:hover {
  background: #074139;
  color: #A2F1DF;
  border-color: #074139;
  box-shadow: 0 2px 8px rgba(7, 65, 57, 0.2);
}

.arrow {
  font-family: sans-serif;
}

/* 主要内容区 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.obrive-tag {
  background: #074139;
  color: #A2F1DF;
  padding: 6px 16px;
  font-weight: 700;
  letter-spacing: 0.5px;
  font-size: 0.75rem;
  border-radius: 9999px;
  border: 1px solid #074139;
  box-shadow: 0 2px 8px rgba(7, 65, 57, 0.15);
}

.version-text {
  color: #074139;
  font-weight: 600;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 600;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: #074139;
}

.gradient-text {
  background: linear-gradient(90deg, #074139 0%, #0d5c52 50%, #00705f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: #08433a;
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 500;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: #074139;
  font-weight: 800;
}

.highlight-brand {
  color: #074139;
  font-weight: 800;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(7, 65, 57, 0.14);
  padding: 2px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: #074139;
  font-weight: 700;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #074139;
  letter-spacing: 1px;
  border-left: 3.5px solid #074139;
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: #074139;
  animation: blink 1s step-end infinite;
  font-weight: 800;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: #074139;
  border-radius: 3px;
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 20px;
}

.hero-brand-embedded {
  position: relative;
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.mascot-frame {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.hero-mascot-img {
  width: 100%;
  max-width: 420px;
  object-fit: contain;
  filter: drop-shadow(0 18px 25px rgba(7, 65, 57, 0.22));
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), filter 0.3s ease;
}

.hero-mascot-img:hover {
  transform: translateY(-6px) scale(1.03);
  filter: drop-shadow(0 24px 30px rgba(7, 65, 57, 0.3));
}

.hero-brand-name {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  -webkit-text-stroke: 1px #074139;
  paint-order: stroke fill;
  letter-spacing: 3px;
  color: #074139;
  margin-bottom: 6px;
}

.hero-brand-desc {
  font-size: 1rem;
  color: #074139;
  font-weight: 600;
  margin-bottom: 18px;
  opacity: 0.9;
}

.hero-brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.6);
  border: 1.5px solid #074139;
  border-radius: 9999px;
  font-size: 0.85rem;
  color: #074139;
  font-weight: 700;
  box-shadow: 0 4px 14px rgba(7, 65, 57, 0.12);
  backdrop-filter: blur(8px);
}

.pill-dot {
  width: 8px;
  height: 8px;
  background: #074139;
  border-radius: 50%;
  box-shadow: 0 0 6px #074139;
}

.scroll-down-btn {
  width: 44px;
  height: 44px;
  border: 1.5px solid #074139;
  background: #FFFFFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #074139;
  font-size: 1.2rem;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(7, 65, 57, 0.1);
}

.scroll-down-btn:hover {
  border-color: #074139;
  background: #074139;
  color: #a2f1df;
  transform: translateY(2px);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #526361;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: #10B981;
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
  color: #111827;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid rgba(7, 65, 57, 0.14);
  border-radius: 12px;
  padding: 20px 30px;
  min-width: 150px;
  background: #FAFDFD;
  transition: all 0.2s ease;
}

.metric-card:hover {
  border-color: rgba(7, 65, 57, 0.3);
  box-shadow: 0 4px 12px rgba(7, 65, 57, 0.05);
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: #074139;
}

.metric-label {
  font-size: 0.85rem;
  color: #526361;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid rgba(7, 65, 57, 0.14);
  border-radius: 14px;
  padding: 30px;
  position: relative;
  background: #FFFFFF;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #526361;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
  color: #074139;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 800;
  color: #074139;
  opacity: 0.75;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 4px;
  color: #111827;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 16px;
  padding: 8px;
  background: #FFFFFF;
  box-shadow: 0 4px 20px -2px rgba(7, 65, 57, 0.06);
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #526361;
}

.upload-zone {
  border: 1.5px dashed rgba(7, 65, 57, 0.25);
  border-radius: 12px;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #F8FAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: rgba(162, 241, 223, 0.08);
  border-color: #074139;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #074139;
  background: #FFFFFF;
}

.upload-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 5px;
  color: #111827;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #526361;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid rgba(7, 65, 57, 0.15);
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.remove-btn:hover {
  color: #ef4444;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(7, 65, 57, 0.1);
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #526361;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1.5px solid rgba(7, 65, 57, 0.18);
  border-radius: 10px;
  background: #FAFDFD;
  transition: all 0.2s ease;
}

.input-wrapper:focus-within {
  border-color: #074139;
  box-shadow: 0 0 0 3px rgba(162, 241, 223, 0.4);
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
  color: #111827;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #074139;
  background: rgba(162, 241, 223, 0.2);
  padding: 2px 8px;
  border-radius: 4px;
}

.start-engine-btn {
  width: 100%;
  border-radius: 12px;
  border: none;
  padding: 20px 24px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.05rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: #074139;
  color: #a2f1df;
  border: 1px solid #074139;
  box-shadow: 0 4px 15px rgba(7, 65, 57, 0.2);
  animation: pulse-border 2.5s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: #052e28;
  color: #FFFFFF;
  border-color: #052e28;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(7, 65, 57, 0.35);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E7EB;
  color: #9CA3AF;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E7EB;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(7, 65, 57, 0.3); }
  70% { box-shadow: 0 0 0 8px rgba(7, 65, 57, 0); }
  100% { box-shadow: 0 0 0 0 rgba(7, 65, 57, 0); }
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>

<style>
/* English locale adjustments (unscoped to target html[lang]) */
html[lang="en"] .main-title {
  font-size: 3.2rem;
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: -0.5px;
}

html[lang="en"] .hero-desc {
  text-align: left;
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .slogan-text {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .tag-row {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .navbar .nav-links {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Left pane: system status + workflow */
html[lang="en"] .status-section {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .status-section .status-ready {
  font-size: 1.4rem;
}

html[lang="en"] .status-section .metric-value {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 1.2rem;
}

html[lang="en"] .workflow-list .step-title {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .workflow-list .step-desc {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-size: 0.68rem !important;
  line-height: 1.4 !important;
}

html[lang="en"] .workflow-list {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
