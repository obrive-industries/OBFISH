<template>
  <section id="decision-dynamics" class="py-24 bg-black relative z-10 overflow-hidden">
    <!-- Ambient Aurora Glow Orbs -->
    <div class="ambient-orb orb-left" aria-hidden="true"></div>
    <div class="ambient-orb orb-right" aria-hidden="true"></div>

    <div class="container-main relative z-[2] max-w-6xl mx-auto px-6">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs font-mono uppercase tracking-widest text-gray-400 mb-4">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Decision Dynamics</span>
        </div>
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
          Simulate Before You Commit
        </h2>
        <p class="text-gray-400 max-w-2xl mx-auto mt-4 text-base md:text-lg leading-relaxed">
          Navigate emergent complexity by testing every strategic assumption against an autonomous multi-agent swarm.
        </p>
      </div>

      <!-- Two-Column Showcase Layout (Screenshot Style) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <!-- Left Column: 2 Interactive Decision Blocks -->
        <div class="lg:col-span-5 flex flex-col gap-6">
          <!-- Box 1: The Future Is Uncertain -->
          <div
            class="decision-card group relative p-6 sm:p-7 rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeCard === 1 ? 'is-active' : 'is-idle'"
            @click="activeCard = 1"
          >
            <div class="card-glow" aria-hidden="true"></div>
            <div class="flex items-start gap-4 relative z-[2]">
              <div class="step-badge shrink-0">
                <span>1</span>
              </div>
              <div class="flex-1">
                <h3 class="text-lg sm:text-xl font-bold text-white mb-2 group-hover:text-amber-300 transition-colors">
                  The Future Is Uncertain
                </h3>
                <p class="text-sm sm:text-base text-gray-400 leading-relaxed">
                  Traditional planning often relies on historical data, assumptions, and individual opinions.
                </p>
              </div>
            </div>
          </div>

          <!-- Box 2: Your Decisions Don't Have to Be Blind -->
          <div
            class="decision-card group relative p-6 sm:p-7 rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeCard === 2 ? 'is-active' : 'is-idle'"
            @click="activeCard = 2"
          >
            <div class="card-glow" aria-hidden="true"></div>
            <div class="flex items-start gap-4 relative z-[2]">
              <div class="step-badge shrink-0">
                <span>2</span>
              </div>
              <div class="flex-1">
                <h3 class="text-lg sm:text-xl font-bold text-white mb-2 group-hover:text-cyan-300 transition-colors">
                  Your Decisions Don’t Have to Be Blind.
                </h3>
                <p class="text-sm sm:text-base text-gray-400 leading-relaxed">
                  But real-world outcomes are shaped by multiple people, competing interests, changing conditions, and unexpected reactions.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Cosmic Galaxy Brain Artwork Frame -->
        <div class="lg:col-span-7 flex justify-center">
          <div class="brain-frame-wrapper relative w-full max-w-xl group">
            <!-- Behind-frame Ambient Holographic Aura -->
            <div class="frame-backdrop-glow" aria-hidden="true"></div>

            <div class="brain-media-frame relative rounded-2xl overflow-hidden border border-white/15 bg-white/[0.02] backdrop-blur-xl shadow-2xl">
              <!-- Top Tech Header Bar -->
              <div class="tech-bar flex items-center justify-between px-4 py-3 bg-white/[0.04] border-b border-white/10 text-xs font-mono text-gray-400">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-red-500/80"></span>
                  <span class="w-2.5 h-2.5 rounded-full bg-yellow-500/80"></span>
                  <span class="w-2.5 h-2.5 rounded-full bg-green-500/80"></span>
                  <span class="ml-2 text-gray-300 font-semibold tracking-wider">BRAIN SWARM SIMULATOR</span>
                </div>
                <div class="flex items-center gap-2 text-[11px] text-gray-400">
                  <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                  <span>ONLINE // 100+ AGENTS</span>
                </div>
              </div>

              <!-- Main Image Display -->
              <div class="relative aspect-[4/3] sm:aspect-[16/11] overflow-hidden bg-black flex items-center justify-center">
                <img
                  src="/images/cosmic-brain.jpg"
                  alt="Brain Swarm Intelligence Cosmic Core"
                  class="w-full h-full object-cover object-center transition-transform duration-700 ease-out group-hover:scale-105"
                  loading="lazy"
                />

                <!-- Subtle Sci-Fi Grid Overlay -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 pointer-events-none"></div>

                <!-- Floating Bottom HUD Metadata Pill -->
                <div class="absolute bottom-4 left-4 right-4 flex items-center justify-between px-4 py-2.5 rounded-xl bg-black/60 backdrop-blur-md border border-white/15 text-xs text-gray-300">
                  <div class="flex items-center gap-2">
                    <span class="font-mono text-cyan-400">STATUS:</span>
                    <span class="font-semibold text-white">Active Predictive Simulation</span>
                  </div>
                  <div class="hidden sm:flex items-center gap-3 font-mono text-[11px] text-gray-400">
                    <span>EPOCH: T+0</span>
                    <span class="text-white/30">|</span>
                    <span>CONFIDENCE: 94.8%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const activeCard = ref(1)
</script>

<style scoped>
.ambient-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(90px);
  z-index: 1;
}

.orb-left {
  width: 400px;
  height: 350px;
  background: radial-gradient(circle, rgba(234, 160, 40, 0.12) 0%, rgba(234, 160, 40, 0) 70%);
  top: 15%;
  left: -5%;
}

.orb-right {
  width: 450px;
  height: 400px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.14) 0%, rgba(56, 189, 248, 0) 70%);
  bottom: 10%;
  right: -5%;
}

.decision-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  overflow: hidden;
}

.decision-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.decision-card.is-active {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.28);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.step-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', 'Space Grotesk', monospace;
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  transition: all 0.3s ease;
}

.decision-card.is-active .step-badge {
  background: #ffffff;
  color: #000000;
  box-shadow: 0 0 14px rgba(255, 255, 255, 0.5);
}

.card-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.06), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.decision-card:hover .card-glow,
.decision-card.is-active .card-glow {
  opacity: 1;
}

.frame-backdrop-glow {
  position: absolute;
  inset: -15px;
  border-radius: 2rem;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, rgba(249, 115, 22, 0.18) 50%, transparent 75%);
  filter: blur(24px);
  opacity: 0.6;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

.brain-frame-wrapper:hover .frame-backdrop-glow {
  opacity: 0.9;
}
</style>
