<template>
  <section class="section-uncertainty" id="uncertainty">
    <div class="container">
      <!-- Section Header with Obrive 3-Ball Badge -->
      <div class="section-header">
        <div class="category-pill">
          <RoundedBallIcon :width="14" :height="20" />
          <span class="pill-text font-microgramma">DECISION DYNAMICS</span>
        </div>

        <h2 class="section-title font-microgramma">
          The Future Is Uncertain.<br />
          <span class="title-accent">Your Decisions Don’t Have to Be Blind.</span>
        </h2>

        <p class="section-lead">
          Traditional planning often relies on historical data, assumptions, and individual opinions. But real-world outcomes are shaped by multiple people, competing interests, changing conditions, and unexpected reactions.
        </p>

        <p class="section-highlight">
          <strong>Brain</strong> is designed to help you explore these complexities in a controlled virtual environment.
        </p>
      </div>

      <!-- Comparison Showcase: Traditional vs BRAIN Multi-Agent Swarm -->
      <div class="comparison-grid">
        <!-- Card 1: Traditional Planning -->
        <div class="comparison-card traditional">
          <div class="card-badge danger font-microgramma">TRADITIONAL PLANNING</div>
          <h3 class="card-title font-microgramma">Static Historical Models</h3>
          <p class="card-desc">
            Linear projections assume static conditions. When unforeseen public sentiment or market shocks arrive, decisions become reactive and vulnerable.
          </p>

          <div class="model-visual linear-visual">
            <div class="linear-line">
              <span class="point p1" title="Initial Assumption"></span>
              <span class="point p2" title="Linear Forecast"></span>
              <span class="point p3 danger-point" title="Critical Blindspot">✕</span>
            </div>
            <div class="linear-legend">
              <span class="blindspot-tag font-microgramma">Critical Blindspots Ignored</span>
            </div>
          </div>

          <ul class="feature-list">
            <li><span class="icon red">✕</span> Single-thread assumptions</li>
            <li><span class="icon red">✕</span> Ignores stakeholder psychological reactions</li>
            <li><span class="icon red">✕</span> High cost of failure in production</li>
          </ul>
        </div>

        <!-- Card 2: BRAIN Multi-Agent Simulation -->
        <div class="comparison-card brain obmind">
          <div class="card-badge success font-microgramma">BRAIN SIMULATION</div>
          <h3 class="card-title font-microgramma">Virtual Emergent Complexity</h3>
          <p class="card-desc">
            Autonomous AI digital twin agents simulate hundreds of interactions, surfacing hidden risks, consensus tipping points, and resilient decision paths.
          </p>

          <!-- Interactive Simulation Sandbox Preview -->
          <div class="model-visual swarm-visual">
            <div class="interactive-controls">
              <button 
                :class="['sim-toggle-btn', { active: activeScenario === 'base' }]"
                @click="activeScenario = 'base'"
              >
                Base Trajectory
              </button>
              <button 
                :class="['sim-toggle-btn', { active: activeScenario === 'shock' }]"
                @click="activeScenario = 'shock'"
              >
                Market Shock
              </button>
              <button 
                :class="['sim-toggle-btn', { active: activeScenario === 'shift' }]"
                @click="activeScenario = 'shift'"
              >
                Sentiment Shift
              </button>
            </div>

            <div class="agent-graph-box">
              <svg viewBox="0 0 400 180" class="graph-svg">
                <!-- Links -->
                <line x1="60" y1="90" :x2="activeScenario === 'shock' ? '180' : '170'" :y2="activeScenario === 'shift' ? '50' : '70'" stroke="rgba(255, 255, 255, 0.35)" stroke-width="1.5" stroke-dasharray="3,3" />
                <line x1="60" y1="90" x2="170" y2="120" stroke="rgba(255, 255, 255, 0.35)" stroke-width="1.5" />
                <line :x1="activeScenario === 'shock' ? '180' : '170'" :y1="activeScenario === 'shift' ? '50' : '70'" x2="310" :y2="activeScenario === 'shock' ? '130' : '85'" stroke="#ffffff" stroke-width="2" />
                <line x1="170" y1="120" x2="310" :y2="activeScenario === 'shock' ? '130' : '85'" stroke="#ffffff" stroke-width="2" />
                <line x1="310" :y1="activeScenario === 'shock' ? '130' : '85'" x2="370" y2="90" stroke="#00E5A3" stroke-width="2.5" />

                <!-- Nodes -->
                <!-- Scenario Origin -->
                <circle cx="60" cy="90" r="9" fill="#ffffff" />
                <text x="60" y="112" fill="#ffffff" font-size="9" font-weight="600" text-anchor="middle">Question</text>

                <!-- Agent Nodes -->
                <circle :cx="activeScenario === 'shock' ? 180 : 170" :cy="activeScenario === 'shift' ? 50 : 70" r="10" fill="#27272a" stroke="#ffffff" stroke-width="2" />
                <text :x="activeScenario === 'shock' ? 180 : 170" :y="activeScenario === 'shift' ? 44 : 64" fill="#ffffff" font-size="8" font-weight="700" text-anchor="middle">Agent A</text>

                <circle cx="170" cy="120" r="10" fill="#27272a" stroke="#ffffff" stroke-width="2" />
                <text x="170" y="138" fill="#ffffff" font-size="8" font-weight="700" text-anchor="middle">Agent B</text>

                <!-- Emergent Outcome -->
                <circle cx="310" :cy="activeScenario === 'shock' ? 130 : 85" r="13" fill="#00E5A3" stroke="#ffffff" stroke-width="2.5" />
                <text x="310" :y="activeScenario === 'shock' ? 152 : 70" fill="#00E5A3" font-weight="bold" font-size="9" text-anchor="middle">
                  {{ activeScenario === 'shock' ? 'Risk Mitigated' : (activeScenario === 'shift' ? 'Consensus' : 'Optimal Path') }}
                </text>
              </svg>
            </div>
          </div>

          <ul class="feature-list">
            <li><span class="icon green">✓</span> Hundreds of simulated agent conversations</li>
            <li><span class="icon green">✓</span> Discovers behavioral tipping points before launch</li>
            <li><span class="icon green">✓</span> Controlled sandbox testing with zero real-world risk</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import RoundedBallIcon from '../common/RoundedBallIcon.vue'

