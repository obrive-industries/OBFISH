<template>
  <header class="header-outer" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-pill">
      <!-- Brand Logo -->
      <router-link to="/" class="brand-link" aria-label="ObMind Home">
        <img
          src="../../assets/icons/obrive-logo.svg"
          alt="Obrive"
          class="brand-logo"
        />
        <span class="brand-sep">/</span>
        <span class="brand-name font-microgramma">OBMIND</span>
      </router-link>

      <!-- Center Navigation Links -->
      <nav class="nav-links">
        <a href="#overview" class="nav-item" @click.prevent="scrollTo('#overview')">Overview</a>
        <a href="#uncertainty" class="nav-item" @click.prevent="scrollTo('#uncertainty')">Decision Dynamics</a>
        <a href="#workflow" class="nav-item" @click.prevent="scrollTo('#workflow')">How It Works</a>
        <a href="#use-cases" class="nav-item" @click.prevent="scrollTo('#use-cases')">Explore</a>
        <a href="#about" class="nav-item" @click.prevent="scrollTo('#about')">Vision</a>
        <a href="#faq" class="nav-item" @click.prevent="scrollTo('#faq')">FAQ</a>
      </nav>

      <!-- Right Action Area -->
      <div class="header-actions">
        <!-- Auth Profile Pill / Sign In -->
        <div
          v-if="authStore.isAuthenticated.value"
          class="user-pill"
          @click="authStore.openProfileModal"
          title="Account Profile"
        >
          <div class="avatar">{{ userInitials }}</div>
          <span class="user-name">{{ authStore.user.value?.full_name || 'Account' }}</span>
          <span
            class="status-dot"
            :class="authStore.isVerified.value ? 'verified' : 'unverified'"
            :title="authStore.isVerified.value ? 'Verified' : 'Verification Pending'"
          ></span>
        </div>
        <button
          v-else
          class="btn-signin"
          @click="authStore.openAuthModal('login')"
        >
          Sign In
        </button>

        <!-- External Obrive link -->
        <a
          href="https://obrive.com"
          target="_blank"
          rel="noopener noreferrer"
          class="link-obrive"
        >
          Explore Obrive <span class="arrow-ext">↗</span>
        </a>

        <!-- Predict Now CTA using Obrive AnimatedButton -->
        <AnimatedButton
          to="/console"
          variant="primary"
          size="sm"
          :iconSize="14"
        >
          Predict Now
        </AnimatedButton>
      </div>

      <!-- Mobile Hamburger Button -->
      <button
        class="mobile-toggle"
        @click="mobileMenuOpen = !mobileMenuOpen"
        aria-label="Toggle menu"
      >
        <span class="hamburger-bar" :class="{ open: mobileMenuOpen }"></span>
      </button>
    </div>

    <!-- Mobile Drawer -->
    <transition name="drawer-slide">
      <div v-if="mobileMenuOpen" class="mobile-drawer">
        <nav class="mobile-nav">
          <a href="#overview" class="mobile-item" @click="handleMobileNav('#overview')">Overview</a>
          <a href="#uncertainty" class="mobile-item" @click="handleMobileNav('#uncertainty')">Decision Dynamics</a>
          <a href="#workflow" class="mobile-item" @click="handleMobileNav('#workflow')">How It Works</a>
          <a href="#use-cases" class="mobile-item" @click="handleMobileNav('#use-cases')">Explore</a>
          <a href="#about" class="mobile-item" @click="handleMobileNav('#about')">Vision</a>
          <a href="#faq" class="mobile-item" @click="handleMobileNav('#faq')">FAQ</a>
        </nav>

        <div class="mobile-footer">
          <AnimatedButton
            to="/console"
            variant="primary"
            size="default"
            class="w-full justify-center"
            @click="mobileMenuOpen = false"
          >
            Predict Now
          </AnimatedButton>
          <div class="mobile-secondary-row">
            <button
              v-if="!authStore.isAuthenticated.value"
              class="mobile-signin"
              @click="authStore.openAuthModal('login'); mobileMenuOpen = false"
            >
              Sign In
            </button>
            <a
              href="https://obrive.com"
              target="_blank"
              rel="noopener noreferrer"
              class="mobile-ext-link"
            >
              Explore Obrive ↗
            </a>
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import authStore from '../../store/auth'
import AnimatedButton from '../common/AnimatedButton.vue'

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
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
    const headerOffset = 90
    const elementPosition = target.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
}

