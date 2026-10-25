<template>
  <component
    :is="componentType"
    :to="to"
    :href="href"
    :target="target"
    :rel="rel"
    :type="isButton ? type : undefined"
    :disabled="disabled"
    class="btn-animated"
    :class="[
      `btn-variant-${variant}`,
      `btn-size-${size}`,
      { 'btn-pill': pill },
      customClass
    ]"
    @click="$emit('click', $event)"
  >
    <span class="btn-inner">
      <!-- Sliding Left Arrow (enters on hover) -->
      <span
        v-if="showArrow"
        class="btn-animated__icon --1"
        :style="{ width: `${iconSize}px`, height: `${iconSize}px` }"
      >
        <RightAnimateIcon :color="resolvedArrowColor" :size="iconSize" />
      </span>

      <!-- Label / Slot -->
      <span class="btn-animated__label">
        <slot />
      </span>

      <!-- Sliding Right Arrow (leaves on hover) -->
      <span
        v-if="showArrow"
        class="btn-animated__icon --2"
        :style="{ width: `${iconSize}px`, height: `${iconSize}px`, marginLeft: '8px' }"
      >
        <RightAnimateIcon :color="resolvedArrowColor" :size="iconSize" />
      </span>
    </span>
  </component>
</template>

<script setup>
import { computed } from 'vue'
import RightAnimateIcon from './RightAnimateIcon.vue'

const props = defineProps({
  to: {
    type: [String, Object],
    default: null,
  },
  href: {
    type: String,
    default: null,
  },
  target: {
    type: String,
    default: null,
  },
  rel: {
    type: String,
    default: null,
  },
  type: {
    type: String,
    default: 'button',
  },
  variant: {
    type: String,
    default: 'primary', // 'primary' | 'accent' | 'outline' | 'outline-white' | 'ghost'
  },
  size: {
    type: String,
    default: 'default', // 'sm' | 'default' | 'lg'
  },
  showArrow: {
    type: Boolean,
    default: true,
  },
  iconSize: {
    type: Number,
    default: 13,
  },
  arrowColor: {
    type: String,
    default: null, // If null, auto-determined by variant
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  pill: {
    type: Boolean,
    default: false,
  },
  customClass: {
    type: String,
    default: '',
  },
})

defineEmits(['click'])

const isButton = computed(() => !props.to && !props.href)

const componentType = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'button'
})

const resolvedArrowColor = computed(() => {
  if (props.arrowColor) return props.arrowColor
  if (props.variant === 'accent') return 'primary'
  if (props.variant === 'outline') return 'primary'
  if (props.variant === 'outline-white') return 'white'
  if (props.variant === 'ghost') return 'primary'
  return 'default' // Primary variant has CAEDE5 arrow
})
</script>

<style scoped>
.btn-inner {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* MiroFish Variants */
.btn-variant-primary {
  background-color: #ffffff;
  color: #000000;
  box-shadow: 0 2px 10px rgba(255, 255, 255, 0.12);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid #ffffff;
  font-weight: 600;
}

.btn-variant-primary:hover {
  background-color: #e5e7eb;
  color: #000000;
  border-color: #e5e7eb;
  box-shadow: 0 4px 16px rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.btn-variant-accent {
  background-color: #ffffff;
  color: #000000;
  box-shadow: 0 2px 10px rgba(255, 255, 255, 0.12);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid #ffffff;
  font-weight: 600;
}

.btn-variant-accent:hover {
  background-color: #e5e7eb;
  color: #000000;
  border-color: #e5e7eb;
  box-shadow: 0 4px 16px rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.btn-variant-outline {
  background-color: transparent;
  color: #ffffff;
  border: 1.5px solid rgba(255, 255, 255, 0.45);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 500;
}

.btn-variant-outline:hover {
  background-color: #ffffff;
  color: #000000;
  border-color: #ffffff;
  transform: translateY(-1px);
}

.btn-variant-outline-white {
  background-color: transparent;
  color: #ffffff;
  border: 1.5px solid #ffffff;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 500;
}

.btn-variant-outline-white:hover {
  background-color: #ffffff;
  color: #000000;
  border-color: #ffffff;
  transform: translateY(-1px);
}

.btn-variant-ghost {
  background-color: transparent;
  color: #ffffff;
  transition: all 0.2s ease;
}

.btn-variant-ghost:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

/* Sizes */
.btn-size-sm {
  padding: 6px 14px;
  font-size: 11px;
  border-radius: 8px;
}

.btn-size-default {
  padding: 10px 22px;
  font-size: 12px;
  border-radius: 10px;
}

.btn-size-lg {
  padding: 14px 28px;
  font-size: 13px;
  border-radius: 12px;
}

.btn-pill {
  border-radius: 9999px !important;
}

/* Disabled */
.btn-animated:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}
</style>
