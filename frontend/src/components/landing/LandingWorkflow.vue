<template>
  <section class="section-workflow" id="workflow">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">WORKFLOW ENGINE</span>
        </div>

        <h2 class="section-title font-microgramma">
          How BRAIN Works
        </h2>

        <p class="section-sub">
          Don't just predict what might happen. Explore why it could happen.
        </p>
      </div>

      <!-- 5 Step Cards with Obrive Cell Interaction -->
      <div class="steps-flow">
        <div 
          v-for="(step, index) in steps" 
          :key="step.number"
          class="step-card obrive-cell"
          :class="{ 'is-active': activeStep === index }"
          @mouseenter="activeStep = index"
        >
          <div class="step-card-header">
            <span class="step-num font-microgramma">{{ step.number }}</span>
            <span class="step-tag font-microgramma">{{ step.tag }}</span>
          </div>

          <h3 class="step-title font-microgramma">{{ step.title }}</h3>

          <p class="step-body">
            {{ step.description }}
          </p>

          <div class="step-indicator">
            <span class="indicator-bar" :class="{ 'bar-active': activeStep === index }"></span>
          </div>
        </div>
      </div>

      <!-- Obrive Pre-Action CTA Banner -->
      <div class="workflow-cta-banner">
        <div class="cta-left">
          <span class="cta-badge font-microgramma">EXPLORATION READY</span>
          <p class="cta-text">Turn your question, dossier, or hypothesis into a 5-step predictive simulation in seconds.</p>
        </div>
        <AnimatedButton
          to="/console"
          variant="primary"
          size="default"
          :iconSize="14"
        >
          Launch Engine Now
        </AnimatedButton>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import AnimatedButton from '../common/AnimatedButton.vue'
import RoundedBallIcon from '../common/RoundedBallIcon.vue'

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
  background: #000000;
  color: #ffffff;
  position: relative;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 820px;
  margin: 0 auto 60px;
}

.category-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 9999px;
  margin-bottom: 20px;
}

.pill-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #ffffff;
}

.section-title {
  font-size: clamp(2.2rem, 3.8vw, 3.2rem);
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  letter-spacing: -0.01em;
}

.section-sub {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #9ca3af;
  margin: 0;
  font-weight: 450;
}

/* Steps Flow */
.steps-flow {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
  margin-bottom: 48px;
}

.step-card {
  background: #09090b;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 320px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.step-card.is-active,
.step-card:hover {
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow: 0 10px 30px -4px rgba(0, 0, 0, 0.6);
  transform: translateY(-2px);
}

.step-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.step-num {
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  opacity: 0.9;
  line-height: 1;
  transition: color 0.3s ease;
}

.step-tag {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.step-card:hover .step-num {
  color: #ffffff !important;
}

.step-card:hover .step-tag {
  background: rgba(255, 255, 255, 0.16);
  color: #ffffff !important;
}

.step-title {
  font-size: 1.08rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.step-body {
  font-size: 0.86rem;
  line-height: 1.6;
  color: #a1a1aa;
  margin: 0 0 20px 0;
  flex: 1;
}

.step-card:hover .step-body {
  color: #d1d5db;
}

.step-indicator {
  height: 3px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  overflow: hidden;
}

.indicator-bar {
  display: block;
  height: 100%;
  width: 0;
  background: #ffffff;
  transition: width 0.3s ease;
}

.indicator-bar.bar-active {
  width: 100%;
}

/* Workflow Bottom Banner */
.workflow-cta-banner {
  background: #0d0d10;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.cta-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.cta-badge {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 6px 12px;
  border-radius: 6px;
}

.cta-text {
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0;
}

/* Responsive */
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
    align-items: flex-start;
  }
}
</style>
