<template>
  <section class="landing-hero" id="overview">
    <!-- Curved vector background from Obrive -->
    <div class="hero-bg-curves">
      <img
        src="../../assets/backgrounds/bg-animate-accent.svg"
        alt="Obrive Curves"
        class="bg-curve-vector"
      />
    </div>

    <div class="hero-container">
      <div class="hero-content">
        <!-- Brand category pill with Obrive 3-ball icon -->
        <div class="brand-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">PREDICTIVE INTELLIGENCE | POWERED BY OBRIVE</span>
        </div>

        <!-- Main Heading from docx & MiroFish -->
        <h1 class="hero-title font-microgramma">
          OBMIND — <span class="title-sub">PREDICTIVE INTELLIGENCE</span>
        </h1>

        <!-- Subheading from docx -->
        <p class="hero-subtitle">
          Obmind helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
        </p>

        <!-- Primary Dual CTAs using Obrive AnimatedButton -->
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

        <!-- Wishlist / Waitlist Banner from docx -->
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

      <!-- Hero Visual: Multi-Agent Simulation Core -->
      <div class="hero-visual">
        <div class="simulation-showcase-card">
          <div class="card-hud-bar">
            <div class="card-dots">
              <span class="dot d-1"></span>
              <span class="dot d-2"></span>
              <span class="dot d-3"></span>
            </div>
            <div class="card-status-badge">
              <span class="status-pulse"></span>
              <span class="hud-status font-microgramma">SIMULATION ENGINE // ACTIVE</span>
            </div>
          </div>

          <!-- Dynamic Agent Stage -->
          <div class="hologram-stage">
            <div class="central-node">
              <div class="node-ring-pulse"></div>
              <img
                src="../../assets/icons/obrive-logo.svg"
                alt="ObMind Simulation Core"
                class="core-logo"
              />
              <span class="core-label font-microgramma">OBMIND</span>
            </div>

            <!-- Orbiting Agent Nodes -->
            <div class="orbit-track track-1">
              <div class="orbit-agent agent-enterprise" title="Enterprise Stakeholders">
                <span class="agent-avatar">🏢</span>
                <span class="agent-tag">Enterprise</span>
              </div>
              <div class="orbit-agent agent-market" title="Market Forces">
                <span class="agent-avatar">📈</span>
                <span class="agent-tag">Market</span>
              </div>
            </div>

            <div class="orbit-track track-2">
              <div class="orbit-agent agent-opinion" title="Public Sentiment">
                <span class="agent-avatar">💬</span>
                <span class="agent-tag">Public Opinion</span>
              </div>
              <div class="orbit-agent agent-regulator" title="Policy & Regulatory">
                <span class="agent-avatar">⚖️</span>
                <span class="agent-tag">Regulatory</span>
              </div>
            </div>

            <!-- Emergent Connection Rays -->
            <svg class="connection-mesh" viewBox="0 0 400 400">
              <circle cx="200" cy="200" r="110" stroke="rgba(7, 65, 57, 0.18)" stroke-dasharray="4 4" fill="none" />
              <circle cx="200" cy="200" r="160" stroke="rgba(7, 65, 57, 0.12)" stroke-dasharray="6 6" fill="none" />
              <line x1="200" y1="200" x2="110" y2="120" stroke="rgba(7, 65, 57, 0.3)" stroke-width="1.5" />
              <line x1="200" y1="200" x2="290" y2="280" stroke="rgba(7, 65, 57, 0.3)" stroke-width="1.5" />
              <line x1="200" y1="200" x2="100" y2="270" stroke="rgba(7, 65, 57, 0.25)" stroke-width="1.5" />
              <line x1="200" y1="200" x2="300" y2="130" stroke="rgba(7, 65, 57, 0.25)" stroke-width="1.5" />
            </svg>
          </div>

          <!-- Bottom Telemetry Stats -->
          <div class="card-telemetry">
            <div class="telemetry-item">
              <span class="tel-label">Active Agents</span>
              <span class="tel-val font-microgramma">128+ Twins</span>
            </div>
            <div class="telemetry-item">
              <span class="tel-label">Emergence Depth</span>
              <span class="tel-val font-microgramma">5 Horizons</span>
            </div>
            <div class="telemetry-item">
              <span class="tel-label">Fidelity</span>
              <span class="tel-val font-microgramma highlight">99.4% Graph</span>
            </div>
          </div>
        </div>
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
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 130px 24px 80px;
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

.hero-bg-curves {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.65;
  z-index: 1;
}

