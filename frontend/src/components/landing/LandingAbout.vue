<template>
  <section class="section-about" id="about">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">ABOUT US: SIMULATE POSSIBILITIES. MAKE SMARTER DECISIONS.</span>
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
            OBMIND is an AI-powered simulation and predictive intelligence platform designed to explore possibilities, understand complex behaviours, and evaluate potential outcomes.
          </p>
          <p class="narrative-text">
            By transforming real-world information, business challenges, research materials, and creative ideas into interactive scenarios, OBMIND helps users examine how different factors, decisions, and interactions could shape future outcomes.
          </p>
        </div>

        <div class="narrative-card">
          <p class="narrative-text">
            Through AI-driven simulations, users can explore multiple perspectives, test assumptions, analyse stakeholder behaviour, and discover alternative pathways.
          </p>
          <p class="narrative-highlight">
            OBMIND creates a virtual environment where possibilities can be explored before decisions are made in the real world.
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
            “Every possibility begins with a question. OBMIND helps you explore what comes next.”
          </p>
          <div class="quote-author">
            <img src="../../assets/icons/obrive-white-logo.svg" alt="Obrive" class="quote-logo" />
            <div class="quote-author-meta">
              <span class="author-name font-microgramma">OBMIND by Obrive Industries</span>
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
  padding: 110px 24px 80px;
  background: #f8fbfa;
  position: relative;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 860px;
  margin: 0 auto 56px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(7, 65, 57, 0.06);
  border: 1px solid rgba(7, 65, 57, 0.18);
  border-radius: 9999px;
  margin-bottom: 20px;
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #074139;
}

.section-title {
  font-size: clamp(2.2rem, 3.8vw, 3.2rem);
  font-weight: 700;
  color: #074139;
  margin: 0;
  letter-spacing: -0.01em;
}

.title-sub {
  color: #0d5c52;
}

/* Narrative Grid */
.narrative-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin-bottom: 60px;
}

.narrative-card {
  background: #ffffff;
  border: 1px solid rgba(7, 65, 57, 0.16);
  border-radius: 18px;
  padding: 36px 32px;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.narrative-lead {
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.6;
  color: #074139;
  margin: 0 0 16px 0;
}

.narrative-text {
  font-size: 0.95rem;
  line-height: 1.65;
  color: rgba(7, 65, 57, 0.85);
  margin: 0 0 16px 0;
}

.narrative-highlight {
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.6;
  color: #074139;
  background: rgba(162, 241, 223, 0.35);
  padding: 16px 20px;
  border-radius: 12px;
  border-left: 3px solid #074139;
  margin: 0;
}

/* Vision */
.vision-wrapper {
  margin-bottom: 60px;
}

.vision-header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 40px;
}

.vision-eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #074139;
  opacity: 0.75;
  margin-bottom: 12px;
}

.vision-title {
  font-size: clamp(1.2rem, 2vw, 1.55rem);
  font-weight: 700;
  color: #074139;
  line-height: 1.4;
  margin: 0;
}

/* Pillars */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.pillar-card {
  background: #ffffff;
  padding: 32px 28px;
  min-height: 260px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.pillar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.pillar-level {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #074139;
  transition: color 0.4s ease;
}

.pillar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00E5A3;
}

.pillar-card:hover .pillar-level {
  color: #a2f1df !important;
}

.pillar-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #074139;
  margin: 0 0 14px 0;
  line-height: 1.3;
  transition: color 0.4s ease;
}

.pillar-card:hover .pillar-name {
  color: #ffffff !important;
}

.pillar-desc {
  font-size: 0.88rem;
  line-height: 1.65;
  color: rgba(7, 65, 57, 0.85);
  margin: 0;
  flex: 1;
  transition: color 0.4s ease;
}

.pillar-card:hover .pillar-desc {
  color: rgba(255, 255, 255, 0.9) !important;
}

/* Quote Card in Primary Dark Teal */
.quote-card {
  background: #074139;
  border-radius: 20px;
  padding: 44px 40px;
  margin-bottom: 30px;
  box-shadow: 0 16px 40px -8px rgba(7, 65, 57, 0.25);
  position: relative;
  overflow: hidden;
}

.quote-card::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(162, 241, 223, 0.15), transparent 70%);
  pointer-events: none;
}

.quote-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.quote-body {
  font-size: clamp(1.2rem, 2.2vw, 1.7rem);
  font-weight: 700;
  line-height: 1.35;
  color: #caede5;
  margin: 0;
  max-width: 900px;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 18px;
  border-top: 1px solid rgba(202, 237, 229, 0.2);
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
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #ffffff;
}

.author-tag {
  font-size: 11px;
  color: rgba(202, 237, 229, 0.7);
}

.about-disclaimer {
  text-align: center;
  font-size: 11px;
  line-height: 1.5;
  color: rgba(7, 65, 57, 0.65);
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
