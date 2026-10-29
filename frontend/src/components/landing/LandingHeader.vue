<template>
  <header
    class="fixed top-0 left-0 right-0 z-[100] transition-all duration-300"
    :class="isScrolled ? 'bg-[#A2F1DF]/90 backdrop-blur-md border-b border-[#0a1c17]/10' : 'bg-transparent'"
  >
    <div class="container-main">
      <div class="flex items-center justify-between h-20">
        <!-- Logo (Only Icon) -->
        <router-link to="/" class="logo" aria-label="Obrive Brain Home">
          <img src="/obrive-logo.svg" alt="Obrive" class="logo-img" width="70" height="50" />
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

            <AnimatedButton
              v-if="route.path !== '/console'"
              to="/console"
              variant="primary"
              size="sm"
              :iconSize="12"
              arrowColor="default"
            >
              Console
            </AnimatedButton>
          </template>

          <AnimatedButton
            v-else
            type="button"
            @click="handleSignIn"
            variant="primary"
            size="sm"
            :iconSize="12"
            arrowColor="default"
          >
            Sign In
          </AnimatedButton>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authStore from '../../store/auth'
import AnimatedButton from '../common/AnimatedButton.vue'

const emit = defineEmits(['open-auth'])
const router = useRouter()
const route = useRoute()
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
  width: 70px;
  height: 50px;
  object-fit: contain;
}

.logo-divider {
  color: #073933;
  font-size: 1.45rem;
  font-weight: 500;
  line-height: 1;
  opacity: 0.85;
}

.logo-text {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 1.45rem;
  letter-spacing: 0.08em;
  color: #073933;
  line-height: 1;
}

.nav-signin-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.4rem;
  background-color: #073933;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border-radius: 0.75rem;
  border: 1px solid #073933;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(7, 57, 51, 0.2);
}

.nav-signin-btn:hover {
  background-color: #042823;
  border-color: #042823;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(7, 57, 51, 0.3);
}

.nav-signin-btn:active {
  transform: translateY(0);
}

.user-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px 4px 5px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 28, 23, 0.15);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.user-pill:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(10, 28, 23, 0.3);
  transform: translateY(-1px);
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0a1c17;
  color: #ffffff;
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
  color: #0a1c17;
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
  background: #f59e0b;
}

.nav-console-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.35rem;
  background-color: #073933;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border-radius: 0.75rem;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(7, 57, 51, 0.2);
}

.nav-console-btn:hover {
  background-color: #042823;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(7, 57, 51, 0.3);
}

.nav-console-btn:active {
  transform: translateY(0);
}
</style>