const handleMobileNav = (hash) => {
  mobileMenuOpen.value = false
  setTimeout(() => scrollTo(hash), 150)
}
</script>

<style scoped>
.header-outer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 16px 20px 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.header-pill {
  pointer-events: auto;
  max-width: 1152px; /* max-w-6xl */
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px 0 24px;
  background-color: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(7, 65, 57, 0.16);
  border-radius: 16px;
  box-shadow: 0 4px 20px -2px rgba(7, 65, 57, 0.06);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.header-outer.is-scrolled .header-pill {
  background-color: rgba(255, 255, 255, 0.96);
  border-color: rgba(7, 65, 57, 0.24);
  box-shadow: 0 10px 30px -4px rgba(7, 65, 57, 0.12);
  height: 60px;
}

/* Brand Logo */
.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #074139;
  flex-shrink: 0;
}

.brand-logo {
  height: 28px;
  width: auto;
  display: block;
}

.brand-sep {
  color: rgba(7, 65, 57, 0.3);
  font-weight: 300;
  font-size: 1.1rem;
}

.brand-name {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #074139;
}

/* Nav Menu */
.nav-links {
  display: flex;
  align-items: center;
  gap: 22px;
}

.nav-item {
  color: #074139;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-decoration: none;
  padding: 6px 4px;
  position: relative;
  transition: color 0.2s ease, font-weight 0.2s ease;
}

.nav-item:hover {
  color: #0d5c52;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: #074139;
  transition: all 0.25s ease;
  transform: translateX(-50%);
}

.nav-item:hover::after {
  width: 100%;
}

/* Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.btn-signin {
  background: transparent;
  border: 1px solid rgba(7, 65, 57, 0.25);
  color: #074139;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-signin:hover {
  background-color: rgba(7, 65, 57, 0.08);
  border-color: #074139;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  background: rgba(7, 65, 57, 0.06);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-pill:hover {
  background: rgba(7, 65, 57, 0.12);
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #074139;
  color: #caede5;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 11px;
  font-weight: 600;
  color: #074139;
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.verified {
  background: #00E5A3;
  box-shadow: 0 0 6px #00E5A3;
}

.status-dot.unverified {
  background: #ffab00;
}

.link-obrive {
  color: rgba(7, 65, 57, 0.75);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 8px;
  transition: color 0.2s ease;
}

.link-obrive:hover {
  color: #074139;
}

.arrow-ext {
  font-size: 12px;
  transition: transform 0.2s ease;
}

.link-obrive:hover .arrow-ext {
  transform: translate(2px, -2px);
}

/* Mobile Toggle */
.mobile-toggle {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #074139;
}

.hamburger-bar {
  display: block;
  width: 20px;
  height: 2px;
  background-color: #074139;
  position: relative;
  transition: all 0.3s ease;
}

.hamburger-bar::before,
.hamburger-bar::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 2px;
  background-color: #074139;
  transition: all 0.3s ease;
}

.hamburger-bar::before {
  top: -6px;
}

.hamburger-bar::after {
  top: 6px;
}

.hamburger-bar.open {
  background-color: transparent;
}

.hamburger-bar.open::before {
  transform: translateY(6px) rotate(45deg);
}

.hamburger-bar.open::after {
  transform: translateY(-6px) rotate(-45deg);
}

/* Mobile Drawer */
.mobile-drawer {
  pointer-events: auto;
  max-width: 1152px;
  margin: 10px auto 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 16px 36px -4px rgba(7, 65, 57, 0.16);
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.mobile-item {
  color: #074139;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.mobile-item:hover {
  background: rgba(7, 65, 57, 0.06);
}

.mobile-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.mobile-secondary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-signin {
  background: none;
  border: none;
  color: #074139;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-transform: uppercase;
}

.mobile-ext-link {
  color: rgba(7, 65, 57, 0.7);
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Breakpoints */
@media (max-width: 960px) {
  .nav-links {
    display: none;
  }

  .link-obrive {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }
}

@media (max-width: 640px) {
  .header-outer {
    padding: 8px 12px 0;
  }

  .header-pill {
    height: 56px;
    padding: 0 14px;
    border-radius: 12px;
  }

  .btn-signin {
    display: none;
  }
}
</style>
