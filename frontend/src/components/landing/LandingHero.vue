<template>
  <section class="landing-hero" id="overview">
    <!-- Ambient background glows -->
    <div class="ambient-glow glow-top"></div>
    <div class="ambient-glow glow-right"></div>
    <div class="grid-overlay"></div>

    <div class="hero-container">
      <div class="hero-content">
        <!-- Brand category pill -->
        <div class="brand-pill">
          <span class="pill-pulse"></span>
          <span class="pill-text">PREDICTIVE INTELLIGENCE | POWERED BY OBRIVE</span>
        </div>

        <!-- Main Heading -->
        <h1 class="hero-title">
          OBMIND — <span class="title-sub">Predictive Intelligence</span>
        </h1>

        <!-- Subheading from docx -->
        <p class="hero-subtitle">
          Obmind helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
        </p>

        <!-- Primary Dual CTAs -->
        <div class="hero-ctas">
          <router-link to="/console" class="btn-primary-cta">
            <span>Predict Now</span>
            <span class="cta-arrow">→</span>
          </router-link>

          <a href="https://obrive.com" target="_blank" rel="noopener noreferrer" class="btn-secondary-cta">
            <span>Explore Obrive</span>
            <span class="cta-external">↗</span>
          </a>
        </div>

        <!-- Wishlist / Waitlist Banner from docx -->
        <div class="wishlist-card">
          <div class="wishlist-header">
            <span class="wishlist-sparkle">✦</span>
            <span class="wishlist-title">Join the Wishlist to get notified at launch !</span>
          </div>

          <form v-if="!submitted" @submit.prevent="handleWishlist" class="wishlist-form">
            <input
              v-model="email"
              type="email"
              placeholder="Enter your work email address..."
              class="wishlist-input"
              required
            />
            <button type="submit" class="wishlist-btn" :disabled="loading">
              {{ loading ? 'Joining...' : 'Join Wishlist' }}
            </button>
          </form>

          <div v-else class="wishlist-success">
            <span class="check-icon">✓</span> You're on the priority wishlist! We'll notify you as soon as new engine allocations open.
          </div>

          <p class="wishlist-disclaimer">
            Proposed product positioning. Capabilities should be enabled and validated before being presented as live features.
          </p>
        </div>
      </div>

      <!-- Hero Visual Representation -->
      <div class="hero-visual">
        <div class="radar-card">
          <div class="radar-header">
            <div class="radar-dots">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <span class="radar-status">SIMULATION CORE // ACTIVE</span>
          </div>

          <!-- Futuristic holographic simulation preview -->
          <div class="hologram-stage">
            <div class="central-node">
              <div class="node-pulse"></div>
              <img src="../../assets/logo/obfish-mascot.png" alt="ObMind Agent Swarm" class="mascot-img" />
            </div>

            <!-- Orbiting Agent Nodes -->
            <div class="orbit-ring ring-1">
              <div class="orbit-node node-a" title="Stakeholder Agent A">
                <span class="node-label">Enterprise</span>
              </div>
              <div class="orbit-node node-b" title="Market Agent B">
                <span class="node-label">Market</span>
              </div>
            </div>

            <div class="orbit-ring ring-2">
              <div class="orbit-node node-c" title="Consumer Sentiment Agent">
                <span class="node-label">Public Opinion</span>
              </div>
              <div class="orbit-node node-d" title="Policy Agent">
                <span class="node-label">Policy</span>
              </div>
            </div>
          </div>

          <!-- Bottom Metric HUD -->
          <div class="radar-hud">
            <div class="hud-item">
              <span class="hud-label">ENGINE</span>
              <span class="hud-val">OB-SWARM v2.4</span>
            </div>
            <div class="hud-item">
              <span class="hud-label">LATENCY</span>
              <span class="hud-val highlight">~120ms</span>
            </div>
            <div class="hud-item">
              <span class="hud-label">PRECISION</span>
              <span class="hud-val highlight">99.4% Graph</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const loading = ref(false)
const submitted = ref(false)

const handleWishlist = () => {
  if (!email.value) return
  loading.value = true
  setTimeout(() => {
    loading.value = false
    submitted.value = true
  }, 600)
}
</script>

<style scoped>
.landing-hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 120px 24px 60px;
  background: #070b0e;
  overflow: hidden;
}

.ambient-glow {
  position: absolute;
  pointer-events: none;
  filter: blur(120px);
  z-index: 1;
}

.glow-top {
  top: -100px;
  left: 20%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(7, 65, 57, 0.45) 0%, rgba(0, 229, 163, 0.08) 70%, transparent 100%);
}

.glow-right {
  bottom: 10%;
  right: -100px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(0, 229, 163, 0.12) 0%, rgba(7, 65, 57, 0.25) 70%, transparent 100%);
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  z-index: 1;
  pointer-events: none;
}

.hero-container {
  max-width: 1320px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.hero-content {
  display: flex;
  flex-direction: column;
}

.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(7, 65, 57, 0.35);
  border: 1px solid rgba(0, 229, 163, 0.25);
  border-radius: 9999px;
  width: fit-content;
  margin-bottom: 24px;
}

