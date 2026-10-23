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
/* Microgramma Bold - Official Obrive Display Font */
@font-face {
  font-family: 'Microgramma';
  src: url('./assets/fonts/microgramma-bold.otf') format('opentype');
  font-weight: 400 900;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Microgramma Bold';
  src: url('./assets/fonts/microgramma-bold.otf') format('opentype');
  font-weight: 400 900;
  font-style: normal;
  font-display: swap;
}

/* Obrive Design Tokens */
:root {
  --obrive-primary: #074139;
  --obrive-primary-dark: #052e28;
  --obrive-primary-light: #0d5c52;
  --obrive-accent: #a2f1df;
  --obrive-accent-light: #caede5;
  --obrive-accent-gradient: linear-gradient(
    to right,
    #caede5,
    #beeee3,
    #b2f0e1,
    #a5f1df,
    #98f2dd
  );
  --obrive-obsidian: #070b0e;
  --obrive-surface: #0c1216;
  --obrive-card: rgba(12, 18, 22, 0.75);
  --obrive-emerald: #00E5A3;
  --obrive-border: rgba(7, 65, 57, 0.18);
  --obrive-border-focus: rgba(7, 65, 57, 0.5);
  --obrive-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08);
}

/* Global Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(7, 65, 57, 0.25) transparent;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #ffffff;
  color: #074139;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

/* Obrive Typography Classes */
.font-microgramma {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-weight: 800;
  letter-spacing: 0;
}

.font-michroma {
  font-family: 'Michroma', sans-serif !important;
}

/* Obrive Gradients */
.bg-gradient-accent {
  background: var(--obrive-accent-gradient);
}

/* Obrive Signature Hover Cell Effect */
.obrive-cell {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 0.75rem;
  transition: color 0.4s ease, border-color 0.4s ease;
  z-index: 1;
}

.obrive-cell::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: #074139;
  transform: scaleY(0);
  transform-origin: center;
  transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
  z-index: -1;
}

.obrive-cell:hover::before {
  transform: scaleY(1);
}

.obrive-cell:hover {
  color: #ffffff !important;
}

/* Obrive Button with Sliding Icons */
.btn-animated {
  display: inline-flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-decoration: none;
  cursor: pointer;
  border: none;
  outline: none;
}

.btn-animated__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.75s cubic-bezier(0.19, 1, 0.22, 1);
}

.btn-animated__icon.--1 {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translate(-250%) translate(-2rem) translateY(-50%);
  transition-delay: 0s;
}

.btn-animated:hover .btn-animated__icon.--1 {
  transform: translate(-0.35rem) translateY(-50%);
  transition-delay: 0.2s;
}

.btn-animated__icon.--2 {
  position: relative;
  transform: translate(0);
  transition-delay: 0.2s;
  margin-left: 8px;
}

.btn-animated:hover .btn-animated__icon.--2 {
  transform: translate(100%) translate(2rem);
  transition-delay: 0s;
}

.btn-animated__label {
  display: inline-block;
  transform: translate(0);
  transition: transform 0.85s cubic-bezier(0.19, 1, 0.22, 1);
}

.btn-animated:hover .btn-animated__label {
  transform: translate(1.35rem);
}

/* Obrive Slim Minimalist Scrollbar */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(7, 65, 57, 0.25);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(7, 65, 57, 0.5);
}

/* Global button reset */
button {
  font-family: inherit;
}
</style>
