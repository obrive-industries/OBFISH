<template>
  <div class="rounded-ball-wrapper" :style="{ width: `${width}px`, height: `${height}px` }">
    <img
      src="../../assets/icons/rounded-icon.svg"
      alt="Obrive Badge"
      class="rounded-ball-img"
      :style="{ width: `${width}px`, height: `${height}px` }"
    />
  </div>
</template>

<script setup>
defineProps({
  width: {
    type: [Number, String],
    default: 16,
  },
  height: {
    type: [Number, String],
    default: 24,
  },
})
</script>

<style scoped>
.rounded-ball-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rounded-ball-img {
  object-fit: contain;
  display: block;
}
</style>
