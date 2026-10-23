<template>
  <header class="landing-header" :class="{ 'scrolled': isScrolled }">
    <div class="header-container">
      <!-- Brand Logo -->
      <router-link to="/" class="brand-link">
        <img src="../../assets/logo/obrive-white-logo.svg" alt="Obrive" class="brand-logo" />
        <span class="brand-divider">/</span>
        <span class="brand-name">OBMIND<span class="brand-tm">TM</span></span>
      </router-link>

      <!-- Center Navigation Links -->
      <nav class="nav-menu">
        <a href="#overview" class="nav-link" @click.prevent="scrollTo('#overview')">Overview</a>
        <a href="#workflow" class="nav-link" @click.prevent="scrollTo('#workflow')">How It Works</a>
        <a href="#use-cases" class="nav-link" @click.prevent="scrollTo('#use-cases')">Explore</a>
        <a href="#about" class="nav-link" @click.prevent="scrollTo('#about')">Vision</a>
        <a href="#faq" class="nav-link" @click.prevent="scrollTo('#faq')">FAQ</a>
      </nav>

      <!-- Right Action Area -->
      <div class="header-actions">
        <!-- Auth Profile Pill / Sign In -->
        <div v-if="authStore.isAuthenticated.value" class="user-pill" @click="authStore.openProfileModal">
          <div class="avatar">{{ userInitials }}</div>
          <span class="user-name">{{ authStore.user.value?.full_name || 'Account' }}</span>
          <span v-if="authStore.isVerified.value" class="status-dot verified" title="Verified"></span>
          <span v-else class="status-dot unverified" title="Verification Pending"></span>
        </div>
        <button v-else class="btn-signin" @click="authStore.openAuthModal('login')">
          Sign In
        </button>

        <!-- External Obrive link -->
        <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="link-obrive">
          Explore Obrive <span class="arrow">↗</span>
        </a>

        <!-- Predict Now CTA to /console -->
        <router-link to="/console" class="btn-predict-header">
          Predict Now <span class="btn-arrow">→</span>
        </router-link>
      </div>

      <!-- Mobile Hamburger Button -->
      <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle menu">
        <span :class="['hamburger-line', { open: mobileMenuOpen }]"></span>
      </button>
    </div>

    <!-- Mobile Dropdown -->
    <div v-if="mobileMenuOpen" class="mobile-drawer">
      <a href="#overview" class="mobile-nav-link" @click="handleMobileNav('#overview')">Overview</a>
      <a href="#workflow" class="mobile-nav-link" @click="handleMobileNav('#workflow')">How It Works</a>
      <a href="#use-cases" class="mobile-nav-link" @click="handleMobileNav('#use-cases')">Explore</a>
      <a href="#about" class="mobile-nav-link" @click="handleMobileNav('#about')">Vision</a>
      <a href="#faq" class="mobile-nav-link" @click="handleMobileNav('#faq')">FAQ</a>
      <div class="mobile-actions">
        <router-link to="/console" class="btn-predict-mobile" @click="mobileMenuOpen = false">
          Predict Now →
        </router-link>
        <a href="https://obrive.com" target="_blank" class="mobile-obrive-link">
          Explore Obrive ↗
        </a>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import authStore from '../../store/auth'

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const userInitials = computed(() => {
  const name = authStore.user.value?.full_name || 'User'
  const parts = name.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const scrollTo = (hash) => {
  const target = document.querySelector(hash)
  if (target) {
    target.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleMobileNav = (hash) => {
  mobileMenuOpen.value = false
  scrollTo(hash)
}
</script>

<style scoped>
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  transition: all 0.3s ease;
  background: rgba(7, 11, 14, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.landing-header.scrolled {
  background: rgba(7, 11, 14, 0.92);
  border-bottom-color: rgba(0, 229, 163, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.header-container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #fff;
}

.brand-logo {
  height: 26px;
  width: auto;
  filter: drop-shadow(0 0 8px rgba(0, 229, 163, 0.3));
}

.brand-divider {
  color: rgba(255, 255, 255, 0.2);
  font-weight: 300;
}

.brand-name {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: 2px;
  color: #ffffff;
}

.brand-tm {
  font-size: 0.6rem;
  color: #00E5A3;
  margin-left: 2px;
  vertical-align: super;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-link {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.2s ease;
  position: relative;
}

.nav-link:hover {
  color: #00E5A3;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-pill:hover {
  border-color: #00E5A3;
  background: rgba(0, 229, 163, 0.08);
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #074139;
  color: #00E5A3;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 0.85rem;
  color: #e2e8f0;
  font-weight: 500;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-dot.verified {
  background: #00E5A3;
  box-shadow: 0 0 6px #00E5A3;
}

.status-dot.unverified {
  background: #f59e0b;
}

.btn-signin {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
  padding: 7px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-signin:hover {
  border-color: #00E5A3;
  color: #00E5A3;
  background: rgba(0, 229, 163, 0.06);
}

.link-obrive {
  color: #94a3b8;
  font-size: 0.85rem;
  text-decoration: none;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;
}

.link-obrive:hover {
  color: #ffffff;
}

.arrow {
  font-size: 0.8rem;
  opacity: 0.7;
}

.btn-predict-header {
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  color: #05080a;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 15px rgba(0, 229, 163, 0.25);
  transition: all 0.25s ease;
}

.btn-predict-header:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 229, 163, 0.4);
  color: #000;
}

.btn-arrow {
  transition: transform 0.2s ease;
}

.btn-predict-header:hover .btn-arrow {
  transform: translateX(3px);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}

.hamburger-line {
  display: block;
  width: 22px;
  height: 2px;
  background: #fff;
  position: relative;
  transition: all 0.3s ease;
}

.hamburger-line::before,
.hamburger-line::after {
  content: '';
  position: absolute;
  width: 22px;
  height: 2px;
  background: #fff;
  transition: all 0.3s ease;
}

.hamburger-line::before {
  top: -6px;
}

.hamburger-line::after {
  top: 6px;
}

.mobile-drawer {
  display: none;
}

@media (max-width: 900px) {
  .nav-menu,
  .link-obrive {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .mobile-drawer {
    display: flex;
    flex-direction: column;
    padding: 20px 24px;
    background: #070b0e;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    gap: 16px;
  }

  .mobile-nav-link {
    color: #cbd5e1;
    text-decoration: none;
    font-size: 1rem;
    padding: 8px 0;
  }

  .mobile-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .btn-predict-mobile {
    background: #00E5A3;
    color: #070b0e;
    padding: 10px;
    text-align: center;
    border-radius: 8px;
    font-weight: 700;
    text-decoration: none;
  }

  .mobile-obrive-link {
    color: #94a3b8;
    text-align: center;
    text-decoration: none;
    font-size: 0.9rem;
  }
}
</style>