.pill-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #00E5A3;
  box-shadow: 0 0 10px #00E5A3;
  animation: pulse-glow 2s infinite ease-in-out;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.pill-text {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #00E5A3;
}

.hero-title {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: clamp(2.8rem, 5.5vw, 4.4rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin: 0 0 20px 0;
}

.title-sub {
  display: block;
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
  font-weight: 600;
  background: linear-gradient(135deg, #00E5A3 0%, #a2f1df 50%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-top: 6px;
}

.hero-subtitle {
  font-size: 1.15rem;
  line-height: 1.65;
  color: #94a3b8;
  max-width: 620px;
  margin: 0 0 36px 0;
}

.hero-ctas {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.btn-primary-cta {
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  color: #05080a;
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 25px rgba(0, 229, 163, 0.35);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-primary-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 229, 163, 0.5);
  color: #000;
}

.cta-arrow {
  transition: transform 0.2s ease;
}

.btn-primary-cta:hover .cta-arrow {
  transform: translateX(4px);
}

.btn-secondary-cta {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.25s ease;
  backdrop-filter: blur(8px);
}

.btn-secondary-cta:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(0, 229, 163, 0.4);
  color: #00E5A3;
}

.cta-external {
  font-size: 0.9rem;
  opacity: 0.7;
}

.wishlist-card {
  background: rgba(12, 18, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 20px 24px;
  backdrop-filter: blur(16px);
  max-width: 580px;
}

.wishlist-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.wishlist-sparkle {
  color: #00E5A3;
  font-size: 1rem;
}

.wishlist-title {
  font-size: 0.92rem;
  font-weight: 600;
  color: #e2e8f0;
  letter-spacing: 0.2px;
}

.wishlist-form {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.wishlist-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 10px 14px;
  color: #ffffff;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s ease;
}

.wishlist-input:focus {
  border-color: #00E5A3;
  box-shadow: 0 0 10px rgba(0, 229, 163, 0.2);
}

.wishlist-btn {
  background: #074139;
  border: 1px solid rgba(0, 229, 163, 0.4);
  color: #00E5A3;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.wishlist-btn:hover {
  background: #00E5A3;
  color: #070b0e;
}

.wishlist-success {
  padding: 10px 14px;
  background: rgba(0, 229, 163, 0.1);
  border: 1px solid rgba(0, 229, 163, 0.3);
  border-radius: 8px;
  color: #00E5A3;
  font-size: 0.85rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.wishlist-disclaimer {
  font-size: 0.75rem;
  line-height: 1.45;
  color: #64748b;
  margin: 0;
}

/* Radar Card Visual */
.hero-visual {
  display: flex;
  justify-content: center;
}

.radar-card {
  width: 100%;
  max-width: 480px;
  background: rgba(12, 18, 22, 0.8);
  border: 1px solid rgba(0, 229, 163, 0.2);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), inset 0 0 30px rgba(7, 65, 57, 0.3);
  backdrop-filter: blur(20px);
}

.radar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.radar-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #10b981; }

.radar-status {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: #00E5A3;
  letter-spacing: 1px;
}

.hologram-stage {
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.central-node {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(7, 65, 57, 0.9) 0%, rgba(7, 11, 14, 0.9) 100%);
  border: 2px solid #00E5A3;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 30px rgba(0, 229, 163, 0.4);
  z-index: 5;
}

.mascot-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
  filter: drop-shadow(0 0 8px #00E5A3);
}

.node-pulse {
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  border: 1px dashed rgba(0, 229, 163, 0.5);
  animation: spin 20s linear infinite;
}

.orbit-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.07);
}

.ring-1 {
  width: 200px;
  height: 200px;
  animation: spin 30s linear infinite;
}

.ring-2 {
  width: 280px;
  height: 280px;
  animation: spin-reverse 45s linear infinite;
}

.orbit-node {
  position: absolute;
  padding: 4px 10px;
  background: rgba(7, 65, 57, 0.85);
  border: 1px solid #00E5A3;
  border-radius: 20px;
  font-size: 0.7rem;
  color: #fff;
  white-space: nowrap;
  box-shadow: 0 0 10px rgba(0, 229, 163, 0.3);
}

.node-a { top: -14px; left: 50%; transform: translateX(-50%); }
.node-b { bottom: -14px; left: 50%; transform: translateX(-50%); }
.node-c { left: -20px; top: 50%; transform: translateY(-50%); }
.node-d { right: -20px; top: 50%; transform: translateY(-50%); }

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

.radar-hud {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 24px;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.hud-item {
  display: flex;
  flex-direction: column;
}

.hud-label {
  font-size: 0.68rem;
  font-family: 'JetBrains Mono', monospace;
  color: #64748b;
  letter-spacing: 0.5px;
}

.hud-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-top: 4px;
}

.hud-val.highlight {
  color: #00E5A3;
}

@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
    padding-top: 20px;
  }

  .hero-visual {
    order: -1;
  }

  .radar-card {
    max-width: 400px;
  }
}
</style>
