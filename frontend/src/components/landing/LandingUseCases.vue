<template>
  <section id="use-cases" class="usecases-section">
    <div class="orb orb-1" aria-hidden="true"></div>
    <div class="orb orb-2" aria-hidden="true"></div>
    <div class="container-main relative z-[2]">
      <div class="sec-header">
        <h2 class="sec-title">
          BRAIN is Built to Explore
        </h2>
        <p class="sec-subtitle">
          <span class="block">From a question to a structured exploration of possibilities</span>
          <span class="block text-gray-500">across all strategic and creative dimensions.</span>
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="(card, index) in useCases"
          :key="card.title"
          class="case-card group relative overflow-hidden rounded-2xl"
          :style="getSpotlightStyle(index)"
          @mousemove="handleMouseMove($event, index)"
          @mouseleave="handleMouseLeave(index)"
        >
          <div class="spot" aria-hidden="true"></div>
          <div class="border-glow" aria-hidden="true"></div>
          <div class="accent" aria-hidden="true"></div>
          <span class="relative block text-xs font-medium text-gray-500 uppercase tracking-widest mb-3">
            {{ card.tag }}
          </span>
          <h3 class="relative text-lg font-semibold text-white mb-2 leading-snug">
            {{ card.title }}
          </h3>
          <p class="relative text-sm text-gray-400 leading-relaxed">
            {{ card.description }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive } from 'vue'

const useCases = [
  {
    title: 'Business Strategy & Decision Intelligence',
    description: 'Simulate customer adoption, competitive dynamics, pricing elasticity, and market shifts before capital deployment.',
    tag: 'Startups / Strategy'
  },
  {
    title: 'Marketing & Brand Intelligence',
    description: 'Simulate customer sentiment reactions to campaigns, launches, pricing models, and narrative positioning.',
    tag: 'Brand / Marketing'
  },
  {
    title: 'Public Opinion & Crisis Rehearsal',
    description: 'Simulate social media propagation, stakeholder reactions, and risk factors to evaluate optimal response strategies.',
    tag: 'Enterprise / PR'
  },
  {
    title: 'Story & Character Deduction',
    description: 'Simulate complex narrative worlds, character relationship evolution, and multi-threaded story trajectories.',
    tag: 'Entertainment / Creative'
  },
  {
    title: 'Policy & Behavioral Simulation',
    description: 'Simulate public responses across diverse demographics before official announcements and policy releases.',
    tag: 'Research / Policy'
  },
  {
    title: 'Financial Decision Support',
    description: 'Simulate market sentiment shifts, investor behavior patterns, and economic scenarios for strategic planning.',
    tag: 'Finance / Investment'
  }
]

const spots = reactive({})

const handleMouseMove = (e, index) => {
  const rect = e.currentTarget.getBoundingClientRect()
  spots[index] = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
}

const handleMouseLeave = (index) => {
  spots[index] = null
}

const getSpotlightStyle = (index) => {
  const spot = spots[index]
  if (!spot) return {}
  return {
    '--spot-x': `${spot.x}px`,
    '--spot-y': `${spot.y}px`
  }
}
</script>

<style scoped>
.usecases-section {
  position: relative;
  z-index: 10;
  background-color: #000000;
  overflow: hidden;
  padding-top: 70px;
  padding-bottom: 80px;
  box-sizing: border-box;
}

.sec-header {
  text-align: center;
  margin-bottom: 3rem;
}

.sec-title {
  font-family: 'Inter', sans-serif;
  font-size: 3rem;
  line-height: 1.15;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1.25rem;
  letter-spacing: -0.025em;
}

@media (max-width: 768px) {
  .sec-title {
    font-size: 2.25rem;
  }
}

.sec-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.25rem;
  line-height: 1.85rem;
  color: #71717a;
  max-width: 44rem;
  margin-left: auto;
  margin-right: auto;
}

.container-main {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container-main {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container-main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.orb {
  position: absolute;
  pointer-events: none;
  z-index: 1;
}

.orb-1 {
  width: 380px;
  height: 200px;
  border-radius: 50%;
  background: #3278f01a;
  filter: blur(60px);
  top: 10%;
  left: 5%;
  transform: rotate(-12deg);
  animation: drift-1 22s ease-in-out infinite;
}

.orb-2 {
  width: 280px;
  height: 180px;
  border-radius: 50%;
  background: #963cdc14;
  filter: blur(55px);
  bottom: 10%;
  right: 8%;
  transform: rotate(18deg);
  animation: drift-2 26s ease-in-out infinite;
}

@keyframes drift-1 {
  0%, 100% { transform: rotate(-12deg) translate(0); }
  50% { transform: rotate(-12deg) translate(35px, -20px); }
}

@keyframes drift-2 {
  0%, 100% { transform: rotate(18deg) translate(0); }
  50% { transform: rotate(18deg) translate(-25px, 18px); }
}

.case-card {
  --spot-x: 50%;
  --spot-y: 50%;
  padding: 1.5rem 1.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #ffffff0a;
  -webkit-backdrop-filter: blur(16px) saturate(1.2);
  backdrop-filter: blur(16px) saturate(1.2);
  min-height: 180px;
  display: flex;
  flex-direction: column;
  transition: border-color 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.case-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: #ffffff0f;
  transform: translateY(-2px);
  box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.4);
}

.spot {
  position: absolute;
  inset: 0;
  opacity: 0;
  background: radial-gradient(320px circle at var(--spot-x) var(--spot-y), rgba(255, 255, 255, 0.08), transparent 60%);
  transition: opacity 0.3s;
  pointer-events: none;
}

.case-card:hover .spot {
  opacity: 1;
}

.border-glow {
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  opacity: 0;
  background: radial-gradient(350px circle at var(--spot-x) var(--spot-y), rgba(255, 255, 255, 0.25), transparent 50%);
  transition: opacity 0.3s;
  pointer-events: none;
  -webkit-mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  mask-composite: exclude;
  padding: 1px;
}

.case-card:hover .border-glow {
  opacity: 1;
}

.accent {
  position: absolute;
  top: 0;
  left: 18%;
  right: 18%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.case-card:hover .accent {
  left: 6%;
  right: 6%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.22), transparent);
}
</style>
