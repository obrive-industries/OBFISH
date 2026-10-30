<template>
  <section id="philosophy" class="philosophy-section">
    <div class="container-main relative z-[2] max-w-3xl mx-auto px-6">
      <div class="text-center mb-12">
        <p :class="['text-xs font-semibold text-[#2d554c] uppercase tracking-widest mb-3 anim font-michroma', { show: isVisible }]" style="transition-delay: 50ms;">
          About BRAIN
        </p>
        <h2 :class="['section-title anim font-microgramma mb-4', { show: isVisible }]" style="transition-delay: 100ms;">
          Simulate Possibilities. Make Smarter Decisions.
        </h2>
      </div>

      <p :class="['philosophy-text mb-6 anim', { show: isVisible }]" style="transition-delay: 200ms;">
        BRAIN is an AI-powered simulation and predictive intelligence platform designed to explore possibilities, understand complex behaviours, and evaluate potential outcomes.
      </p>

      <p :class="['philosophy-text mb-12 anim', { show: isVisible }]" style="transition-delay: 250ms;">
        By transforming real-world information, business challenges, research materials, and creative ideas into interactive scenarios, BRAIN helps users examine how different factors, decisions, and interactions could shape future outcomes. It creates a virtual environment where possibilities can be explored before decisions are made in the real world.
      </p>

      <h3 :class="['text-lg font-semibold text-[#073933] mb-4 anim font-michroma', { show: isVisible }]" style="transition-delay: 300ms;">
        How It Works
      </h3>
      <ul :class="['philosophy-text mb-12 space-y-2 anim', { show: isVisible }]" style="transition-delay: 350ms;">
        <li class="flex gap-2">
          <span class="text-[#2d554c] shrink-0">—</span>
          <span>You provide source materials such as data reports, research dossiers, or policy drafts and define your scenario in natural language.</span>
        </li>
        <li class="flex gap-2">
          <span class="text-[#2d554c] shrink-0">—</span>
          <span>BRAIN constructs ontological knowledge graphs, runs multi-agent swarms in a virtual environment, and synthesizes structured intelligence reports.</span>
        </li>
      </ul>

      <h3 :class="['text-lg font-semibold text-[#073933] mb-4 anim font-michroma', { show: isVisible }]" style="transition-delay: 400ms;">
        Our Vision
      </h3>
      <p :class="['philosophy-text mb-4 anim', { show: isVisible }]" style="transition-delay: 450ms;">
        Making advanced multi-agent simulation accessible to everyone — from founders and enterprise leaders to researchers and creative storytellers:
      </p>

      <ul :class="['philosophy-text mb-12 space-y-2 anim', { show: isVisible }]" style="transition-delay: 500ms;">
        <li class="flex gap-2">
          <span class="text-[#2d554c] shrink-0">—</span>
          <span><strong class="text-[#073933] font-michroma text-sm">Strategic Level:</strong> Explore business strategies, evaluate market opportunities, examine stakeholder responses, and assess potential risks before committing real capital and organizational resources.</span>
        </li>
        <li class="flex gap-2">
          <span class="text-[#2d554c] shrink-0">—</span>
          <span><strong class="text-[#073933] font-michroma text-sm">Creative Level:</strong> A generative sandbox for exploring ideas, developing fictional worlds, simulating character interactions, and discovering alternative storylines and creative endings.</span>
        </li>
        <li class="flex gap-2">
          <span class="text-[#2d554c] shrink-0">—</span>
          <span><strong class="text-[#073933] font-michroma text-sm">Research Level:</strong> Enable researchers and policy makers to investigate hypotheses, explore non-linear relationships, and generate targeted questions for real-world empirical validation.</span>
        </li>
      </ul>

      <div :class="['text-center anim mt-24', { show: isVisible }]" style="transition-delay: 600ms; font-family: 'Caveat', cursive;">
        <p class="text-4xl md:text-5xl text-black leading-snug">
          “Every possibility begins with a question.
        </p>
        <p class="text-4xl md:text-5xl text-[#073933] leading-snug mt-1">
          BRAIN helps you explore what comes next.”
        </p>
        <p class="text-xs font-michroma tracking-widest text-[#2d554c] uppercase mt-4">
          — BRAIN by Obrive Industries
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)

const checkScroll = () => {
  const el = document.getElementById('philosophy')
  if (!el) return
  if (el.getBoundingClientRect().top < window.innerHeight * 0.95 && !isVisible.value) {
    isVisible.value = true
  }
}

onMounted(() => {
  window.addEventListener('scroll', checkScroll, { passive: true })
  setTimeout(checkScroll, 100)
})

onUnmounted(() => {
  window.removeEventListener('scroll', checkScroll)
})
</script>

<style scoped>
.philosophy-section {
  position: relative;
  z-index: 10;
  background-color: transparent;
  padding-top: 70px;
  padding-bottom: 90px;
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

.anim {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.anim.show {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .anim {
    transition: none;
    opacity: 1;
    transform: none;
  }
}

.philosophy-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 22.75px;
  color: rgb(0, 0, 0);
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
