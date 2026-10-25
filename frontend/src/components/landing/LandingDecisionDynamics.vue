<template>
  <section id="decision-dynamics" class="decision-section py-20 bg-black relative z-10 overflow-hidden">
    <!-- Ambient Glow Orb -->
    <div class="orb orb-1" aria-hidden="true"></div>

    <div class="container-main relative z-[2]">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <p class="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4">Decision Dynamics</p>
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">Simulate Before You Commit</h2>
        <p class="text-gray-400 max-w-2xl mx-auto text-base md:text-lg leading-relaxed">
          Navigate emergent complexity by testing every strategic assumption against an autonomous multi-agent swarm.
        </p>
      </div>

      <!-- Side-by-Side Flex Layout (Exact match with reference screenshot) -->
      <div class="decision-row flex flex-col md:flex-row gap-8 max-w-5xl mx-auto items-stretch">
        <!-- Left Side: 2 Decision Blocks -->
        <div class="decision-col-left md:w-[38%] flex flex-col justify-between gap-5">
          <!-- Box 1: The Future Is Uncertain -->
          <div
            class="video-btn text-left rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeIdx === 0 ? 'is-active' : 'is-idle'"
            @click="activeIdx = 0"
          >
            <div class="flex items-start gap-4">
              <span
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-mono shrink-0 mt-0.5"
                :class="activeIdx === 0 ? 'bg-white/10 text-white font-semibold' : 'bg-white/5 text-gray-500'"
              >
                1
              </span>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-white text-base sm:text-lg leading-snug">
                  The Future Is Uncertain
                </h3>
                <p class="text-sm text-gray-400 mt-3 leading-relaxed">
                  Traditional planning often relies on historical data, assumptions, and individual opinions.
                </p>
              </div>
            </div>
          </div>

          <!-- Box 2: Your Decisions Don't Have to Be Blind -->
          <div
            class="video-btn text-left rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeIdx === 1 ? 'is-active' : 'is-idle'"
            @click="activeIdx = 1"
          >
            <div class="flex items-start gap-4">
              <span
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-mono shrink-0 mt-0.5"
                :class="activeIdx === 1 ? 'bg-white/10 text-white font-semibold' : 'bg-white/5 text-gray-500'"
              >
                2
              </span>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-white text-base sm:text-lg leading-snug">
                  Your Decisions Don’t Have to Be Blind.
                </h3>
                <p class="text-sm text-gray-400 mt-3 leading-relaxed">
                  But real-world outcomes are shaped by multiple people, competing interests, changing conditions, and unexpected reactions.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Brain Image Frame (In place of video block) -->
        <div class="decision-col-right md:w-[62%]">
          <div class="player-frame relative w-full h-full rounded-2xl overflow-hidden bg-white/5 border border-white/10 shadow-2xl flex items-center justify-center">
            <img
              src="/images/cosmic-brain.jpg"
              alt="Predictive Intelligence Brain"
              class="w-full h-full object-cover object-center"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const activeIdx = ref(0)
</script>

<style scoped>
.orb-1 {
  position: absolute;
  width: 320px;
  height: 220px;
  border-radius: 50%;
  background: rgba(234, 160, 40, 0.08);
  filter: blur(60px);
  top: 20%;
  right: 10%;
  transform: rotate(-10deg);
  pointer-events: none;
  z-index: 1;
}

.decision-row {
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .decision-row {
    flex-direction: row;
  }
  .decision-col-left {
    width: 38%;
  }
  .decision-col-right {
    width: 62%;
  }
}

.video-btn {
  padding: 1.75rem 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  user-select: none;
  box-sizing: border-box;
}

@media (min-width: 640px) {
  .video-btn {
    padding: 1.875rem 1.75rem;
  }
}

.video-btn.is-active {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.video-btn.is-idle {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
}

.video-btn.is-idle:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.12);
  color: #e5e7eb;
}

.player-frame {
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  aspect-ratio: 16 / 9;
  min-height: 260px;
}

@media (min-width: 768px) {
  .player-frame {
    height: 100%;
    min-height: 100%;
    aspect-ratio: 16 / 9;
  }
}
</style>
