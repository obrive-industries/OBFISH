<template>
  <section class="section-workflow" id="workflow">
    <div class="container">
      <div class="section-header">
        <div class="category-pill">
          <span class="pill-dot"></span>
          WORKFLOW ENGINE
        </div>

        <h2 class="section-title">
          How OBMIND Works
        </h2>

        <p class="section-sub">
          Don't just predict what might happen. Explore why it could happen.
        </p>
      </div>

      <!-- 5 Step Cards with Connector Flow -->
      <div class="steps-flow">
        <div 
          v-for="(step, index) in steps" 
          :key="step.number"
          class="step-card"
          :class="{ 'active': activeStep === index }"
          @mouseenter="activeStep = index"
        >
          <div class="step-card-header">
            <span class="step-num">{{ step.number }}</span>
            <span class="step-tag">{{ step.tag }}</span>
          </div>

          <h3 class="step-title">{{ step.title }}</h3>

          <p class="step-body">
            {{ step.description }}
          </p>

          <div class="step-indicator">
            <span class="indicator-bar"></span>
          </div>
        </div>
      </div>

      <!-- Interactive Step Summary Bar -->
      <div class="workflow-cta-banner">
        <div class="cta-left">
          <span class="cta-badge">EXPLORATION READY</span>
          <p class="cta-text">Turn your dossier or hypothesis into a 5-step simulation in seconds.</p>
        </div>
        <router-link to="/console" class="btn-launch-step">
          Launch Engine Now →
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const activeStep = ref(0)

const steps = [
  {
    number: '01',
    tag: 'SOURCE & SEED',
    title: 'Define Your Scenario',
    description: 'Start with a question, business challenge, research document, market report, policy proposal, or other relevant source material. Describe what you want to explore and the decision you need to make.'
  },
  {
    number: '02',
    tag: 'ONTOLOGY & GRAPH',
    title: 'Build the Simulation',
    description: 'The platform organises relevant information, identifies key entities and relationships, and prepares simulated stakeholders with different roles, goals, and perspectives.'
  },
  {
    number: '03',
    tag: 'MULTI-AGENT SWARM',
    title: 'Simulate Possible Outcomes',
    description: 'Run interactions between AI agents in a virtual environment to explore how opinions, decisions, and relationships could evolve under your chosen assumptions.'
  },
  {
    number: '04',
    tag: 'INTELLIGENCE REPORT',
    title: 'Analyse the Results',
    description: 'Review a structured report containing possible outcome paths, stakeholder reactions, emerging risks, important assumptions, and strategic considerations.'
  },
  {
    number: '05',
    tag: 'DEEP INTERACTION',
    title: 'Explore Further',
    description: 'Ask follow-up questions, investigate alternative scenarios, adjust assumptions, and compare how different decisions could change the simulated outcome.'
  }
]
</script>

<style scoped>
.section-workflow {
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
  max-width: 760px;
  margin: 0 auto 64px;
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
  margin: 0 0 16px 0;
}

.section-sub {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0;
}

.steps-flow {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 60px;
}

.step-card {
  background: rgba(12, 18, 22, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  backdrop-filter: blur(12px);
}

.step-card:hover,
.step-card.active {
  border-color: rgba(0, 229, 163, 0.4);
  background: rgba(12, 18, 22, 0.9);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 229, 163, 0.1);
}

.step-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.8rem;
  font-weight: 800;
  color: #00E5A3;
}

.step-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #64748b;
  letter-spacing: 0.5px;
}

.step-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.12rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.step-body {
  font-size: 0.88rem;
  line-height: 1.55;
  color: #94a3b8;
  margin: 0 0 20px 0;
  flex: 1;
}

.step-indicator {
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.indicator-bar {
  display: block;
  height: 100%;
  width: 0%;
  background: #00E5A3;
  transition: width 0.3s ease;
}

.step-card:hover .indicator-bar,
.step-card.active .indicator-bar {
  width: 100%;
}

.workflow-cta-banner {
  background: linear-gradient(135deg, rgba(7, 65, 57, 0.4) 0%, rgba(12, 18, 22, 0.8) 100%);
  border: 1px solid rgba(0, 229, 163, 0.25);
  border-radius: 14px;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(16px);
}

.cta-left {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cta-badge {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #00E5A3;
}

.cta-text {
  font-size: 1.05rem;
  color: #e2e8f0;
  font-weight: 500;
  margin: 0;
}

.btn-launch-step {
  background: #00E5A3;
  color: #070b0e;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.btn-launch-step:hover {
  background: #a2f1df;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 229, 163, 0.35);
}

@media (max-width: 1100px) {
  .steps-flow {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .steps-flow {
    grid-template-columns: 1fr;
  }

  .workflow-cta-banner {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
