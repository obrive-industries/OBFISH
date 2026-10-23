<template>
  <section class="section-uncertainty">
    <div class="container">
      <!-- Section Header -->
      <div class="section-header">
        <div class="category-pill">
          <span class="pill-dot"></span>
          DECISION DYNAMICS
        </div>

        <h2 class="section-title">
          The Future Is Uncertain.<br />
          <span class="gradient-text">Your Decisions Don’t Have to Be Blind.</span>
        </h2>

        <p class="section-lead">
          Traditional planning often relies on historical data, assumptions, and individual opinions. But real-world outcomes are shaped by multiple people, competing interests, changing conditions, and unexpected reactions.
        </p>

        <p class="section-highlight">
          <strong>Obmind</strong> is designed to help you explore these complexities in a controlled virtual environment.
        </p>
      </div>

      <!-- Comparison Showcase: Traditional vs OBMIND Multi-Agent Swarm -->
      <div class="comparison-grid">
        <!-- Card 1: Traditional Planning -->
        <div class="comparison-card traditional">
          <div class="card-badge danger">TRADITIONAL PLANNING</div>
          <h3 class="card-title">Static Historical Models</h3>
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
              <span class="blindspot-tag">Critical Blindspots Ignored</span>
            </div>
          </div>

          <ul class="feature-list">
            <li><span class="icon red">✕</span> Single-thread assumptions</li>
            <li><span class="icon red">✕</span> Ignores stakeholder psychological reactions</li>
            <li><span class="icon red">✕</span> High cost of failure in production</li>
          </ul>
        </div>

        <!-- Card 2: OBMIND Multi-Agent Simulation -->
        <div class="comparison-card obmind">
          <div class="card-badge success">OBMIND SIMULATION</div>
          <h3 class="card-title">Virtual Emergent Complexity</h3>
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
                <line x1="60" y1="90" :x2="activeScenario === 'shock' ? '180' : '170'" :y2="activeScenario === 'shift' ? '50' : '70'" stroke="rgba(0, 229, 163, 0.4)" stroke-width="1.5" stroke-dasharray="3,3" />
                <line x1="60" y1="90" x2="170" y2="120" stroke="rgba(0, 229, 163, 0.4)" stroke-width="1.5" />
                <line :x1="activeScenario === 'shock' ? '180' : '170'" :y1="activeScenario === 'shift' ? '50' : '70'" x2="310" :y2="activeScenario === 'shock' ? '130' : '85'" stroke="#00E5A3" stroke-width="2" />
                <line x1="170" y1="120" x2="310" :y2="activeScenario === 'shock' ? '130' : '85'" stroke="#00E5A3" stroke-width="2" />
                <line x1="310" :y1="activeScenario === 'shock' ? '130' : '85'" x2="370" y2="90" stroke="#10b981" stroke-width="2.5" />

                <!-- Nodes -->
                <!-- Scenario Origin -->
                <circle cx="60" cy="90" r="8" fill="#074139" stroke="#00E5A3" stroke-width="2" />
                <text x="60" y="112" fill="#94a3b8" font-size="9" text-anchor="middle">Question</text>

                <!-- Agent Nodes -->
                <circle :cx="activeScenario === 'shock' ? 180 : 170" :cy="activeScenario === 'shift' ? 50 : 70" r="10" fill="#0c1216" stroke="#00E5A3" stroke-width="2" />
                <text :x="activeScenario === 'shock' ? 180 : 170" :y="activeScenario === 'shift' ? 44 : 64" fill="#00E5A3" font-size="8" text-anchor="middle">Agent A</text>

                <circle cx="170" cy="120" r="10" fill="#0c1216" stroke="#00E5A3" stroke-width="2" />
                <text x="170" y="138" fill="#00E5A3" font-size="8" text-anchor="middle">Agent B</text>

                <!-- Emergent Outcome -->
                <circle cx="310" :cy="activeScenario === 'shock' ? 130 : 85" r="12" fill="#074139" stroke="#00E5A3" stroke-width="2.5" />
                <text x="310" :y="activeScenario === 'shock' ? 152 : 72" fill="#ffffff" font-weight="bold" font-size="9" text-anchor="middle">
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

const activeScenario = ref('base')
</script>

<style scoped>
.section-uncertainty {
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
  max-width: 820px;
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
  font-size: clamp(2rem, 3.8vw, 3rem);
  font-weight: 700;
  line-height: 1.15;
  color: #ffffff;
  margin: 0 0 20px 0;
}

.gradient-text {
  background: linear-gradient(135deg, #00E5A3 0%, #a2f1df 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-lead {
  font-size: 1.1rem;
  line-height: 1.65;
  color: #94a3b8;
  margin: 0 0 16px 0;
}

.section-highlight {
  font-size: 1.15rem;
  line-height: 1.6;
  color: #e2e8f0;
  margin: 0;
}

.section-highlight strong {
  color: #00E5A3;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1.25fr;
  gap: 32px;
  align-items: stretch;
}

.comparison-card {
  background: rgba(12, 18, 22, 0.6);
  border-radius: 18px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}

.comparison-card.traditional {
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.comparison-card.obmind {
  border: 1px solid rgba(0, 229, 163, 0.3);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 229, 163, 0.08);
  background: rgba(12, 18, 22, 0.85);
}

.card-badge {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 4px 10px;
  border-radius: 6px;
  width: fit-content;
  margin-bottom: 16px;
}

.card-badge.danger {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.card-badge.success {
  background: rgba(0, 229, 163, 0.15);
  color: #00E5A3;
  border: 1px solid rgba(0, 229, 163, 0.3);
}

.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
}

.card-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #94a3b8;
  margin: 0 0 24px 0;
}

.model-visual {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.linear-visual {
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.linear-line {
  position: relative;
  width: 80%;
  height: 3px;
  background: linear-gradient(90deg, #94a3b8, #ef4444);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.point {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #94a3b8;
}

.danger-point {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #ef4444;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.linear-legend {
  margin-top: 20px;
}

.blindspot-tag {
  font-size: 0.75rem;
  color: #f87171;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(239, 68, 68, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.swarm-visual {
  position: relative;
}

.interactive-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.sim-toggle-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sim-toggle-btn.active {
  background: rgba(0, 229, 163, 0.15);
  border-color: #00E5A3;
  color: #00E5A3;
}

.agent-graph-box {
  height: 150px;
}

.graph-svg {
  width: 100%;
  height: 100%;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: auto 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #cbd5e1;
}

.icon {
  font-size: 0.85rem;
  font-weight: bold;
}

.icon.red { color: #f87171; }
.icon.green { color: #00E5A3; }

@media (max-width: 900px) {
  .comparison-grid {
    grid-template-columns: 1fr;
  }
}
</style>
