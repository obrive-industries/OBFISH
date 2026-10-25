<template>
  <section id="hero" class="hero-section">
    <!-- Ambient Glowing Hero Orb -->
    <div class="hero-orb" aria-hidden="true"></div>

    <div class="container-main relative z-[2]">
      <div class="hero-content">
        <!-- Main Headline -->
        <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold text-white mb-8 tracking-tight hero-heading">
          <span>Predictive</span>
          <span class="relative inline-block whitespace-nowrap ml-2 sm:ml-4">
            Intelligence
            <svg class="absolute -bottom-2 left-0 w-full" viewBox="0 0 200 12" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path class="underline-path" d="M2 10C50 4 150 4 198 10" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
            </svg>
          </span>
        </h1>

        <!-- Tagline -->
        <p class="text-xl md:text-2xl text-gray-500 mb-12 max-w-2xl mx-auto leading-relaxed">
          Brain helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-wrap gap-5 justify-center mb-8">
          <router-link
            to="/console"
            class="hero-btn-primary group"
          >
            <span class="relative z-[1]">Predict Now</span>
          </router-link>

          <a
            href="https://obrive.com"
            target="_blank"
            rel="noopener noreferrer"
            class="hero-btn-github group"
          >
            <img src="/obrive-white-logo.svg" alt="Obrive" class="hero-btn-logo" />
            <span class="relative z-[1]">Explore Obrive</span>
          </a>
        </div>

        <!-- Wishlist Form (MiroFish Style) -->
        <div class="wishlist-wrapper mt-4 mb-4 w-full max-w-xl mx-auto">
          <h2 class="wishlist-heading text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-3" style="font-family: 'Caveat', cursive; font-style: italic;">
            Join the Wishlist to get notified about offers !
          </h2>
          <p class="wishlist-subtitle text-sm sm:text-base text-gray-400 mb-6 leading-relaxed">
            <span class="block">Proposed product positioning.</span>
            <span class="block">Capabilities should be enabled and validated before being presented as live features.</span>
          </p>

          <form @submit.prevent="handleWishlistSubmit" class="wishlist-form flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <input
              v-model="emailInput"
              type="email"
              placeholder="Enter your email"
              required
              class="wishlist-input flex-1 px-4 py-3 bg-transparent border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white transition-colors"
              :disabled="submitting"
            />
            <button
              type="submit"
              class="wishlist-submit inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 bg-white text-black hover:bg-gray-200 px-6 py-3 text-base cursor-pointer"
              :disabled="submitting || !emailInput"
            >
              <span v-if="!submitting">Send</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4 text-black" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                Sending...
              </span>
            </button>
          </form>

          <!-- Feedback alerts (Prominent Confirmation Card) -->
          <div
            v-if="feedbackMsg"
            class="mt-4 p-4 rounded-xl text-sm font-medium transition-all max-w-md mx-auto flex items-center justify-center gap-2.5 shadow-xl"
            :class="isSuccess ? 'bg-emerald-500/15 border border-emerald-500/40 text-emerald-300' : 'bg-rose-500/15 border border-rose-500/40 text-rose-300'"
          >
            <span class="text-base font-bold">{{ isSuccess ? '✓' : '⚠️' }}</span>
            <span>{{ feedbackMsg }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Pulsing Down Indicator -->
    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 cursor-pointer pulse-down" @click="scrollDown">
      <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M19 14l-7 7m0 0l-7-7m7 7V3" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import wishlistApi from '../../api/wishlist'

const emailInput = ref('')
const submitting = ref(false)
const feedbackMsg = ref('')
const isSuccess = ref(false)

const handleWishlistSubmit = async () => {
  if (!emailInput.value || submitting.value) return
  submitting.value = true
  feedbackMsg.value = ''
  try {
    const res = await wishlistApi.subscribe(emailInput.value, 'landing_hero')
    const ok = res?.success || res?.data?.success
    const msg = res?.message || res?.data?.message
    if (ok) {
      isSuccess.value = true
      feedbackMsg.value = msg || "Thank you for joining our wishlist! We'll notify you about exclusive offers."
      emailInput.value = ''
    } else {
      isSuccess.value = false
      feedbackMsg.value = res?.error || res?.data?.error || 'Something went wrong. Please try again.'
    }
  } catch (err) {
    isSuccess.value = false
    feedbackMsg.value = err.message || err.response?.data?.error || 'Failed to submit. Please try again.'
  } finally {
    submitting.value = false
  }
}

const scrollDown = () => {
  const el = document.getElementById('features')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap');

.hero-section {
  position: relative;
  min-height: 75vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 7rem;
  padding-bottom: 3.5rem;
  background-color: #000000;
  overflow: hidden;
  box-sizing: border-box;
}

.container-main {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
  width: 100%;
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

.hero-content {
  max-width: 56rem;
  width: 100%;
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-heading {
  text-align: center;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35em;
  flex-wrap: nowrap;
}

@media (max-width: 640px) {
  .hero-heading {
    flex-wrap: wrap;
    gap: 8px 12px;
  }
}

.underline-path {
  stroke-dasharray: 210;
  stroke-dashoffset: 210;
  animation: draw-underline 0.6s ease-out 0.5s forwards;
}

@keyframes draw-underline {
  to { stroke-dashoffset: 0; }
}

.hero-orb {
  position: absolute;
  width: 600px;
  height: 400px;
  border-radius: 50%;
  background: #6482dc0f;
  filter: blur(80px);
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
  animation: drift-hero 30s ease-in-out infinite;
}

@keyframes drift-hero {
  0%, 100% { transform: translate(-50%, -50%); }
  50% { transform: translate(calc(-50% + 20px), calc(-50% - 15px)); }
}

.hero-btn-primary {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  line-height: 1.75rem;
  font-weight: 700;
  padding: 0.875rem 2.25rem;
  border-radius: 0.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1e1e22, #35353c, #62626e, #8a8a98 45%, #a0a0b0, #8a8a98 55%, #62626e, #35353c, #1e1e22);
  background-size: 200% 200%;
  animation: metal-shift 8s ease infinite;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: inset 0 1px #ffffff40, inset 0 -1px #0000004d, 0 2px 12px #0006, 0 0 30px #b4b4c81a;
  filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.5));
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: #ffffff;
  box-sizing: border-box;
}

.hero-btn-primary:before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(105deg, transparent 20%, rgba(255, 255, 255, 0.15) 45%, rgba(255, 255, 255, 0.22) 50%, rgba(255, 255, 255, 0.15) 55%, transparent 80%);
  background-size: 300% 100%;
  animation: metal-shimmer 6s ease-in-out infinite;
}

.hero-btn-primary:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #252529, #3e3e46, #70707e, #9898a8 45%, #b0b0c0, #9898a8 55%, #70707e, #3e3e46, #252529);
  background-size: 200% 200%;
  border-color: #ffffff4d;
  box-shadow: inset 0 1px #ffffff59, inset 0 -1px #0000004d, 0 4px 20px #00000080, 0 0 40px #c8c8dc33;
}

