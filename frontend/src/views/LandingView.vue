<template>
  <div class="landing-page-root">
    <!-- Header -->
    <LandingHeader />

    <!-- Main Content -->
    <main class="landing-main">
      <LandingHero />
      <LandingUncertainty />
      <LandingWorkflow />
      <LandingUseCases />
      <LandingAbout />
      <LandingFAQ />
    </main>

    <!-- Footer -->
    <LandingFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import LandingHeader from '../components/landing/LandingHeader.vue'
import LandingHero from '../components/landing/LandingHero.vue'
import LandingUncertainty from '../components/landing/LandingUncertainty.vue'
import LandingWorkflow from '../components/landing/LandingWorkflow.vue'
import LandingUseCases from '../components/landing/LandingUseCases.vue'
import LandingAbout from '../components/landing/LandingAbout.vue'
import LandingFAQ from '../components/landing/LandingFAQ.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'

onMounted(() => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.landing-page-root {
  min-height: 100vh;
  background-color: #070b0e;
  color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow-x: hidden;
  position: relative;
}

.landing-main {
  position: relative;
  z-index: 2;
}
</style>
