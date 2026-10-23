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
  --obrive-primary: #074139;
  --obrive-primary-dark: #052e28;
  --obrive-primary-light: #0d5c52;
  --obrive-accent: #a2f1df;
  --obrive-accent-light: #caede5;
  --obrive-accent-gradient: linear-gradient(135deg, #a2f1df 0%, #34d399 50%, #059669 100%);
  --obrive-bg: #A2F1DF;
  --obrive-surface: #FFFFFF;
  --obrive-border: rgba(7, 65, 57, 0.18);
  --obrive-border-focus: rgba(7, 65, 57, 0.35);
  --obrive-shadow: 0 4px 20px -2px rgba(7, 65, 57, 0.08);
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(7, 57, 51, 0.25) transparent;
}

body {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #A2F1DF;
  color: #074139;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  font-family: 'Michroma', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #074139;
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
  background-color: rgba(7, 57, 51, 0.25);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(7, 57, 51, 0.5);
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}
</style>