.bg-curve-vector {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.hero-container {
  max-width: 1240px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 56px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.hero-content {
  display: flex;
  flex-direction: column;
}

/* Category Pill */
.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 9999px;
  width: fit-content;
  margin-bottom: 24px;
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #074139;
}

/* Titles */
.hero-title {
  font-size: clamp(2.4rem, 4.2vw, 3.8rem);
  font-weight: 700;
  line-height: 1.08;
  color: #074139;
  margin: 0 0 20px 0;
  letter-spacing: -0.01em;
}

.title-sub {
  color: #0d5c52;
  font-weight: 700;
}

.hero-subtitle {
  font-size: clamp(1rem, 1.25vw, 1.18rem);
  line-height: 1.65;
  color: #074139;
  opacity: 0.9;
  max-width: 620px;
  margin: 0 0 32px 0;
  font-weight: 450;
}

/* CTAs */
.hero-ctas {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}

/* Wishlist Outlined Card */
.wishlist-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 16px;
  padding: 22px 26px;
  box-shadow: 0 8px 30px -4px rgba(7, 65, 57, 0.08);
  max-width: 580px;
}

.wishlist-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
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
  padding: 10px 16px;
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
  padding: 10px 14px;
  background: rgba(7, 65, 57, 0.08);
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 8px;
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

/* Simulation Showcase Card */
.hero-visual {
  display: flex;
  justify-content: center;
}

.simulation-showcase-card {
  width: 100%;
  max-width: 480px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 20px;
  box-shadow: 0 20px 50px -10px rgba(7, 65, 57, 0.14);
  overflow: hidden;
}

.card-hud-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: rgba(7, 65, 57, 0.05);
  border-bottom: 1px solid rgba(7, 65, 57, 0.12);
}

.card-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.dot.d-1 {
  background: #ff5f56;
}

.dot.d-2 {
  background: #ffbd2e;
}

.dot.d-3 {
  background: #27c93f;
}

.card-status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00E5A3;
  box-shadow: 0 0 8px #00E5A3;
  animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.6; }
}

.hud-status {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #074139;
}

/* Hologram Stage */
.hologram-stage {
  position: relative;
  height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.connection-mesh {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.central-node {
  position: relative;
  z-index: 5;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #074139;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px rgba(7, 65, 57, 0.35);
}

.core-logo {
  height: 28px;
  filter: brightness(0) invert(1);
}

.core-label {
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #caede5;
  margin-top: 4px;
}

.node-ring-pulse {
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid rgba(7, 65, 57, 0.3);
  animation: pulse-ring 3s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(0.9); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

/* Orbit tracks */
.orbit-track {
  position: absolute;
  border-radius: 50%;
  border: 1px dashed rgba(7, 65, 57, 0.16);
  pointer-events: none;
}

.track-1 {
  width: 220px;
  height: 220px;
  animation: spin 32s linear infinite;
}

.track-2 {
  width: 320px;
  height: 320px;
  animation: spin-reverse 45s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

.orbit-agent {
  position: absolute;
  pointer-events: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 6px 10px;
  background: #ffffff;
  border: 1px solid rgba(7, 65, 57, 0.2);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(7, 65, 57, 0.12);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.orbit-agent:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(7, 65, 57, 0.2);
}

.agent-avatar {
  font-size: 16px;
}

.agent-tag {
  font-size: 9px;
  font-weight: 700;
  color: #074139;
  letter-spacing: 0.02em;
}

/* Positions on tracks */
.agent-enterprise {
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
}

.agent-market {
  bottom: -16px;
  left: 50%;
  transform: translateX(-50%);
}

.agent-opinion {
  left: -20px;
  top: 50%;
  transform: translateY(-50%);
}

.agent-regulator {
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
}

/* Telemetry Stats Bar */
.card-telemetry {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  padding: 14px 20px;
  background: rgba(7, 65, 57, 0.04);
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.telemetry-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tel-label {
  font-size: 10px;
  color: rgba(7, 65, 57, 0.7);
  font-weight: 500;
}

.tel-val {
  font-size: 12px;
  font-weight: 700;
  color: #074139;
}

.tel-val.highlight {
  color: #074139;
}

/* Responsiveness */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .hero-content {
    align-items: center;
    text-align: center;
  }

  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }

  .hero-ctas {
    justify-content: center;
  }

  .wishlist-card {
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .landing-hero {
    padding: 100px 16px 60px;
  }

  .wishlist-form {
    flex-direction: column;
  }

  .hologram-stage {
    height: 320px;
  }

  .track-2 {
    width: 280px;
    height: 280px;
  }
}
</style>
