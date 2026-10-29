<template>
  <component
    :is="componentType"
    :to="to"
    :href="href"
    :target="target"
    :rel="rel"
    :type="isButton ? type : undefined"
    :disabled="disabled"
    class="btn-animated btn"
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
        class="btn-animated__icon btn__icon --1"
        :style="{ width: `${iconSize}px`, height: `${iconSize}px` }"
        aria-hidden="true"
      >
        <RightAnimateIcon :color="resolvedArrowColor" :size="iconSize" />
      </span>

      <!-- Label / Slot -->
      <span class="btn-animated__label btn__label">
        <slot />
      </span>

      <!-- Sliding Right Arrow (leaves on hover) -->
      <span
        v-if="showArrow"
        class="btn-animated__icon btn__icon --2"
        :style="{ width: `${iconSize}px`, height: `${iconSize}px`, marginInlineStart: '8px' }"
        aria-hidden="true"
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
    default: 'primary', // 'primary' | 'outline' | 'white' | 'outline-white' | 'dark' | 'accent' | 'ghost'
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
  if (props.variant === 'primary') return 'default' // #CAEDE5 mint
  if (props.variant === 'outline') return 'primary' // #074139 forest
  if (props.variant === 'outline-white') return 'white'
  if (props.variant === 'white') return 'primary'
  if (props.variant === 'accent') return 'primary'
  if (props.variant === 'dark' || props.variant === 'black') return 'accent'
  if (props.variant === 'ghost') return 'primary'
  return 'default'
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

/* Obrive Variants */
.btn-variant-primary {
  background-color: #073933;
  color: #ffffff;
  border: 1px solid #073933;
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.25);
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
  font-weight: 600;
}

.btn-variant-primary:hover {
  background-color: #074139;
  border-color: #074139;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(7, 57, 51, 0.38);
}

.btn-variant-outline {
  background-color: transparent;
  color: #074139;
  border: 1px solid #074139;
  box-shadow: 0 2px 8px rgba(7, 65, 57, 0.08);
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
  font-weight: 600;
}

.btn-variant-outline:hover {
  background-color: rgba(7, 65, 57, 0.08);
  border-color: #073933;
  color: #073933;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(7, 65, 57, 0.16);
}

.btn-variant-white {
  background-color: #ffffff;
  color: #073933;
  border: 1px solid #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 600;
}

.btn-variant-white:hover {
  background-color: #f3f4f6;
  border-color: #f3f4f6;
  color: #073933;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
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
  color: #073933;
  border-color: #ffffff;
  transform: translateY(-2px);
}

.btn-variant-dark,
.btn-variant-black {
  background-color: #000000;
  color: #A2F1DF;
  border: 1px solid #000000;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  transition: all 0.3s ease;
  font-weight: 700;
}

.btn-variant-dark:hover,
.btn-variant-black:hover {
  background-color: #073933;
  border-color: #073933;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(7, 57, 51, 0.35);
}

.btn-variant-accent {
  background-color: #A2F1DF;
  color: #073933;
  border: 1px solid #A2F1DF;
  box-shadow: 0 2px 10px rgba(7, 57, 51, 0.12);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 600;
}

.btn-variant-accent:hover {
  background-color: #8eebd6;
  border-color: #8eebd6;
  color: #073933;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(7, 57, 51, 0.2);
}

.btn-variant-ghost {
  background-color: transparent;
  color: #073933;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  font-weight: 600;
}

.btn-variant-ghost:hover {
  background-color: rgba(7, 57, 51, 0.08);
  color: #073933;
}

/* Sizes matching Obrive */
.btn-size-sm {
  padding: 0.6rem 1.4rem;
  font-size: 0.75rem;
  line-height: 1rem;
  border-radius: 0.75rem;
}

.btn-size-default {
  padding: 0.75rem 1.85rem;
  font-size: 0.8125rem;
  line-height: 1.25rem;
  border-radius: 0.75rem;
}

.btn-size-lg {
  padding: 0.875rem 2.25rem;
  font-size: 0.8125rem;
  line-height: 1.25rem;
  border-radius: 0.75rem;
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
