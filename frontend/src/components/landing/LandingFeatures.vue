<template>
  <section id="features" class="features-section">
    <div class="orb orb-1" aria-hidden="true"></div>
    <div class="container-main relative z-[2]">
      <div class="sec-header">
        <h2 class="sec-title">How BRAIN Works</h2>
        <p class="sec-subtitle">
          <span class="block">Built for universality and end-to-end automation.</span>
          <span class="block text-gray-500">Compatible with virtually any analytical prediction task.</span>
        </p>
      </div>

      <div class="feat-grid">
        <div
          v-for="(card, p) in features"
          :key="card.step"
          class="feat-card group relative overflow-hidden rounded-2xl w-full"
          :style="getSpotlightStyle(p)"
          @mousemove="handleMouseMove($event, p)"
          @mouseleave="handleMouseLeave(p)"
        >
          <div class="spot" aria-hidden="true"></div>
          <div class="border-glow" aria-hidden="true"></div>

          <!-- Blurred Watermark Icon -->
          <div class="feat-icon-bg" aria-hidden="true">
            <svg v-if="card.icon === 'graph'" class="w-20 h-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <circle cx="5" cy="6" r="2" stroke-width="1.5" />
              <circle cx="19" cy="6" r="2" stroke-width="1.5" />
              <circle cx="12" cy="12" r="2" stroke-width="1.5" />
              <circle cx="5" cy="18" r="2" stroke-width="1.5" />
              <circle cx="19" cy="18" r="2" stroke-width="1.5" />
              <path stroke-linecap="round" stroke-width="1.5" d="M7 6h10M6.5 7.5L10.5 11M17.5 7.5L13.5 11M6.5 16.5L10.5 13M17.5 16.5L13.5 13" />
            </svg>

            <svg v-else-if="card.icon === 'users'" class="w-20 h-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>

            <svg v-else-if="card.icon === 'play'" class="w-20 h-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>

            <svg v-else-if="card.icon === 'report'" class="w-20 h-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>

            <svg v-else class="w-20 h-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>

          <!-- Step Number -->
          <div class="relative text-[#2d554c] font-michroma text-xs tracking-wider mb-4 group-hover:text-[#073933] transition-colors">
            {{ card.step }}
          </div>

          <!-- Title -->
          <h3 class="relative text-xl font-semibold text-[#073933] mb-2 font-microgramma">
            {{ card.title }}
          </h3>

          <!-- Description -->
          <p class="relative text-[#163830] text-sm leading-relaxed">
            {{ card.description }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive } from 'vue'

const features = [
  {
    step: '01',
    title: 'Scenario Definition',
    description: 'Seed Information Ingestion & Entity Relationship Extraction & GraphRAG Construction',
    icon: 'graph'
  },
  {
    step: '02',
    title: 'Environment Setup',
    description: 'Agent Persona Synthesis & Simulation Parameter Configuration & Memory Space Allocation',
    icon: 'users'
  },
  {
    step: '03',
    title: 'Run Simulation',
    description: 'Parallel Multi-Agent Swarm Simulation & Scenario Forecasting & Dynamic Temporal Updates',
    icon: 'play'
  },
  {
    step: '04',
    title: 'Report Generation',
    description: 'Structured Intelligence Synthesis & Strategic Risk Assessment & Multidimensional Trajectory Analysis',
    icon: 'report'
  },
  {
    step: '05',
    title: 'Deep Exploration',
    description: 'Interactive Scenario Exploration & Post-Simulation Deep Dive & Decision Stress-Testing',
    icon: 'chat'
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
  const s = spots[index]
  if (!s) return {}
  return {
    '--spot-x': `${s.x}px`,
    '--spot-y': `${s.y}px`
  }
}
</script>

<style scoped>
.features-section {
  position: relative;
  z-index: 10;
  background-color: transparent;
  overflow: hidden;
  padding-top: 70px;
  padding-bottom: 70px;
  box-sizing: border-box;
}

.sec-header {
  text-align: center;
  margin-bottom: 3rem;
}

.sec-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif !important;
  font-size: 2.75rem;
  line-height: 1.15;
  font-weight: 700;
  color: #073933;
  margin-bottom: 1.25rem;
  letter-spacing: -0.02em;
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
  color: #163830;
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
  width: 360px;
  height: 200px;
  border-radius: 50%;
  background: #34d39914;
  filter: blur(60px);
  top: 25%;
  left: 10%;
  transform: rotate(8deg);
  animation: drift-f1 22s ease-in-out infinite;
}

@keyframes drift-f1 {
  0%, 100% { transform: rotate(8deg) translate(0); }
  50% { transform: rotate(8deg) translate(30px, -15px); }
}

.feat-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
  justify-items: center;
}

@media (min-width: 768px) {
  .feat-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .feat-grid > :last-child:nth-child(odd) {
    grid-column: 1 / -1;
    max-width: calc(50% - 0.625rem);
  }
}

@media (min-width: 1024px) {
  .feat-grid {
    grid-template-columns: repeat(5, 1fr);
  }
  .feat-grid > :last-child:nth-child(odd) {
    grid-column: auto;
    max-width: none;
  }
}

.feat-card {
  --spot-x: 50%;
  --spot-y: 50%;
  padding: 1.5rem;
  border: 1px solid rgba(10, 28, 23, 0.12);
  background: rgba(255, 255, 255, 0.45);
  -webkit-backdrop-filter: blur(16px) saturate(1.2);
  backdrop-filter: blur(16px) saturate(1.2);
  min-height: 230px;
  display: flex;
  flex-direction: column;
  transition: border-color 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.feat-card:hover {
  border-color: rgba(10, 28, 23, 0.25);
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 12px 28px -6px rgba(10, 28, 23, 0.1);
}

.spot {
  position: absolute;
  inset: 0;
  opacity: 0;
  background: radial-gradient(200px circle at var(--spot-x) var(--spot-y), rgba(255, 255, 255, 0.6), transparent 60%);
  transition: opacity 0.3s;
  pointer-events: none;
}

.feat-card:hover .spot {
  opacity: 1;
}

.border-glow {
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  opacity: 0;
  background: radial-gradient(250px circle at var(--spot-x) var(--spot-y), rgba(255, 255, 255, 0.8), transparent 50%);
  transition: opacity 0.3s;
  pointer-events: none;
  -webkit-mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  mask-composite: exclude;
  padding: 1px;
}

.feat-card:hover .border-glow {
  opacity: 1;
}

.feat-icon-bg {
  position: absolute;
  top: 10px;
  right: 10px;
  color: rgba(10, 28, 23, 0.08);
  filter: blur(2px);
  transition: color 0.35s ease, filter 0.35s ease;
  pointer-events: none;
  z-index: 0;
}

.feat-card:hover .feat-icon-bg {
  color: rgba(10, 28, 23, 0.16);
  filter: blur(1.5px);
}
</style>
