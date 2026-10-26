<template>
  <section id="decision-dynamics" class="decision-section py-20 bg-transparent relative z-10 overflow-hidden">
    <!-- Ambient Glow Orb -->
    <div class="orb orb-1" aria-hidden="true"></div>

    <div class="container-main relative z-[2]">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <p class="text-xs font-semibold text-[#2d554c] uppercase tracking-widest mb-4 font-michroma">Decision Dynamics</p>
        <h2 class="text-4xl md:text-5xl font-bold text-[#073933] mb-4 font-microgramma">Simulate Before You Commit</h2>
        <p class="text-[#163830] max-w-2xl mx-auto text-base md:text-lg leading-relaxed">
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
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-michroma shrink-0 mt-0.5"
                :class="activeIdx === 0 ? 'bg-[#073933] text-white font-semibold' : 'bg-black/5 text-[#163830] font-semibold'"
              >
                1
              </span>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-[#073933] text-base sm:text-lg leading-snug">
                  The Future Is Uncertain
                </h3>
                <p class="text-sm text-[#163830] mt-3 leading-relaxed">
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
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-michroma shrink-0 mt-0.5"
                :class="activeIdx === 1 ? 'bg-[#073933] text-white font-semibold' : 'bg-black/5 text-[#163830] font-semibold'"
              >
                2
              </span>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-[#073933] text-base sm:text-lg leading-snug">
                  Your Decisions Don’t Have to Be Blind.
                </h3>
                <p class="text-sm text-[#163830] mt-3 leading-relaxed">
                  But real-world outcomes are shaped by multiple people, competing interests, changing conditions, and unexpected reactions.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Brain Image Frame (In place of video block) -->
        <div class="decision-col-right md:w-[62%] flex items-center justify-center">
          <div class="player-frame relative w-full h-full bg-transparent flex items-center justify-center">
            <img
              src="/images/cosmic-brain.png"
              alt="Predictive Intelligence Brain"
              class="brain-transparent-img w-full h-full object-contain object-center"
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
  border: 1px solid rgba(10, 28, 23, 0.12);
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
  background: rgba(255, 255, 255, 0.9);
  border-color: #0a1c17;
  color: #0a1c17;
  box-shadow: 0 10px 25px -5px rgba(10, 28, 23, 0.12);
}

.video-btn.is-idle {
  background: rgba(255, 255, 255, 0.45);
  border-color: rgba(10, 28, 23, 0.12);
  color: #163830;
}

.video-btn.is-idle:hover {
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(10, 28, 23, 0.25);
  color: #0a1c17;
}

.player-frame {
  border: none;
  background: transparent;
  aspect-ratio: 16 / 9;
  min-height: 260px;
}

.brain-transparent-img {
  filter: drop-shadow(0 14px 28px rgba(7, 65, 57, 0.18));
  transition: transform 0.4s ease, filter 0.4s ease;
  user-select: none;
}

.brain-transparent-img:hover {
  transform: scale(1.02);
  filter: drop-shadow(0 18px 36px rgba(7, 65, 57, 0.25));
}

@media (min-width: 768px) {
  .player-frame {
    height: 100%;
    min-height: 100%;
    aspect-ratio: 16 / 9;
  }
}
</style>
