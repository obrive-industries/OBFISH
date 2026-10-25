<template>
  <header
    class="fixed top-0 left-0 right-0 z-[100] transition-all duration-300"
    :class="isScrolled ? 'bg-black/85 backdrop-blur-md border-b border-white/[0.08]' : 'bg-transparent'"
  >
    <div class="container-main">
      <div class="flex items-center justify-between h-20">
        <!-- Logo -->
        <router-link to="/" class="logo" aria-label="Brain Home">
          <img src="/obrive-white-logo.svg" alt="Obrive" class="logo-img" />
          <span class="logo-divider">/</span>
          <span class="logo-text">BRAIN</span>
        </router-link>

        <!-- Right Actions: Profile Pill when Logged In, Sign In when Logged Out -->
        <div class="flex items-center gap-3">
          <template v-if="authStore.isAuthenticated.value">
            <div
              class="user-pill"
              @click="authStore.openProfileModal"
              title="Account & Settings"
              role="button"
              tabindex="0"
            >
              <div class="avatar">{{ userInitials }}</div>
              <span class="user-name">{{ authStore.user.value?.full_name || 'My Account' }}</span>
              <span v-if="authStore.isVerified.value" class="status-dot verified" title="Email Verified"></span>
              <span v-else class="status-dot unverified" title="Verification Pending"></span>
            </div>

            <router-link
              to="/console"
              class="nav-console-btn"
            >
              Console →
            </router-link>
          </template>

          <button
            v-else
            type="button"
            @click="handleSignIn"
            class="nav-signin-btn"
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authStore from '../../store/auth'

const emit = defineEmits(['open-auth'])
const router = useRouter()
const isScrolled = ref(false)

const userInitials = computed(() => {
  const name = authStore.user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const handleSignIn = () => {
  if (authStore.isAuthenticated.value) {
    router.push('/console')
  } else {
    emit('open-auth')
  }
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.container-main {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container-main {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container-main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.85;
}

.logo-img {
  height: 24px;
  width: auto;
  object-fit: contain;
}

.logo-divider {
  color: rgba(255, 255, 255, 0.25);
  font-size: 1.15rem;
  font-weight: 300;
  line-height: 1;
}

.logo-text {
  font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: 0.08em;
  color: #ffffff;
  line-height: 1;
}

.nav-signin-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.25rem;
  background-color: #ffffff;
  color: #000000;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.nav-signin-btn:hover {
  background-color: #e5e7eb;
  transform: translateY(-1px);
}

.nav-signin-btn:active {
  transform: translateY(0);
}

.user-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px 4px 5px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.user-pill:hover {
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(255, 255, 255, 0.35);
  transform: translateY(-1px);
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ffffff;
  color: #000000;
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-family: 'Space Grotesk', 'Inter', monospace;
  font-size: 0.8rem;
  font-weight: 600;
  color: #ffffff;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.verified {
  background: #00e5a3;
  box-shadow: 0 0 6px rgba(0, 229, 163, 0.6);
}

.status-dot.unverified {
  background: #ff4500;
}

.nav-console-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.15rem;
  background-color: #ffffff;
  color: #000000;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.nav-console-btn:hover {
  background-color: #e5e7eb;
  transform: translateY(-1px);
}

.nav-console-btn:active {
  transform: translateY(0);
}
</style>
