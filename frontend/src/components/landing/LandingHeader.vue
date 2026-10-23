<template>
  <header class="header-outer" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-pill">
      <!-- Brand Logo -->
      <router-link to="/" class="brand-link" aria-label="Brain Home">
        <img
          src="../../assets/icons/obrive-logo.svg"
          alt="Obrive"
          class="brand-logo"
        />
        <span class="brand-divider"></span>
        <div class="brand-text-lockup font-microgramma">
          <span class="brand-name">BRAIN</span>
          <span class="brand-badge">AI</span>
        </div>
      </router-link>

      <!-- Center Navigation Links -->
      <nav class="nav-links">
        <a href="#overview" class="nav-item" @click.prevent="scrollTo('#overview')">Overview</a>
        <a href="#uncertainty" class="nav-item" @click.prevent="scrollTo('#uncertainty')">Dynamics</a>
        <a href="#workflow" class="nav-item" @click.prevent="scrollTo('#workflow')">Workflow</a>
        <a href="#use-cases" class="nav-item" @click.prevent="scrollTo('#use-cases')">Use Cases</a>
        <a href="#about" class="nav-item" @click.prevent="scrollTo('#about')">Vision</a>
        <a href="#faq" class="nav-item" @click.prevent="scrollTo('#faq')">FAQ</a>
      </nav>

      <!-- Right Action Area -->
      <div class="header-actions">
        <!-- External Obrive link (hidden on narrower desktop viewports) -->
        <a
          href="https://obrive.com"
          target="_blank"
          rel="noopener noreferrer"
          class="link-obrive font-microgramma"
          title="Visit Obrive Industries"
        >
          <span>Obrive</span>
          <span class="arrow-ext">↗</span>
        </a>

        <!-- Console Link (when logged in) -->
        <router-link
          v-if="authStore.isAuthenticated.value"
          to="/console"
          class="header-console-btn font-microgramma"
          title="Open Console"
        >
          Console
        </router-link>

        <!-- Auth Profile Pill (when logged in) -->
        <div
          v-if="authStore.isAuthenticated.value"
          class="user-pill font-microgramma"
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
        :aria-expanded="mobileMenuOpen"
        aria-label="Toggle navigation menu"
      >
        <span class="hamburger-bar" :class="{ open: mobileMenuOpen }"></span>
      </button>
    </div>

    <!-- Mobile Backdrop Overlay -->
    <transition name="fade">
      <div
        v-if="mobileMenuOpen"
        class="mobile-backdrop"
        @click="mobileMenuOpen = false"
      ></div>
    </transition>

    <!-- Mobile Drawer -->
    <transition name="drawer-slide">
      <div v-if="mobileMenuOpen" class="mobile-drawer">
        <div class="mobile-drawer-header">
          <div class="drawer-brand font-microgramma">
            <span>BRAIN</span>
            <span class="brand-badge">AI</span>
          </div>
          <button
            class="drawer-close-btn"
            @click="mobileMenuOpen = false"
            aria-label="Close menu"
          >
            ✕
          </button>
        </div>

        <nav class="mobile-nav">
          <a href="#overview" class="mobile-item" @click="handleMobileNav('#overview')">
            <span>Overview</span>
            <span class="mobile-item-arrow">→</span>
          </a>
          <a href="#uncertainty" class="mobile-item" @click="handleMobileNav('#uncertainty')">
            <span>Decision Dynamics</span>
            <span class="mobile-item-arrow">→</span>
          </a>
          <a href="#workflow" class="mobile-item" @click="handleMobileNav('#workflow')">
            <span>How It Works</span>
            <span class="mobile-item-arrow">→</span>
          </a>
          <a href="#use-cases" class="mobile-item" @click="handleMobileNav('#use-cases')">
            <span>Use Cases</span>
            <span class="mobile-item-arrow">→</span>
          </a>
          <a href="#about" class="mobile-item" @click="handleMobileNav('#about')">
            <span>Vision</span>
            <span class="mobile-item-arrow">→</span>
          </a>
          <a href="#faq" class="mobile-item" @click="handleMobileNav('#faq')">
            <span>FAQ</span>
            <span class="mobile-item-arrow">→</span>
          </a>
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

          <!-- Mobile Console Link (when logged in) -->
          <router-link
            v-if="authStore.isAuthenticated.value"
            to="/console"
            class="mobile-console-btn font-microgramma"
            @click="mobileMenuOpen = false"
          >
            Console
          </router-link>

          <div class="mobile-secondary-row">
            <div
              v-if="authStore.isAuthenticated.value"
              class="mobile-user-info"
              @click="authStore.openProfileModal(); mobileMenuOpen = false"
            >
              <div class="avatar">{{ userInitials }}</div>
              <span>{{ authStore.user.value?.full_name || 'My Account' }}</span>
            </div>

            <a
              href="https://obrive.com"
              target="_blank"
              rel="noopener noreferrer"
              class="mobile-ext-link font-microgramma"
            >
              Obrive Industries ↗
            </a>
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authStore from '../../store/auth'
import AnimatedButton from '../common/AnimatedButton.vue'

