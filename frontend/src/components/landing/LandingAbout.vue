<template>
  <section class="section-about" id="about">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">ABOUT BRAIN</span>
        </div>

        <h2 class="section-title font-microgramma">
          Simulate Possibilities.<br />
          <span class="title-sub">Make Smarter Decisions.</span>
        </h2>
      </div>

      <!-- Narrative Story Grid -->
      <div class="narrative-grid">
        <div class="narrative-card">
          <p class="narrative-lead">
            BRAIN is an AI-powered simulation and predictive intelligence platform designed to explore possibilities, understand complex behaviours, and evaluate potential outcomes.
          </p>
          <p class="narrative-text">
            By transforming real-world information, business challenges, research materials, and creative ideas into interactive scenarios, BRAIN helps users examine how different factors, decisions, and interactions could shape future outcomes.
          </p>
        </div>

        <div class="narrative-card">
          <p class="narrative-text">
            Through AI-driven simulations, users can explore multiple perspectives, test assumptions, analyse stakeholder behaviour, and discover alternative pathways.
          </p>
          <p class="narrative-highlight">
            BRAIN creates a virtual environment where possibilities can be explored before decisions are made in the real world.
          </p>
        </div>
      </div>

      <!-- Vision & 3 Pillars -->
      <div class="vision-wrapper">
        <div class="vision-header">
          <span class="vision-eyebrow font-microgramma">OUR VISION</span>
          <h3 class="vision-title font-microgramma">
            Making advanced simulation accessible to everyone — from founders and enterprise leaders to researchers and creative storytellers.
          </h3>
        </div>

        <div class="pillars-grid">
          <!-- Pillar 1 -->
          <div class="pillar-card obrive-cell">
            <div class="pillar-top">
              <span class="pillar-level font-microgramma">01 // STRATEGIC LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name font-microgramma">Executive Strategy & Risk</h4>
            <p class="pillar-desc">
              Explore business strategies, evaluate market opportunities, examine stakeholder responses, and assess potential risks before committing real capital and organizational resources.
            </p>
          </div>

          <!-- Pillar 2 -->
          <div class="pillar-card obrive-cell">
            <div class="pillar-top">
              <span class="pillar-level font-microgramma">02 // CREATIVE LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name font-microgramma">Idea Sandbox & Worldbuilding</h4>
            <p class="pillar-desc">
              A generative sandbox for exploring ideas, developing fictional worlds, simulating character interactions, and discovering alternative storylines and creative endings.
            </p>
          </div>

          <!-- Pillar 3 -->
          <div class="pillar-card obrive-cell">
            <div class="pillar-top">
              <span class="pillar-level font-microgramma">03 // RESEARCH LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name font-microgramma">Hypothesis & Complexity</h4>
            <p class="pillar-desc">
              Enable researchers and policy makers to investigate hypotheses, explore non-linear relationships, and generate targeted questions for real-world empirical validation.
            </p>
          </div>
        </div>
      </div>

      <!-- High Impact Quote Card in Obrive Dark Teal Primary Style -->
      <div class="quote-card">
        <div class="quote-content">
          <p class="quote-body font-microgramma">
            “Every possibility begins with a question. BRAIN helps you explore what comes next.”
          </p>
          <div class="quote-author">
            <img src="../../assets/icons/obrive-white-logo.svg" alt="Obrive" class="quote-logo" />
            <div class="quote-author-meta">
              <span class="author-name font-microgramma">BRAIN by Obrive Industries</span>
              <span class="author-tag">Predictive Intelligence Architecture</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Explanatory Disclaimer from docx -->
      <p class="about-disclaimer">
        Simulated results are exploratory, not guaranteed forecasts or substitutes for real-world evidence, professional judgement, or validated research.
      </p>
    </div>
  </section>
</template>

<script setup>
import RoundedBallIcon from '../common/RoundedBallIcon.vue'
</script>

<style scoped>
.section-about {
  padding: 120px 24px 90px;
  background: #000000;
  position: relative;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 860px;
  margin: 0 auto 60px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 9999px;
  margin-bottom: 22px;
}

.pill-text {
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #ffffff;
}

.section-title {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: clamp(2.2rem, 3.8vw, 3.4rem);
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.02em;
  line-height: 1.15;
}

.title-sub {
  color: rgba(255, 255, 255, 0.7);
}

/* Narrative Grid */
.narrative-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin-bottom: 70px;
}

.narrative-card {
  background: #09090b;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 40px 36px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.narrative-lead {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.18rem;
  font-weight: 600;
  line-height: 1.6;
  color: #ffffff;
  margin: 0 0 18px 0;
}

.narrative-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 18px 0;
}

.narrative-text:last-child {
  margin-bottom: 0;
}

.narrative-highlight {
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.6;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 22px;
  border-radius: 12px;
  border-left: 3px solid #ffffff;
  margin: 0;
}

/* Vision */
.vision-wrapper {
  margin-bottom: 70px;
}

.vision-header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 44px;
}

.vision-eyebrow {
  display: inline-block;
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 14px;
}

.vision-title {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: clamp(1.25rem, 2vw, 1.65rem);
  font-weight: 600;
  color: #ffffff;
  line-height: 1.45;
  margin: 0;
}

/* Pillars */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.pillar-card {
  background: #09090b;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 34px 30px;
  min-height: 260px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.pillar-card:hover {
  transform: translateY(-4px);
  background: #111114;
  border-color: rgba(255, 255, 255, 0.32);
  box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.8), 0 0 24px rgba(255, 255, 255, 0.05);
}

.pillar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.pillar-level {
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.3s ease;
}

.pillar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.pillar-card:hover .pillar-level {
  color: #ffffff;
}

.pillar-name {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 14px 0;
  line-height: 1.35;
  transition: color 0.3s ease;
}

.pillar-desc {
  font-size: 0.9rem;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.68);
  margin: 0;
  flex: 1;
  transition: color 0.3s ease;
}

.pillar-card:hover .pillar-desc {
  color: rgba(255, 255, 255, 0.9);
}

/* Quote Card in MiroFish High Impact Card */
.quote-card {
  background: linear-gradient(135deg, #131318 0%, #09090b 100%);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 20px;
  padding: 48px 44px;
  margin-bottom: 36px;
  box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.8);
  position: relative;
  overflow: hidden;
}

.quote-card::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.06), transparent 70%);
  pointer-events: none;
}

.quote-content {
  display: flex;
  flex-direction: column;
  gap: 26px;
}

.quote-body {
  font-family: var(--font-display, "Space Grotesk", sans-serif);
  font-size: clamp(1.25rem, 2.2vw, 1.8rem);
  font-weight: 600;
  line-height: 1.4;
  color: #ffffff;
  margin: 0;
  max-width: 920px;
  letter-spacing: -0.01em;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
}

.quote-logo {
  height: 28px;
  width: auto;
}

.quote-author-meta {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-family: var(--font-mono, monospace);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #ffffff;
}

.author-tag {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

.about-disclaimer {
  text-align: center;
  font-size: 11px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.5);
  max-width: 780px;
  margin: 0 auto;
  font-style: italic;
}

@media (max-width: 960px) {
  .narrative-grid {
    grid-template-columns: 1fr;
  }

  .pillars-grid {
    grid-template-columns: 1fr;
  }
}
</style>
