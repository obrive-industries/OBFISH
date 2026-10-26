<template>
  <section id="decision-dynamics" class="decision-section py-20 bg-transparent relative z-10 overflow-hidden">
    <!-- Ambient Glow Orb -->
    <div class="orb orb-1" aria-hidden="true"></div>

    <div class="container-main relative z-[2]">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <p class="text-xs font-semibold text-[#2d554c] uppercase tracking-widest mb-4 font-michroma">Decision Dynamics</p>
        <h2 class="section-title mb-4 font-microgramma">Simulate Before You Commit</h2>
        <p class="text-black max-w-2xl mx-auto text-base md:text-lg leading-relaxed font-normal">
          Navigate emergent complexity by testing every strategic assumption against an autonomous multi-agent swarm.
        </p>
      </div>

      <!-- Side-by-Side Flex Layout (Exact match with reference screenshot) -->
      <div class="decision-row flex flex-col md:flex-row gap-8 max-w-5xl mx-auto items-center">
        <!-- Left Side: 2 Decision Blocks -->
        <div class="decision-col-left md:w-[38%] w-full grid grid-cols-1 gap-4">
          <!-- Box 1: The Future Is Uncertain -->
          <div
            class="video-btn text-left rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeIdx === 0 ? 'is-active' : 'is-idle'"
            @click="activeIdx = 0"
          >
            <h3 class="font-semibold text-[#073933] text-base leading-snug">
              The Future Is Uncertain
            </h3>
            <p class="text-xs sm:text-sm text-black mt-2 leading-relaxed font-normal">
              Traditional planning relies on static assumptions and historical data that fail when unexpected real-world reactions emerge.
            </p>
          </div>

          <!-- Box 2: Check Your Decisions -->
          <div
            class="video-btn text-left rounded-2xl transition-all duration-300 cursor-pointer"
            :class="activeIdx === 1 ? 'is-active' : 'is-idle'"
            @click="activeIdx = 1"
          >
            <h3 class="font-semibold text-[#073933] text-base leading-snug">
              Check Your Decisions
            </h3>
            <p class="text-xs sm:text-sm text-black mt-2 leading-relaxed font-normal">
              Shaped by multiple people, competing interests, changing conditions, and unexpected reactions
            </p>
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

.decision-col-left {
  display: grid;
  grid-template-rows: repeat(2, minmax(0, 1fr));
  gap: 1rem;
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
  padding: 1.15rem 1.25rem;
  border-radius: 1rem;
  border: 1px solid rgba(10, 28, 23, 0.12);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  user-select: none;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 110px;
}

@media (min-width: 640px) {
  .video-btn {
    padding: 1.25rem 1.35rem;
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
  color: #000000;
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

.section-title {
  font-family: microgrammaBold, "microgrammaBold Fallback", 'Microgramma', sans-serif !important;
  font-size: 40px !important;
  font-weight: 800 !important;
  line-height: 44.4444px !important;
  color: rgb(0, 0, 0) !important;
}

@media (max-width: 640px) {
  .section-title {
    font-size: clamp(28px, 6vw, 40px) !important;
    line-height: 1.15 !important;
  }
}
</style>
