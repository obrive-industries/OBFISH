<template>
  <section class="landing-hero" id="overview">
    <div class="hero-container">
      <div class="hero-content">
        <!-- Main Heading in Microgramma Bold matching Owning the Future -->
        <h1 class="hero-title font-microgramma">
          Predictive Intelligence
        </h1>

        <!-- Subheading in Michroma font matching Obrive hero body -->
        <p class="hero-subtitle font-michroma">
          Obmind helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
        </p>

        <!-- Primary Dual Pill Buttons (Matched to Obrive.com screenshot) -->
        <div class="hero-ctas">
          <AnimatedButton
            to="/console"
            variant="primary"
            size="lg"
            :pill="true"
            :iconSize="16"
            class="hero-btn-pill font-michroma"
          >
            Predict Now
          </AnimatedButton>

          <AnimatedButton
            href="https://obrive.com"
            target="_blank"
            rel="noopener noreferrer"
            variant="outline"
            size="lg"
            :pill="true"
            :showArrow="false"
            class="hero-btn-pill font-michroma"
          >
            Explore Obrive
          </AnimatedButton>
        </div>

        <!-- Wishlist / Waitlist Banner from docx (Centered Frosted Card) -->
        <div class="wishlist-card">
          <div class="wishlist-header">
            <span class="wishlist-sparkle">✦</span>
            <span class="wishlist-title font-michroma">Join the Wishlist to get notified at launch !</span>
          </div>

          <form v-if="!submitted" @submit.prevent="handleWishlist" class="wishlist-form">
            <input
              v-model="email"
              type="email"
              placeholder="Enter your work email address..."
              class="wishlist-input"
              required
            />
            <AnimatedButton
              type="submit"
              variant="primary"
              size="default"
              :pill="true"
              :disabled="loading"
              :iconSize="13"
              class="font-michroma text-[10px]"
            >
              {{ loading ? 'Joining...' : 'Join Wishlist' }}
            </AnimatedButton>
          </form>

          <div v-else class="wishlist-success">
            <span class="check-icon">✓</span> You're on the priority wishlist! We'll notify you as soon as new engine allocations open.
          </div>

          <p class="wishlist-disclaimer">
            Proposed product positioning. Capabilities should be enabled and validated before being presented as live features.
          </p>
        </div>
      </div>
    </div>

    <!-- Obrive.com Brand Divider Line (Matched to page.tsx) -->
    <div class="brand-line-wrapper">
      <div class="brand-line-inner">
        <div class="brand-line-badge font-michroma">
          <span>SYSTEM READY</span>
        </div>
        <p class="brand-line-text font-michroma">
          TURNING COMPLEX UNCERTAINTIES INTO PREDICTIVE DECISIONS.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import AnimatedButton from '../common/AnimatedButton.vue'

const email = ref('')
const loading = ref(false)
const submitted = ref(false)

const handleWishlist = () => {
  if (!email.value) return
  loading.value = true
  setTimeout(() => {
    loading.value = false
    submitted.value = true
  }, 500)
}
</script>

<style scoped>
.landing-hero {
  position: relative;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 150px 24px 40px;
  background: linear-gradient(
    90deg,
    #caede5 0%,
    #beeee3 25%,
    #b2f0e1 50%,
    #a5f1df 75%,
    #98f2dd 100%
  );
  overflow: hidden;
}

.hero-container {
  max-width: 1080px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  z-index: 2;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* Main Heading matched to Owning the Future in Microgramma Bold font */
.hero-title {
  font-family: 'Microgramma', sans-serif !important;
  font-size: clamp(2.4rem, 5vw, 4.4rem);
  font-weight: 800;
  line-height: 1.15;
  color: #074139;
  margin: 0 0 24px 0;
  letter-spacing: -0.015em;
  text-transform: none; /* Exact Title Case matching screenshot */
}

/* Subheading in Michroma font */
.hero-subtitle {
  font-family: 'Michroma', sans-serif !important;
  font-size: clamp(0.82rem, 1.08vw, 0.98rem);
  line-height: 1.85;
  color: #074139;
  opacity: 0.95;
  max-width: 860px;
  margin: 0 0 36px 0;
  font-weight: 400;
  letter-spacing: 0.015em;
}

/* CTAs centered pills */
.hero-ctas {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.hero-btn-pill {
  font-family: 'Michroma', sans-serif !important;
  font-size: 11px !important;
  letter-spacing: 0.08em !important;
  padding: 13px 32px !important;
  text-transform: uppercase;
}

/* Wishlist Centered Frosted Card */
.wishlist-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 18px;
  padding: 24px 30px;
  box-shadow: 0 10px 30px -4px rgba(7, 65, 57, 0.08);
  max-width: 620px;
  width: 100%;
}

.wishlist-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}

.wishlist-sparkle {
  color: #074139;
  font-size: 14px;
}

.wishlist-title {
  font-family: 'Michroma', sans-serif !important;
  font-size: 11px;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.03em;
}

.wishlist-form {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.wishlist-input {
  flex: 1;
  background: #ffffff;
  border: 1px solid rgba(7, 65, 57, 0.25);
  border-radius: 9999px;
  padding: 11px 20px;
  font-size: 13px;
  color: #074139;
  outline: none;
  transition: all 0.2s ease;
}

.wishlist-input::placeholder {
  color: rgba(7, 65, 57, 0.5);
}

.wishlist-input:focus {
  border-color: #074139;
  box-shadow: 0 0 0 3px rgba(7, 65, 57, 0.12);
}

.wishlist-success {
  padding: 12px 16px;
  background: rgba(7, 65, 57, 0.08);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 12px;
  font-size: 12px;
  color: #074139;
  margin-bottom: 10px;
  font-weight: 500;
}

.check-icon {
  color: #074139;
  font-weight: 800;
  margin-right: 4px;
}

.wishlist-disclaimer {
  font-size: 11px;
  line-height: 1.5;
  color: rgba(7, 65, 57, 0.7);
  margin: 0;
  font-style: italic;
}

/* Obrive Brand Divider Line (Matched to obrive.com page.tsx) */
.brand-line-wrapper {
  width: 100%;
  max-width: 1180px;
  margin-top: 56px;
  padding: 0 20px;
  position: relative;
  z-index: 2;
}

.brand-line-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 24px;
  border-bottom: 2px solid rgba(7, 65, 57, 0.35);
}

.brand-line-badge {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(7, 65, 57, 0.25);
  color: #074139;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 6px 14px;
  border-radius: 9999px;
}

.brand-line-text {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
  margin: 0;
  text-align: right;
}

@media (max-width: 768px) {
  .landing-hero {
    padding: 120px 16px 36px;
  }

  .wishlist-form {
    flex-direction: column;
  }

  .brand-line-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .brand-line-text {
    text-align: left;
  }
}
</style>