const activeScenario = ref('base')
</script>

<style scoped>
.section-uncertainty {
  padding: 120px 24px;
  background: #000000;
  color: #ffffff;
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 840px;
  margin: 0 auto 56px;
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
  line-height: 1.15;
  color: #ffffff;
  margin: 0 0 20px 0;
  letter-spacing: -0.01em;
}

.title-accent {
  color: #9ca3af;
}

.section-lead {
  font-size: 1.05rem;
  line-height: 1.65;
  color: #a1a1aa;
  margin: 0 0 14px 0;
}

.section-highlight {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #ffffff;
  margin: 0;
}

/* Comparison Grid */
.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.comparison-card {
  border-radius: 18px;
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.comparison-card.traditional {
  background: #09090b;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
}

.comparison-card.brain,
.comparison-card.obmind {
  background: #0e0e11;
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 0 12px 35px -5px rgba(0, 0, 0, 0.7);
}

.card-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 5px 12px;
  border-radius: 6px;
  margin-bottom: 16px;
  width: fit-content;
}

.card-badge.danger {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.card-badge.success {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.card-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
}

.card-desc {
  font-size: 0.92rem;
  line-height: 1.6;
  color: #a1a1aa;
  margin: 0 0 24px 0;
}

/* Model Visuals */
.model-visual {
  height: 200px;
  border-radius: 12px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.linear-visual {
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.16);
  padding: 20px;
}

.linear-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  margin: 20px 20px 30px;
}

.linear-line::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-50%);
  z-index: 1;
}

.point {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffffff;
  position: relative;
  z-index: 2;
}

.danger-point {
  background: #ef4444;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
}

.linear-legend {
  text-align: center;
}

.blindspot-tag {
  display: inline-block;
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
  font-size: 10px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
}

/* Swarm Visual */
.swarm-visual {
  background: #000000;
  border: 1px solid rgba(255, 255, 255, 0.14);
  padding: 12px;
}

.interactive-controls {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 8px;
}

.sim-toggle-btn {
  background: #18181b;
  border: 1px solid rgba(255, 255, 255, 0.16);
  color: #9ca3af;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sim-toggle-btn:hover {
  border-color: rgba(255, 255, 255, 0.35);
  color: #ffffff;
}

.sim-toggle-btn.active {
  background: #ffffff;
  color: #000000;
  border-color: #ffffff;
  font-weight: 700;
}

.agent-graph-box {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.graph-svg {
  width: 100%;
  height: 100%;
  max-height: 150px;
}

/* Feature List */
.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.88rem;
  color: #e4e4e7;
  font-weight: 500;
}

.icon {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  flex-shrink: 0;
}

.icon.red {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.icon.green {
  background: rgba(0, 229, 163, 0.15);
  color: #00E5A3;
}

@media (max-width: 860px) {
  .comparison-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>
