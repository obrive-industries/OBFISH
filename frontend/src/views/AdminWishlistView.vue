<template>
  <div class="admin-wishlist-page min-h-screen bg-black text-white px-4 sm:px-6 py-10 relative overflow-hidden font-sans">
    <!-- Ambient Sci-Fi Glows -->
    <div class="glow-orb orb-top" aria-hidden="true"></div>
    <div class="glow-orb orb-bottom" aria-hidden="true"></div>

    <div class="max-w-6xl mx-auto relative z-10">
      <!-- Top Navigation & Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 pb-6 border-b border-white/10">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-mono uppercase tracking-wider text-gray-400 mb-2">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <span>Admin Portal</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            Wishlist & Waitlist Leads
          </h1>
          <p class="text-sm text-gray-400 mt-1">
            Real-time prospective customer emails submitted via the landing page.
          </p>
        </div>

        <div class="flex items-center gap-3">
          <router-link
            to="/"
            class="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-gray-300 hover:text-white transition-colors"
          >
            ← Back to Home
          </router-link>
          <router-link
            to="/console"
            class="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-gray-300 hover:text-white transition-colors"
          >
            Console
          </router-link>
        </div>
      </div>

      <!-- State 1: Admin Login Card (If unauthenticated or not admin) -->
      <div v-if="!isAdmin" class="max-w-md mx-auto my-12 p-8 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl shadow-2xl">
        <div class="text-center mb-6">
          <div class="w-12 h-12 mx-auto rounded-full bg-white/10 flex items-center justify-center text-xl mb-3">
            🔒
          </div>
          <h2 class="text-xl font-bold text-white">Administrator Access Required</h2>
          <p class="text-xs text-gray-400 mt-1">
            Sign in with your admin credentials to view collected subscriber emails.
          </p>
        </div>

        <form @submit.prevent="handleAdminLogin" class="flex flex-col gap-4">
          <div v-if="loginError" class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-xs text-red-400">
            {{ loginError }}
          </div>

          <div>
            <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Admin Email</label>
            <input
              v-model="loginForm.email"
              type="email"
              placeholder="ai@obrive.com"
              required
              class="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/15 text-white text-sm focus:outline-none focus:border-white transition-colors"
              :disabled="loggingIn"
            />
          </div>

          <div>
            <label class="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Password</label>
            <input
              v-model="loginForm.password"
              type="password"
              placeholder="••••••••"
              required
              class="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/15 text-white text-sm focus:outline-none focus:border-white transition-colors"
              :disabled="loggingIn"
            />
          </div>

          <button
            type="submit"
            class="w-full py-2.5 mt-2 rounded-lg bg-white text-black font-semibold text-sm hover:bg-gray-200 transition-colors disabled:opacity-50"
            :disabled="loggingIn"
          >
            {{ loggingIn ? 'Authenticating...' : 'Sign In as Admin →' }}
          </button>
        </form>
      </div>

      <!-- State 2: Authenticated Admin Dashboard -->
      <div v-else>
        <!-- Metric Cards & Actions -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div class="p-5 rounded-xl bg-white/[0.03] border border-white/10">
            <span class="text-xs font-mono uppercase tracking-wider text-gray-400">Total Subscribers</span>
            <div class="text-3xl font-bold text-white mt-2">{{ subscribers.length }}</div>
          </div>

          <div class="p-5 rounded-xl bg-white/[0.03] border border-white/10">
            <span class="text-xs font-mono uppercase tracking-wider text-gray-400">Unique Domains</span>
            <div class="text-3xl font-bold text-cyan-400 mt-2">{{ uniqueDomainsCount }}</div>
          </div>

          <div class="p-5 rounded-xl bg-white/[0.03] border border-white/10 flex flex-col justify-between">
            <span class="text-xs font-mono uppercase tracking-wider text-gray-400">Quick Actions</span>
            <div class="flex items-center gap-2 mt-2">
              <button
                @click="copyAllEmails"
                class="flex-1 px-3 py-2 rounded-lg bg-white/10 hover:bg-white/15 border border-white/10 text-xs font-medium text-white transition-all text-center"
              >
                {{ copied ? '✓ Copied!' : '📋 Copy All' }}
              </button>
              <button
                @click="exportCsv"
                class="flex-1 px-3 py-2 rounded-lg bg-white text-black hover:bg-gray-200 text-xs font-semibold transition-all text-center"
              >
                📥 Export CSV
              </button>
            </div>
          </div>
        </div>

        <!-- Filter & Search Toolbar -->
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
          <div class="relative w-full sm:w-80">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by email or domain..."
              class="w-full px-4 py-2 pl-9 rounded-lg bg-white/5 border border-white/10 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-white transition-colors"
            />
            <span class="absolute left-3 top-2.5 text-gray-500 text-sm">🔍</span>
          </div>

          <button
            @click="fetchSubscribers"
            class="self-end sm:self-auto px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-gray-300 hover:text-white transition-colors flex items-center gap-2"
          >
            <span>↻</span> Refresh List
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-16 text-gray-400 text-sm">
          <div class="inline-block animate-spin h-6 w-6 border-2 border-white/30 border-t-white rounded-full mb-3"></div>
          <div>Loading wishlist submissions...</div>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredSubscribers.length === 0" class="text-center py-16 rounded-xl bg-white/[0.02] border border-white/10">
          <div class="text-3xl mb-2">📭</div>
          <h3 class="text-base font-semibold text-white">No submissions found</h3>
          <p class="text-xs text-gray-500 mt-1 max-w-sm mx-auto">
            {{ searchQuery ? 'No subscriber emails matched your search query.' : 'New submissions from the landing page will automatically appear here.' }}
          </p>
        </div>

        <!-- Data Table -->
        <div v-else class="rounded-xl overflow-hidden border border-white/10 bg-white/[0.02] shadow-2xl">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-white/5 border-b border-white/10 text-xs font-mono uppercase tracking-wider text-gray-400">
                <tr>
                  <th class="py-3 px-4 w-16 text-center">#</th>
                  <th class="py-3 px-4">Email Address</th>
                  <th class="py-3 px-4">Signed Up (UTC)</th>
                  <th class="py-3 px-4">Source</th>
                  <th class="py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr
                  v-for="(sub, idx) in filteredSubscribers"
                  :key="sub.id || idx"
                  class="hover:bg-white/[0.04] transition-colors"
                >
                  <td class="py-3.5 px-4 text-center font-mono text-xs text-gray-500">
                    {{ idx + 1 }}
                  </td>
                  <td class="py-3.5 px-4 font-medium text-white select-all">
                    {{ sub.email }}
                  </td>
                  <td class="py-3.5 px-4 text-xs font-mono text-gray-400">
                    {{ formatDate(sub.created_at) }}
                  </td>
                  <td class="py-3.5 px-4 text-xs">
                    <span class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-gray-300 font-mono">
                      {{ sub.source || 'landing_hero' }}
                    </span>
                  </td>
                  <td class="py-3.5 px-4 text-xs">
                    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[11px] font-medium">
                      <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                      {{ sub.status || 'active' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import authStore from '../store/auth'
import wishlistApi from '../api/wishlist'

const subscribers = ref([])
const loading = ref(false)
const copied = ref(false)
const searchQuery = ref('')

const loggingIn = ref(false)
const loginError = ref('')
const loginForm = reactive({
  email: '',
  password: ''
})

const isAdmin = computed(() => {
  return authStore.state.isAuthenticated && authStore.user.value?.role === 'admin'
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
    const res = await authStore.login(loginForm.email, loginForm.password)
    if (res.success) {
      if (authStore.user.value?.role !== 'admin') {
        loginError.value = 'Access denied: This account does not have administrator privileges.'
        return
      }
      await fetchSubscribers()
    } else {
      loginError.value = res.error || 'Authentication failed.'
    }
  } catch (err) {
    loginError.value = err.response?.data?.error || 'Failed to sign in.'
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

const exportCsv = async () => {
  try {
    const res = await wishlistApi.exportCsv()
    const blob = new Blob([res.data], { type: 'text/csv;charset=utf-8;' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `wishlist_subscribers_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Failed to export CSV:', err)
  }
}

onMounted(() => {
  if (isAdmin.value) {
    fetchSubscribers()
  }
})
</script>

<style scoped>
.admin-wishlist-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(100px);
  z-index: 1;
}

.orb-top {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 70%);
  top: -100px;
  left: 20%;
}

.orb-bottom {
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(234, 160, 40, 0.1) 0%, transparent 70%);
  bottom: -150px;
  right: 15%;
}
</style>