.hero-btn-primary:active {
  transform: translateY(0) scale(0.98);
}

@keyframes metal-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes metal-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.hero-btn-github {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  line-height: 1.75rem;
  font-weight: 700;
  padding: 0.875rem 2rem;
  border-radius: 0.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  position: relative;
  overflow: hidden;
  background: #ffffff0f;
  border: 1px solid rgba(255, 255, 255, 0.12);
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: #ffffff;
  box-sizing: border-box;
}

.hero-btn-github:before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(105deg, transparent 40%, rgba(255, 255, 255, 0.08) 50%, transparent 60%);
  background-size: 300% 100%;
  background-position: 50% 0;
}

.hero-btn-github:hover {
  background: #ffffff1a;
  border-color: #ffffff38;
  transform: translateY(-1px);
}

.hero-btn-github:active {
  transform: translateY(0);
}

.hero-btn-logo {
  height: 1.25rem;
  width: auto;
  position: relative;
  z-index: 1;
  object-fit: contain;
  opacity: 0.9;
  transition: transform 0.3s ease;
}

.hero-btn-github:hover .hero-btn-logo {
  transform: scale(1.1);
}

.pulse-down {
  animation: pulse-sink 2.4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@keyframes pulse-sink {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}

.wishlist-wrapper {
  position: relative;
  z-index: 5;
}

.wishlist-heading {
  font-family: 'Caveat', cursive !important;
  font-style: italic !important;
  letter-spacing: 0.02em;
  font-weight: 700;
}

.wishlist-input {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.wishlist-input:focus {
  border-color: #ffffff;
  outline: none;
  background: rgba(255, 255, 255, 0.08);
}

.wishlist-submit {
  background-color: #ffffff;
  color: #000000;
  border-radius: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
}

.wishlist-submit:hover:not(:disabled) {
  background-color: #e5e7eb;
  transform: translateY(-1px);
}

.wishlist-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
