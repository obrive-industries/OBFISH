<template>
  <!-- Pricing is now handled exclusively by the dedicated /pricing page -->
</template>

<script setup>
import { watch } from 'vue'
import { useRouter } from 'vue-router'
import billingStore from '../store/billing'

const router = useRouter()
const state = billingStore.state

watch(
  () => state.pricingOpen,
  (open) => {
    if (open) {
      state.pricingOpen = false
      router.push('/pricing')
    }
  },
  { immediate: true }
)
</script>
