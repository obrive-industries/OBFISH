<template>
  <router-view />
  <!-- Global Modals -->
  <AuthModal />
  <UserProfileModal />
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import AuthModal from './components/AuthModal.vue'
import UserProfileModal from './components/UserProfileModal.vue'
import authStore from './store/auth'
import authApi from './api/auth'

const handleLogoutEvent = () => {
  authStore.clearSession()
}

onMounted(async () => {
  window.addEventListener('obmind-auth-logout', handleLogoutEvent)

  // Sync profile if token exists
  if (authStore.state.accessToken) {
    try {
      const res = await authApi.getMe()
      if (res?.user) {
        authStore.updateUser(res.user)
      }
    } catch (e) {
      // If token expired, interceptor will try refresh or trigger logout
      console.warn('Initial auth sync:', e.message)
    }
  }
})

onUnmounted(() => {
  window.removeEventListener('obmind-auth-logout', handleLogoutEvent)
})
</script>

<style>
/* Obrive Design Tokens */
:root {
  --obrive-obsidian: #070b0e;
  --obrive-surface: #0c1216;
  --obrive-card: rgba(12, 18, 22, 0.75);
  --obrive-primary: #074139;
  --obrive-primary-dark: #052e28;
  --obrive-primary-light: #0d5c52;
  --obrive-emerald: #00E5A3;
  --obrive-accent: #00E5A3;
  --obrive-accent-light: #a2f1df;
  --obrive-accent-gradient: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  --obrive-bg: #070b0e;
  --obrive-border: rgba(255, 255, 255, 0.08);
  --obrive-border-focus: rgba(0, 229, 163, 0.4);
  --obrive-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 229, 163, 0.25) transparent;
}

body {
  font-family: 'Space Grotesk', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #070b0e;
  color: #ffffff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  font-family: 'Space Grotesk', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #ffffff;
  background-color: var(--obrive-bg);
  min-height: 100vh;
}

/* Obrive Slim-line minimalist custom scrollbar everywhere */
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 229, 163, 0.25);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 229, 163, 0.5);
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}
</style>