const router = useRouter()
const emit = defineEmits(['open-auth'])

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const handleSignIn = () => {
  if (authStore.isAuthenticated.value) {
    router.push('/console')
  } else {
    emit('open-auth')
    authStore.openAuthModal('login')
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
  max-width: 1180px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px 0 22px;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(7, 65, 57, 0.16);
  border-radius: 16px;
  box-shadow: 0 4px 20px -2px rgba(7, 65, 57, 0.06);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.header-outer.is-scrolled .header-pill {
  background-color: rgba(255, 255, 255, 0.96);
  border-color: rgba(7, 65, 57, 0.22);
  box-shadow: 0 10px 30px -4px rgba(7, 65, 57, 0.12);
  height: 58px;
}

/* Brand Logo */
.brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #074139;
  flex-shrink: 0;
}

.brand-logo {
  height: 24px;
  width: auto;
  display: block;
}

.brand-divider {
  width: 1px;
  height: 18px;
  background-color: rgba(7, 65, 57, 0.2);
}

.brand-text-lockup {
  display: flex;
  align-items: center;
  gap: 6px;
}

.brand-name {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
}

.brand-badge {
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  background: rgba(7, 65, 57, 0.08);
  color: #074139;
  border-radius: 4px;
  letter-spacing: 0.04em;
}

/* Nav Menu */
.nav-links {
  display: flex;
  align-items: center;
  gap: clamp(14px, 1.8vw, 24px);
}

.nav-item {
  color: #074139;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-decoration: none;
  padding: 6px 2px;
  position: relative;
  transition: color 0.2s ease;
  white-space: nowrap;
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
  border-radius: 2px;
}

.nav-item:hover::after {
  width: 100%;
}

/* Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.header-sign-in-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 16px;
  font-family: 'Microgramma', 'Michroma', sans-serif !important;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #074139;
  background: rgba(7, 65, 57, 0.05);
  border: 1px solid rgba(7, 65, 57, 0.28);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
}

.header-sign-in-btn:hover {
  background: #074139;
  color: #caede5;
  border-color: #074139;
  box-shadow: 0 4px 14px -2px rgba(7, 65, 57, 0.25);
  transform: translateY(-1px);
}

.header-sign-in-btn:active {
  transform: translateY(0);
}

.header-console-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 14px;
  font-family: 'Microgramma', 'Michroma', sans-serif !important;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #074139;
  text-decoration: none;
  background: rgba(7, 65, 57, 0.04);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.header-console-btn:hover {
  background: rgba(7, 65, 57, 0.1);
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
  padding: 6px 10px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.link-obrive:hover {
  color: #074139;
  background: rgba(7, 65, 57, 0.05);
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
  padding: 10px;
  color: #074139;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.mobile-toggle:hover {
  background: rgba(7, 65, 57, 0.06);
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

/* Backdrop */
.mobile-backdrop {
  pointer-events: auto;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(7, 65, 57, 0.3);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 101;
}

/* Mobile Drawer */
.mobile-drawer {
  pointer-events: auto;
  position: relative;
  z-index: 102;
  max-width: 600px;
  margin: 10px auto 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 18px;
  padding: 20px 22px 24px;
  box-shadow: 0 20px 45px -5px rgba(7, 65, 57, 0.2);
}

.mobile-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(7, 65, 57, 0.1);
}

.drawer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #074139;
}

.drawer-close-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #074139;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.drawer-close-btn:hover {
  background: rgba(7, 65, 57, 0.08);
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 20px;
}

.mobile-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #074139;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  padding: 10px 14px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.mobile-item:hover {
  background: rgba(7, 65, 57, 0.06);
  padding-left: 18px;
}

.mobile-item-arrow {
  font-size: 13px;
  color: rgba(7, 65, 57, 0.4);
  transition: transform 0.2s ease;
}

.mobile-item:hover .mobile-item-arrow {
  transform: translateX(3px);
  color: #074139;
}

.mobile-footer {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-top: 16px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.mobile-secondary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #074139;
  cursor: pointer;
}

.mobile-ext-link {
  color: rgba(7, 65, 57, 0.75);
  font-size: 11px;
  font-weight: 600;
  text-decoration: none;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  transition: color 0.2s ease;
}

.mobile-ext-link:hover {
  color: #074139;
}

.mobile-sign-in-btn,
.mobile-console-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 11px 16px;
  font-family: 'Microgramma', 'Michroma', sans-serif !important;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #074139;
  text-decoration: none;
  background: rgba(7, 65, 57, 0.05);
  border: 1px solid rgba(7, 65, 57, 0.24);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mobile-sign-in-btn:hover,
.mobile-console-btn:hover {
  background: #074139;
  color: #caede5;
  border-color: #074139;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.98);
}

/* Breakpoints */
@media (max-width: 1140px) {
  .link-obrive {
    display: none;
  }
}

@media (max-width: 1024px) {
  .nav-links {
    display: none;
  }

  .mobile-toggle {
    display: flex;
  }
}

@media (max-width: 640px) {
  .header-outer {
    padding: 8px 12px 0;
  }

  .header-pill {
    height: 54px;
    padding: 0 14px;
    border-radius: 12px;
  }
}

@media (max-width: 560px) {
  .header-actions .header-sign-in-btn,
  .header-actions .header-console-btn {
    display: none;
  }
}
</style>
