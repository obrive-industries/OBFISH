<template>
  <div class="marketing-page admin-wishlist-page">
    <LandingHeader @open-auth="openAuth" />

    <main class="admin-main">
      <!-- Ambient Glow Orb matching MiroFish / FaqView -->
      <div class="admin-glow" aria-hidden="true"></div>

      <div class="admin-container">
        <!-- Hero Header -->
        <header class="admin-hero">
          <div class="category-pill">
            <RoundedBallIcon :width="14" :height="20" />
            <span class="pill-text font-michroma">ADMIN PORTAL</span>
          </div>

          <h1 class="admin-title font-microgramma">
            Wishlist & Waitlist Leads
          </h1>

          <p class="admin-intro font-michroma">
            Real-time prospective customer emails submitted via the landing page.
          </p>

          <!-- Navigation Pills -->
          <div class="admin-nav-actions">
            <router-link
              to="/"
              class="nav-pill-btn font-michroma"
            >
              ← Back to Home
            </router-link>
            <router-link
              to="/console"
              class="nav-pill-btn nav-pill-btn-primary font-michroma"
            >
              Open Console →
            </router-link>
          </div>
        </header>

        <!-- State 1: Admin Login Card (If unauthenticated or not admin) -->
        <div v-if="!isAdmin" class="admin-auth-card">
          <div class="auth-card-icon">
            <svg class="w-6 h-6 text-[#073933]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>

          <h2 class="auth-card-title font-microgramma">Administrator Access Required</h2>
          <p class="auth-card-desc font-michroma">
            Sign in with verified administrator credentials to view and manage customer waitlist emails.
          </p>

          <form @submit.prevent="handleAdminLogin" class="auth-form">
            <div v-if="loginError" class="auth-error-banner font-michroma">
              {{ loginError }}
            </div>

            <div class="form-field">
              <label class="field-label font-michroma">ADMIN EMAIL</label>
              <input
                v-model="loginForm.email"
                type="email"
                placeholder="ai@obrive.com"
                required
                class="field-input"
                :disabled="loggingIn"
              />
            </div>

            <div class="form-field">
              <label class="field-label font-michroma">PASSWORD</label>
              <input
                v-model="loginForm.password"
                type="password"
                placeholder="••••••••"
                required
                class="field-input"
                :disabled="loggingIn"
              />
            </div>

            <div class="auth-submit-wrapper">
              <button
                type="submit"
                class="auth-submit-btn font-microgramma"
                :disabled="loggingIn"
              >
                <span>{{ loggingIn ? 'Authenticating...' : 'Sign In as Admin →' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- State 2: Authenticated Admin Dashboard -->
        <div v-else class="admin-dashboard">
          <!-- Metric Cards & Actions -->
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-header">
                <span class="metric-label font-michroma">Total Subscribers</span>
                <span class="metric-icon">👥</span>
              </div>
              <div class="metric-value font-microgramma">{{ subscribers.length }}</div>
              <div class="metric-subtext font-michroma">Verified landing page signups</div>
            </div>

            <div class="metric-card">
              <div class="metric-header">
                <span class="metric-label font-michroma">Unique Domains</span>
                <span class="metric-icon">🌐</span>
              </div>
              <div class="metric-value font-microgramma text-emerald-700">{{ uniqueDomainsCount }}</div>
              <div class="metric-subtext font-michroma">Distinct corporate & user domains</div>
            </div>

            <div class="metric-card action-card">
              <div class="metric-header">
                <span class="metric-label font-michroma">Quick Actions</span>
                <span class="metric-icon">⚡</span>
              </div>
              <div class="action-buttons-group">
                <button
                  @click="copyAllEmails"
                  class="action-btn copy-btn font-michroma"
                  :disabled="subscribers.length === 0"
                >
                  <span>{{ copied ? '✓ Copied All!' : '📋 Copy All' }}</span>
                </button>
                <button
                  @click="exportCsv"
                  class="action-btn export-btn font-michroma"
                  :disabled="subscribers.length === 0 || exporting"
                >
                  <span>{{ exporting ? '⏳ Exporting...' : '📥 Export CSV' }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Filter & Search Toolbar -->
          <div class="toolbar-wrapper">
            <div class="search-input-box">
              <svg class="search-icon w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by email or domain..."
                class="search-input"
              />
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="clear-search-btn"
                title="Clear search"
              >
                ✕
              </button>
            </div>

            <div class="toolbar-right">
              <span class="leads-counter font-michroma">
                Showing {{ filteredSubscribers.length }} of {{ subscribers.length }}
              </span>
              <button
                @click="fetchSubscribers"
                class="refresh-btn"
                :class="{ 'is-loading': loading }"
                title="Refresh leads list"
              >
                <span class="refresh-icon" :class="{ 'animate-spin': loading }">↻</span>
                <span class="refresh-text font-michroma">REFRESH</span>
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="state-card loading-card">
            <div class="spinner"></div>
            <div class="state-title font-microgramma">Syncing Wishlist Submissions...</div>
            <p class="state-desc font-michroma">Fetching real-time subscriber records from database.</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredSubscribers.length === 0" class="state-card empty-card">
            <div class="empty-icon">📭</div>
            <h3 class="state-title font-microgramma">No Submissions Found</h3>
            <p class="state-desc font-michroma">
              {{ searchQuery ? 'No subscriber emails matched your search query.' : 'New submissions from the landing page will automatically appear here.' }}
            </p>
          </div>

          <!-- Data Table -->
          <div v-else class="table-card">
            <div class="overflow-x-auto">
              <table class="leads-table">
                <thead>
                  <tr>
                    <th class="th-index font-michroma">#</th>
                    <th class="th-email font-michroma">Email Address</th>
                    <th class="th-date font-michroma">Signed Up (UTC)</th>
                    <th class="th-source font-michroma">Source</th>
                    <th class="th-status font-michroma">Status</th>
                    <th class="th-actions font-michroma text-right">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(sub, idx) in filteredSubscribers"
                    :key="sub.id || idx"
                    class="table-row"
                  >
                    <td class="td-index font-mono">
                      {{ idx + 1 }}
                    </td>
                    <td class="td-email">
                      <div class="email-wrapper">
                        <span class="email-text select-all">{{ sub.email }}</span>
                        <button
                          @click="copySingleEmail(sub.email)"
                          class="copy-single-btn"
                          :title="copiedEmail === sub.email ? 'Copied!' : 'Copy email'"
                        >
                          {{ copiedEmail === sub.email ? '✓' : '❐' }}
                        </button>
                      </div>
                    </td>
                    <td class="td-date font-mono">
                      {{ formatDate(sub.created_at) }}
                    </td>
                    <td class="td-source">
                      <span class="source-badge font-mono">
                        {{ sub.source || 'landing_hero' }}
                      </span>
                    </td>
                    <td class="td-status">
                      <span class="status-badge font-michroma">
                        <span class="status-dot"></span>
                        {{ sub.status || 'active' }}
                      </span>
                    </td>
                    <td class="td-actions text-right">
                      <a
                        :href="`mailto:${sub.email}`"
                        class="contact-link font-michroma"
                        title="Send email"
                      >
                        ✉ Mail
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>

    <LandingFooter />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import authStore from '../store/auth'
import authApi from '../api/auth'
import wishlistApi from '../api/wishlist'
import LandingHeader from '../components/landing/LandingHeader.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'
import RoundedBallIcon from '../components/common/RoundedBallIcon.vue'

const subscribers = ref([])
const loading = ref(false)
const copied = ref(false)
const exporting = ref(false)
const copiedEmail = ref('')
const searchQuery = ref('')

const loggingIn = ref(false)
const loginError = ref('')
const loginForm = reactive({
  email: '',
  password: ''
})

const isAdmin = computed(() => {
  return authStore.isAdmin.value
})

const uniqueDomainsCount = computed(() => {
  const domains = new Set()
  subscribers.value.forEach(s => {
    if (s.email && s.email.includes('@')) {
      domains.add(s.email.split('@')[1].toLowerCase())
    }
  })
  return domains.size
})

const filteredSubscribers = computed(() => {
  if (!searchQuery.value.trim()) return subscribers.value
  const q = searchQuery.value.toLowerCase().trim()
  return subscribers.value.filter(s => s.email && s.email.toLowerCase().includes(q))
})

const formatDate = (isoString) => {
  if (!isoString) return '—'
  try {
    const d = new Date(isoString)
    return d.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })
  } catch {
    return isoString
  }
}

const openAuth = () => {
  authStore.openAuthModal('login')
}

const fetchSubscribers = async () => {
  if (!isAdmin.value) return
  loading.value = true
  try {
    const res = await wishlistApi.getSubscribers()
    const ok = res?.success || res?.data?.success
    if (ok) {
      subscribers.value = res?.subscribers || res?.data?.subscribers || []
    }
  } catch (err) {
    console.error('Failed to load wishlist subscribers:', err)
  } finally {
    loading.value = false
  }
}

const handleAdminLogin = async () => {
  loggingIn.value = true
  loginError.value = ''
  try {
    const res = await authApi.login({
      email: loginForm.email.trim(),
      password: loginForm.password
    })
    authStore.setSession(res.access_token, res.refresh_token, res.user)
    if (authStore.isAdmin.value) {
      await fetchSubscribers()
    } else {
      loginError.value = 'Access denied: This account does not have administrator privileges.'
    }
  } catch (err) {
    loginError.value = err.message || err.response?.data?.error || 'Failed to sign in.'
  } finally {
    loggingIn.value = false
  }
}

const copyAllEmails = async () => {
  if (subscribers.value.length === 0) return
  const emails = subscribers.value.map(s => s.email).join(', ')
  try {
    await navigator.clipboard.writeText(emails)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2500)
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
  }
}

