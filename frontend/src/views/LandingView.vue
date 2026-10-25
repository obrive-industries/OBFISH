<template>
  <div class="marketing-page relative min-h-screen bg-black overflow-x-hidden text-white font-sans">
    <main class="relative z-10">
      <LandingHeader @open-auth="openAuth" />
      <LandingHero />
      <LandingDecisionDynamics />
      <LandingFeatures />
      <LandingUseCases />
      <LandingPhilosophy />
      <LandingFooter />
    </main>

    <!-- Fixed Dynamic Crowd Layer across the bottom of viewport -->
    <CrowdHeroIllustration class="fixed bottom-0 left-0 right-0 h-[40vh] z-[1000] pointer-events-none" />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import authStore from '../store/auth'
import LandingHeader from '../components/landing/LandingHeader.vue'
import LandingHero from '../components/landing/LandingHero.vue'
import LandingDecisionDynamics from '../components/landing/LandingDecisionDynamics.vue'
import LandingFeatures from '../components/landing/LandingFeatures.vue'
import LandingUseCases from '../components/landing/LandingUseCases.vue'
import LandingPhilosophy from '../components/landing/LandingPhilosophy.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'
import CrowdHeroIllustration from '../components/landing/CrowdHeroIllustration.vue'

const route = useRoute()

const openAuth = () => {
  authStore.openAuthModal('login')
}

onMounted(() => {
  document.body.style.backgroundColor = '#000000'
  if (route.query.auth === 'login') {
    authStore.openAuthModal('login', 'Please sign in to access protected simulation views.')
  }
  if (!route.hash) {
    window.scrollTo(0, 0)
  }
})

onUnmounted(() => {
  document.body.style.backgroundColor = ''
})
</script>

<style scoped>
.marketing-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #000000;
  color: #ffffff;
}
</style>
