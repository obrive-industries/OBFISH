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
          Brain helps transform information, research, and ideas into simulated scenarios that support better-informed decisions.
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
      </div>
    </div>
  </section>
</template>

<script setup>
import AnimatedButton from '../common/AnimatedButton.vue'
</script>

<style scoped>
.landing-hero {
  position: relative;
  min-height: 72vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 170px 24px 100px;
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
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-size: clamp(2.25rem, 4.5vw, 3.75rem);
  font-weight: 800;
  line-height: 1.15;
  color: #074139;
  margin: 0 0 24px 0;
  letter-spacing: 0;
  text-transform: none; /* Exact Title Case matching screenshot */
}

/* Subheading in Michroma font matched to Obrive hero body */
.hero-subtitle {
  font-family: 'Michroma', sans-serif !important;
  font-size: clamp(0.875rem, 1.1vw, 1rem);
  line-height: 1.75;
  color: #074139;
  max-width: 896px;
  padding: 0 16px;
  margin: 0 auto 36px auto;
  font-weight: 400;
  letter-spacing: 0.01em;
  text-align: center;
  text-wrap: balance;
}

/* CTAs centered pills */
.hero-ctas {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 0;
  flex-wrap: wrap;
}

.hero-btn-pill {
  font-family: 'Michroma', sans-serif !important;
  font-size: 12px !important;
  letter-spacing: 0.06em !important;
  padding: 13px 32px !important;
  text-transform: uppercase;
}

@media (max-width: 768px) {
  .landing-hero {
    padding: 130px 16px 60px;
    min-height: auto;
  }
}
</style>
