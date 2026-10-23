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

/* Variants */
.btn-variant-primary {
  background-color: #074139;
  color: #caede5;
  box-shadow: 0 4px 14px rgba(7, 65, 57, 0.25);
  transition: all 0.3s ease;
}

.btn-variant-primary:hover {
  background-color: #052e28;
  color: #ffffff;
  box-shadow: 0 6px 20px rgba(7, 65, 57, 0.35);
}

.btn-variant-accent {
  background-color: #a2f1df;
  color: #074139;
  box-shadow: 0 4px 14px rgba(162, 241, 223, 0.3);
  transition: all 0.3s ease;
}

.btn-variant-accent:hover {
  background-color: #8eead4;
  color: #052e28;
  box-shadow: 0 6px 20px rgba(162, 241, 223, 0.45);
}

.btn-variant-outline {
  background-color: transparent;
  color: #074139;
  border: 1px solid #074139;
  transition: all 0.3s ease;
}

.btn-variant-outline:hover {
  background-color: rgba(7, 65, 57, 0.08);
  color: #074139;
  border-color: #074139;
}

.btn-variant-outline-white {
  background-color: transparent;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.45);
  transition: all 0.3s ease;
}

.btn-variant-outline-white:hover {
  background-color: #ffffff;
  color: #074139;
  border-color: #ffffff;
}

.btn-variant-ghost {
  background-color: transparent;
  color: #074139;
  transition: all 0.3s ease;
}

.btn-variant-ghost:hover {
  background-color: rgba(7, 65, 57, 0.08);
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
