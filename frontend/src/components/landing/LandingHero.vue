<template>
  <section class="landing-hero" id="overview">
    <div class="hero-container">
      <div class="hero-content">
        <!-- Brand category pill with Obrive 3-ball icon -->
        <div class="brand-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">PREDICTIVE INTELLIGENCE | POWERED BY OBRIVE</span>
        </div>

        <!-- Main Heading from docx & MiroFish in Microgramma Bold -->
        <h1 class="hero-title font-microgramma">
          OBMIND — <span class="title-sub">PREDICTIVE INTELLIGENCE</span>
        </h1>

        <!-- Subheading from docx -->
        <p class="hero-subtitle">
          Obmind helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
        </p>

        <!-- Primary Dual CTAs centered (Matched to Obrive.com) -->
        <div class="hero-ctas">
          <AnimatedButton
            to="/console"
            variant="primary"
            size="lg"
            :iconSize="16"
          >
            Predict Now
          </AnimatedButton>

          <AnimatedButton
            href="https://obrive.com"
            target="_blank"
            rel="noopener noreferrer"
            variant="outline"
            size="lg"
            :iconSize="16"
          >
            Explore Obrive
          </AnimatedButton>
        </div>

        <!-- Wishlist / Waitlist Banner from docx (Centered Frosted Card) -->
        <div class="wishlist-card">
          <div class="wishlist-header">
            <span class="wishlist-sparkle">✦</span>
            <span class="wishlist-title font-microgramma">Join the Wishlist to get notified at launch !</span>
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
              :disabled="loading"
              :iconSize="13"
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
        <div class="brand-line-badge font-microgramma">
          <span>SYSTEM READY</span>
        </div>
        <p class="brand-line-text font-microgramma">
          TURNING COMPLEX UNCERTAINTIES INTO PREDICTIVE DECISIONS.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import AnimatedButton from '../common/AnimatedButton.vue'
import RoundedBallIcon from '../common/RoundedBallIcon.vue'

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
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 160px 24px 40px;
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
  max-width: 1100px;
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

/* Category Pill */
.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 7px 18px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 9999px;
  width: fit-content;
  margin-bottom: 28px;
  box-shadow: 0 2px 10px rgba(7, 65, 57, 0.04);
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #074139;
}

/* Main Titles */
.hero-title {
  font-size: clamp(2.4rem, 4.8vw, 4.4rem);
  font-weight: 700;
  line-height: 1.1;
  color: #074139;
  margin: 0 0 22px 0;
  letter-spacing: -0.01em;
  max-width: 980px;
}

.title-sub {
  color: #0d5c52;
  font-weight: 700;
}

.hero-subtitle {
  font-size: clamp(1.05rem, 1.35vw, 1.25rem);
  line-height: 1.7;
  color: #074139;
  opacity: 0.92;
  max-width: 820px;
  margin: 0 0 36px 0;
  font-weight: 450;
}

/* CTAs centered */
.hero-ctas {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

/* Wishlist Centered Frosted Card */
.wishlist-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 16px;
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
  font-size: 12px;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.04em;
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
  border-radius: 10px;
  padding: 11px 16px;
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
  border-radius: 10px;
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
  max-width: 1200px;
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
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 6px 14px;
  border-radius: 8px;
}

.brand-line-text {
  font-size: 11px;
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
