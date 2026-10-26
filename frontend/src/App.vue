<template>
  <router-view />
  <!-- Global Modals -->
  <AuthModal />
  <UserProfileModal />
  <PricingModal />
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import AuthModal from './components/AuthModal.vue'
import UserProfileModal from './components/UserProfileModal.vue'
import PricingModal from './components/PricingModal.vue'
import authStore from './store/auth'
import authApi from './api/auth'
import billingStore from './store/billing'

const handleLogoutEvent = () => {
  authStore.clearSession()
}

const handlePlanRequired = () => {
  billingStore.openPricing({ resume: false })
}

onMounted(async () => {
  window.addEventListener('brain-auth-logout', handleLogoutEvent)
  window.addEventListener('obmind-auth-logout', handleLogoutEvent)
  window.addEventListener('brain-plan-required', handlePlanRequired)

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
    billingStore.refresh()
  }
})

onUnmounted(() => {
  window.removeEventListener('brain-auth-logout', handleLogoutEvent)
  window.removeEventListener('obmind-auth-logout', handleLogoutEvent)
  window.removeEventListener('brain-plan-required', handlePlanRequired)
})
</script>

<style>
/* Microgramma Bold & Caveat - Official Display Fonts */
@font-face {
  font-family: 'microgrammaBold';
  src: url('/fonts/microgramma-bold.otf') format('opentype'),
       url('./assets/fonts/microgramma-bold.otf') format('opentype');
  font-weight: 400 900;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: 'Microgramma';
  src: url('/fonts/microgramma-bold.otf') format('opentype'),
       url('./assets/fonts/microgramma-bold.otf') format('opentype');
  font-weight: 400 900;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: 'Microgramma Bold';
  src: url('/fonts/microgramma-bold.otf') format('opentype'),
       url('./assets/fonts/microgramma-bold.otf') format('opentype');
  font-weight: 400 900;
  font-style: normal;
  font-display: block;
}

@font-face {
  font-family: 'Caveat';
  src: url('/fonts/caveat.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: block;
}

/* MiroFish & Obrive Design Tokens */
:root {
  --color-black: #000000;
  --color-white: #ffffff;
  --color-orange: #073933;
  --color-orange-hover: #074139;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;

  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display: 'Microgramma', 'Microgramma Bold', sans-serif;
  --font-michroma: 'Michroma', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Mono', monospace;

  /* Obrive official brand design tokens (matched with /home/yash/Obrive/Obrive) */
  --obrive-primary: #073933;
  --obrive-primary-teal: #074139;
  --obrive-primary-dark: #042823;
  --obrive-accent: #a2f1df;
  --obrive-accent-light: #caede5;
  --obrive-accent-gradient: linear-gradient(to right, #caede5, #beeee3, #b2f0e1, #a5f1df, #98f2dd);
  --obrive-text-dark: #073933;
  --obrive-text-body: #000000;
  --obrive-text-muted: #000000;
  --obrive-text-subtle: #2d554c;
  --obrive-border: rgba(7, 57, 51, 0.15);
  --obrive-border-focus: rgba(7, 57, 51, 0.4);
  --obrive-shadow: 0 10px 30px -5px rgba(7, 57, 51, 0.12);
}

/* Global Reset */
* {
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(7, 57, 51, 0.22) transparent;
}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(7, 57, 51, 0.22);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(7, 57, 51, 0.45);
}

body {
  font-family: var(--font-sans);
  background-color: #A2F1DF;
  color: var(--obrive-text-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

/* Typography Classes */
.font-microgramma {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  letter-spacing: -0.01em;
}

.font-michroma {
  font-family: 'Michroma', sans-serif !important;
  letter-spacing: 0.04em;
}

.font-mono {
  font-family: var(--font-mono) !important;
}

/* Obrive Cell Effect (Adapted to MiroFish aesthetic) */
.obrive-cell {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 0.75rem;
  transition: all 0.25s ease;
  z-index: 1;
}

.obrive-cell:hover {
  border-color: rgba(255, 255, 255, 0.35);
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