const copySingleEmail = async (email) => {
  if (!email) return
  try {
    await navigator.clipboard.writeText(email)
    copiedEmail.value = email
    setTimeout(() => {
      if (copiedEmail.value === email) copiedEmail.value = ''
    }, 2000)
  } catch (err) {
    console.error('Failed to copy email:', err)
  }
}

const exportCsv = async () => {
  if (exporting.value) return
  exporting.value = true
  try {
    let csvBlob = null

    // 1. Attempt server-side CSV export
    try {
      const res = await wishlistApi.exportCsv()
      if (res instanceof Blob) {
        if (res.type && res.type.includes('application/json')) {
          const text = await res.text()
          const errData = JSON.parse(text)
          throw new Error(errData.error || errData.message || 'Export error')
        }
        csvBlob = res
      } else if (typeof res === 'string') {
        csvBlob = new Blob([res], { type: 'text/csv;charset=utf-8;' })
      } else if (res && res.data) {
        csvBlob = res.data instanceof Blob ? res.data : new Blob([res.data], { type: 'text/csv;charset=utf-8;' })
      }
    } catch (apiErr) {
      console.warn('Backend CSV export failed, generating from active subscriber state:', apiErr)
    }

    // 2. Client-side fallback if backend response did not yield a valid CSV blob
    if (!csvBlob) {
      if (!subscribers.value || subscribers.value.length === 0) {
        alert('No subscriber records available to export.')
        return
      }
      const headers = ['ID', 'Email Address', 'Source', 'Status', 'Subscribed At (UTC)']
      const rows = subscribers.value.map((sub, idx) => [
        sub.id || idx + 1,
        `"${(sub.email || '').replace(/"/g, '""')}"`,
        `"${(sub.source || 'landing_hero').replace(/"/g, '""')}"`,
        `"${(sub.status || 'active').replace(/"/g, '""')}"`,
        `"${(sub.created_at || '').replace(/"/g, '""')}"`
      ])
      const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n')
      // Prepend UTF-8 BOM for flawless Excel encoding
      csvBlob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
    }

    // 3. Trigger direct browser download
    const url = window.URL.createObjectURL(csvBlob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `wishlist_subscribers_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Failed to export CSV:', err)
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  document.body.style.backgroundColor = '#A2F1DF'
  if (isAdmin.value) {
    fetchSubscribers()
  }
})

onUnmounted(() => {
  document.body.style.backgroundColor = ''
})

watch(isAdmin, (val) => {
  if (val) {
    fetchSubscribers()
  }
})
</script>

<style scoped>
.admin-wishlist-page {
  min-height: 100vh;
  background-color: #A2F1DF;
  color: #0a1c17;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
  overflow-x: hidden;
}

.admin-main {
  position: relative;
  padding: 8rem 1.5rem 5rem;
  min-height: calc(100vh - 80px);
}

.admin-glow {
  position: absolute;
  top: 3rem;
  left: 50%;
  width: min(840px, 92vw);
  height: 420px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.65), transparent 70%);
  filter: blur(55px);
  pointer-events: none;
}

.admin-container {
  position: relative;
  z-index: 1;
  max-width: 72rem;
  margin: 0 auto;
}

/* Hero Header */
.admin-hero {
  text-align: center;
  margin-bottom: 3rem;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  margin-bottom: 18px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 9999px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.04);
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #073933;
}

.admin-title {
  margin: 0 0 14px;
  font-size: clamp(2rem, 3.4vw, 3rem);
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1.15;
  color: #073933;
}

.admin-intro {
  margin: 0 auto 20px;
  max-width: 36rem;
  font-size: 13.5px;
  font-weight: 500;
  line-height: 1.6;
  color: #073933;
  opacity: 0.85;
}

.admin-nav-actions {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.nav-pill-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 18px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(7, 57, 51, 0.18);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #073933;
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(7, 57, 51, 0.04);
}

.nav-pill-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(7, 57, 51, 0.35);
  transform: translateY(-1px);
}

.nav-pill-btn-primary {
  background: #073933;
  color: #ffffff;
  border-color: #073933;
  box-shadow: 0 3px 10px rgba(7, 57, 51, 0.18);
}

.nav-pill-btn-primary:hover {
  background: #09473f;
  color: #ffffff;
}

/* Auth Card */
.admin-auth-card {
  max-width: 440px;
  margin: 2rem auto;
  padding: 36px 32px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(7, 57, 51, 0.18);
  border-radius: 1.5rem;
  box-shadow: 0 12px 36px rgba(7, 57, 51, 0.08);
  backdrop-filter: blur(16px);
  text-align: center;
}

.auth-card-icon {
  width: 52px;
  height: 52px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: rgba(7, 57, 51, 0.08);
  border: 1px solid rgba(7, 57, 51, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #073933;
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}

.auth-card-desc {
  font-size: 12px;
  color: #073933;
  opacity: 0.75;
  line-height: 1.5;
  margin-bottom: 24px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.auth-error-banner {
  padding: 10px 14px;
  border-radius: 8px;
  background: #fef2f2;
  border: 1px solid #fecdd3;
  color: #b91c1c;
  font-size: 11.5px;
  line-height: 1.4;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.field-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #073933;
  opacity: 0.8;
  margin-bottom: 6px;
}

.field-input {
  width: 100%;
  padding: 11px 16px;
  border-radius: 10px;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.2);
  color: #073933;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.field-input:focus {
  border-color: #073933;
  box-shadow: 0 0 0 3px rgba(7, 57, 51, 0.1);
}

.auth-submit-wrapper {
  margin-top: 6px;
}

.auth-submit-btn {
  width: 100%;
  padding: 12px 18px;
  border-radius: 12px;
  background: #073933;
  color: #ffffff;
  border: 1px solid #073933;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.2);
}

.auth-submit-btn:hover:not(:disabled) {
  background: #09473f;
  transform: translateY(-1px);
}

.auth-submit-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.metric-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(7, 57, 51, 0.14);
  border-radius: 1.25rem;
  padding: 22px 24px;
  box-shadow: 0 4px 18px rgba(7, 57, 51, 0.05);
  backdrop-filter: blur(12px);
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.metric-card:hover {
  border-color: rgba(7, 57, 51, 0.3);
  box-shadow: 0 8px 24px rgba(7, 57, 51, 0.08);
  transform: translateY(-2px);
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.metric-label {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #073933;
  opacity: 0.75;
}

.metric-icon {
  font-size: 18px;
}

.metric-value {
  font-size: 2.3rem;
  font-weight: 800;
  color: #073933;
  line-height: 1.1;
  margin-bottom: 4px;
}

.metric-subtext {
  font-size: 12px;
  color: #073933;
  opacity: 0.65;
}

.action-buttons-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.action-btn {
  flex: 1;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  transition: all 0.2s ease;
  cursor: pointer;
  text-align: center;
  border: none;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.copy-btn {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(7, 57, 51, 0.2);
  color: #073933;
  box-shadow: 0 2px 6px rgba(7, 57, 51, 0.04);
}

.copy-btn:hover:not(:disabled) {
  background: #ffffff;
  border-color: #073933;
}

.export-btn {
  background: #073933;
  border: 1px solid #073933;
  color: #ffffff;
  box-shadow: 0 3px 10px rgba(7, 57, 51, 0.18);
}

.export-btn:hover:not(:disabled) {
  background: #09473f;
}

/* Toolbar */
.toolbar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

@media (min-width: 640px) {
  .toolbar-wrapper {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.search-input-box {
  position: relative;
  width: 100%;
  max-width: 380px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #073933;
  opacity: 0.5;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 38px 10px 38px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(7, 57, 51, 0.2);
  color: #073933;
  font-size: 13.5px;
  outline: none;
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #073933;
  opacity: 0.45;
}

.search-input:focus {
  background: #ffffff;
  border-color: #073933;
  box-shadow: 0 0 0 3px rgba(7, 57, 51, 0.1);
}

.clear-search-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  color: #073933;
  opacity: 0.5;
  cursor: pointer;
  font-size: 12px;
}

.clear-search-btn:hover {
  opacity: 1;
}

.toolbar-right {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.leads-counter {
  font-size: 11.5px;
  font-weight: 600;
  color: #073933;
  opacity: 0.75;
  letter-spacing: 0.04em;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(7, 57, 51, 0.18);
  color: #073933;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: #ffffff;
  border-color: rgba(7, 57, 51, 0.35);
  transform: translateY(-1px);
}

.refresh-icon {
  font-size: 14px;
}

.refresh-text {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.1em;
}

/* State Cards */
.state-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.25rem;
  padding: 60px 24px;
  text-align: center;
  box-shadow: 0 4px 18px rgba(7, 57, 51, 0.05);
  backdrop-filter: blur(12px);
}

.spinner {
  width: 28px;
  height: 28px;
  margin: 0 auto 16px;
  border: 3px solid rgba(7, 57, 51, 0.15);
  border-top-color: #073933;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.state-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #073933;
  margin-bottom: 6px;
}

.state-desc {
  font-size: 12.5px;
  color: #073933;
  opacity: 0.7;
  max-width: 400px;
  margin: 0 auto;
}

/* Data Table Card */
.table-card {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.25rem;
  box-shadow: 0 6px 24px rgba(7, 57, 51, 0.06);
  backdrop-filter: blur(14px);
  overflow: hidden;
}

.leads-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.leads-table thead {
  background: rgba(7, 57, 51, 0.05);
  border-bottom: 1px solid rgba(7, 57, 51, 0.12);
}

.leads-table th {
  padding: 14px 18px;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #073933;
}

.th-index {
  width: 50px;
  text-align: center;
}

.table-row {
  transition: background-color 0.15s ease;
  border-bottom: 1px solid rgba(7, 57, 51, 0.07);
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: rgba(162, 241, 223, 0.28);
}

.leads-table td {
  padding: 13px 18px;
  vertical-align: middle;
  color: #073933;
  font-size: 13.5px;
}

.td-index {
  text-align: center;
  font-size: 12px;
  opacity: 0.55;
}

.email-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.email-text {
  font-weight: 600;
  color: #073933;
  font-size: 14px;
}

.copy-single-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  border: 1px solid rgba(7, 57, 51, 0.15);
  background: rgba(255, 255, 255, 0.7);
  color: #073933;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s ease;
}

.copy-single-btn:hover {
  background: #ffffff;
  border-color: #073933;
}

.td-date {
  font-size: 12px;
  opacity: 0.7;
}

.source-badge {
  display: inline-block;
  padding: 2.5px 8px;
  border-radius: 6px;
  background: rgba(7, 57, 51, 0.06);
  border: 1px solid rgba(7, 57, 51, 0.12);
  font-size: 11.5px;
  color: #073933;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 9999px;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(7, 57, 51, 0.06);
  border: 1px solid rgba(7, 57, 51, 0.15);
  color: #073933;
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  transition: all 0.15s ease;
}

.contact-link:hover {
  background: #073933;
  color: #ffffff;
  border-color: #073933;
}
</style>
