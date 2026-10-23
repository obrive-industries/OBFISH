<template>
  <section class="section-about" id="about">
    <div class="container">
      <!-- Section Header -->
      <div class="section-header">
        <div class="category-pill">
          <span class="pill-dot"></span>
          About Us: Simulate Possibilities. Make Smarter Decisions.
        </div>

        <h2 class="section-title">
          Simulate Possibilities.<br />
          <span class="gradient-text">Make Smarter Decisions.</span>
        </h2>
      </div>

      <!-- Narrative Story Grid -->
      <div class="narrative-grid">
        <div class="narrative-col">
          <p class="narrative-lead">
            OBMIND is an AI-powered simulation and predictive intelligence platform designed to explore possibilities, understand complex behaviours, and evaluate potential outcomes.
          </p>
          <p class="narrative-text">
            By transforming real-world information, business challenges, research materials, and creative ideas into interactive scenarios, OBMIND helps users examine how different factors, decisions, and interactions could shape future outcomes.
          </p>
        </div>

        <div class="narrative-col">
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
          <span class="vision-eyebrow">OUR VISION</span>
          <h3 class="vision-title">
            Making advanced simulation accessible to everyone — from founders and enterprise leaders to researchers and creative storytellers.
          </h3>
        </div>

        <div class="pillars-grid">
          <!-- Pillar 1 -->
          <div class="pillar-card">
            <div class="pillar-top">
              <span class="pillar-level">01 // STRATEGIC LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name">Executive Strategy & Risk</h4>
            <p class="pillar-desc">
              Explore business strategies, evaluate market opportunities, examine stakeholder responses, and assess potential risks before committing real capital and organizational resources.
            </p>
          </div>

          <!-- Pillar 2 -->
          <div class="pillar-card">
            <div class="pillar-top">
              <span class="pillar-level">02 // CREATIVE LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name">Idea Sandbox & Worldbuilding</h4>
            <p class="pillar-desc">
              A generative sandbox for exploring ideas, developing fictional worlds, simulating character interactions, and discovering alternative storylines and creative endings.
            </p>
          </div>

          <!-- Pillar 3 -->
          <div class="pillar-card">
            <div class="pillar-top">
              <span class="pillar-level">03 // RESEARCH LEVEL</span>
              <span class="pillar-dot"></span>
            </div>
            <h4 class="pillar-name">Hypothesis & Complexity</h4>
            <p class="pillar-desc">
              Enable researchers and policy makers to investigate hypotheses, explore non-linear relationships, and generate targeted questions for real-world empirical validation.
            </p>
          </div>
        </div>
      </div>

      <!-- Featured Quote Callout from docx -->
      <div class="quote-card">
        <div class="quote-symbol">“</div>
        <p class="quote-body">
          Every possibility begins with a question. OBMIND helps you explore what comes next.
        </p>
        <div class="quote-author">
          <span class="author-name">OBMIND by Obrive Industries</span>
          <span class="author-tag">Predictive Intelligence Architecture</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-about {
  padding: 120px 24px;
  background: #070b0e;
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px;
  background: rgba(7, 65, 57, 0.3);
  border: 1px solid rgba(0, 229, 163, 0.2);
  border-radius: 9999px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #00E5A3;
  margin-bottom: 20px;
}

.pill-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  font-weight: 800;
  color: #ffffff;
  line-height: 1.15;
  margin: 0;
}

.gradient-text {
  background: linear-gradient(135deg, #00E5A3 0%, #a2f1df 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.narrative-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 70px;
}

.narrative-lead {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #ffffff;
  font-weight: 600;
  margin: 0 0 18px 0;
}

.narrative-text {
  font-size: 1.05rem;
  line-height: 1.65;
  color: #94a3b8;
  margin: 0 0 18px 0;
}

.narrative-highlight {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #00E5A3;
  padding: 16px 20px;
  background: rgba(7, 65, 57, 0.2);
  border-left: 3px solid #00E5A3;
  border-radius: 0 10px 10px 0;
  margin: 0;
}

.vision-wrapper {
  background: rgba(12, 18, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 48px;
  margin-bottom: 60px;
  backdrop-filter: blur(14px);
}

.vision-header {
  max-width: 860px;
  margin-bottom: 40px;
}

.vision-eyebrow {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: #00E5A3;
}

.vision-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(1.4rem, 2.5vw, 1.9rem);
  font-weight: 700;
  color: #ffffff;
  line-height: 1.35;
  margin: 12px 0 0 0;
}

.pillars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.pillar-card {
  background: rgba(7, 11, 14, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.pillar-card:hover {
  border-color: rgba(0, 229, 163, 0.3);
  transform: translateY(-3px);
}

.pillar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.pillar-level {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #00E5A3;
  letter-spacing: 1px;
}

.pillar-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
}

.pillar-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
}

.pillar-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0;
}

.quote-card {
  position: relative;
  background: linear-gradient(135deg, rgba(7, 65, 57, 0.4) 0%, rgba(12, 18, 22, 0.9) 100%);
  border: 1px solid rgba(0, 229, 163, 0.3);
  border-radius: 18px;
  padding: 40px 48px;
  text-align: center;
  overflow: hidden;
}

.quote-symbol {
  font-size: 4rem;
  color: rgba(0, 229, 163, 0.2);
  line-height: 1;
  margin-bottom: -20px;
}

.quote-body {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(1.3rem, 2.4vw, 1.8rem);
  font-weight: 600;
  color: #ffffff;
  max-width: 820px;
  margin: 0 auto 20px;
  line-height: 1.4;
}

.quote-author {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #00E5A3;
  letter-spacing: 1px;
}

.author-tag {
  font-size: 0.8rem;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

@media (max-width: 900px) {
  .narrative-grid,
  .pillars-grid {
    grid-template-columns: 1fr;
  }

  .vision-wrapper {
    padding: 28px 20px;
  }

  .quote-card {
    padding: 30px 20px;
  }
}
</style>
