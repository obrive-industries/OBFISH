<template>
  <div
    v-if="!isCompletelyGone"
    class="crowd-illustration-root"
    :class="{ 'is-exiting': isExiting }"
    aria-hidden="true"
    ref="containerRef"
  >
    <!-- Parallax crowd stage -->
    <div class="crowd-stage" :style="stageStyle">
      <!-- Person entities - ALL characters actively move -->
      <div
        v-for="person in activePersons"
        :key="person.id"
        class="person-wrapper"
        :class="person.motionClass"
        :style="getPersonWrapperStyle(person)"
      >
        <div class="person-gate-wing">
          <div
            class="person-entity"
            :class="{ 'animate-bob': !reducedMotion }"
            :style="getEntityStyle(person)"
          >
            <img
              :src="person.svgUrl"
              alt=""
              class="person-svg"
              :style="getImageStyle(person)"
              loading="eager"
              decoding="async"
              draggable="false"
              @error="handleSvgError(person, $event)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const containerRef = ref(null)
const isExiting = ref(false)
const isDismissed = ref(false)
const isCompletelyGone = ref(false)
const reducedMotion = ref(false)
const mouseOffsetX = ref(0)
const mouseOffsetY = ref(0)
const persons = ref([])

// Total pool of 105 verified OpenPeeps SVGs in /peeps/
const TOTAL_SVGS = 105
const getSvgUrl = (index) => {
  return `/peeps/openpeeps${index}.svg`
}

// Generate crowd where EVERY single image moves (half LTR, half RTL)
const generateCrowd = () => {
  if (isDismissed.value) return

  const width = typeof window !== 'undefined' ? window.innerWidth : 1200
  const isMobile = width < 640
  const isTablet = width >= 640 && width < 1024

  const list = []
  let idCounter = 0

  // Shuffle SVG indices so characters are nicely distributed
  const allSvgIndices = Array.from({ length: TOTAL_SVGS }, (_, i) => i + 1)
  for (let i = allSvgIndices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[allSvgIndices[i], allSvgIndices[j]] = [allSvgIndices[j], allSvgIndices[i]]
  }
  let svgPtr = 0
  const nextSvgIndex = () => {
    const idx = allSvgIndices[svgPtr % TOTAL_SVGS]
    svgPtr++
    return idx
  }

  // Helper to populate a moving tier with staggered starting points
  const addMovingTier = ({ count, layer, baseDuration, scaleMin, scaleMax, blur, opacity, zBase, bottomMin, bottomMax, bobDurationBase, bobAmount, swayDeg }) => {
    for (let i = 0; i < count; i++) {
      // Alternate direction: every even is walk-ltr, every odd is walk-rtl
      const movingLtr = i % 2 === 0
      const type = movingLtr ? 'walk-ltr' : 'walk-rtl'
      const motionClass = movingLtr ? 'motion-walk-ltr' : 'motion-walk-rtl'

      // Duration varies per person
      const duration = baseDuration + (i % 5) * 3 + Math.floor(Math.random() * 4)

      // Evenly distribute stagger fraction across the tier so characters populate the entire width on load
      const fraction = (i + 0.35 + (Math.random() * 0.2 - 0.1)) / count
      const clampedFraction = Math.max(0.05, Math.min(0.95, fraction))
      const staggerDelay = duration * clampedFraction

      const scale = scaleMin + (i % 3) * ((scaleMax - scaleMin) / 2)
      const bottomPercent = bottomMin + (i % 4) * ((bottomMax - bottomMin) / 3)

      const chosenSvgIndex = nextSvgIndex()

      list.push({
        id: `crowd-${layer}-${++idCounter}`,
        layer,
        type,
        motionClass,
        svgIndex: chosenSvgIndex,
        svgUrl: getSvgUrl(chosenSvgIndex),
        scale,
        blur,
        opacity,
        zIndex: zBase + i,
        bottomPercent,
        duration,
        staggerDelay,
        flip: !movingLtr, // RTL characters face left, LTR characters face right
        bobDuration: bobDurationBase + (i % 4) * 0.35,
        bobDelay: (i * 0.8) % 3.0,
        bobAmount,
        swayDeg,
      })
    }
  }

  // Tier 1: Background Crowd (All moving, slower, softer silhouettes, higher up)
  const bgCount = isMobile ? 8 : isTablet ? 14 : 22
  addMovingTier({
    count: bgCount,
    layer: 'bg',
    baseDuration: 48,
    scaleMin: 0.65,
    scaleMax: 0.78,
    blur: 0.8,
    opacity: 0.75,
    zBase: 10,
    bottomMin: 3,
    bottomMax: 7,
    bobDurationBase: 3.5,
    bobAmount: 2.5,
    swayDeg: 0.6,
  })

  // Tier 2: Midground Crowd (All moving, moderate speed, crisp outlines)
  const midCount = isMobile ? 12 : isTablet ? 18 : 28
  addMovingTier({
    count: midCount,
    layer: 'mid',
    baseDuration: 34,
    scaleMin: 0.80,
    scaleMax: 0.95,
    blur: 0,
    opacity: 0.92,
    zBase: 30,
    bottomMin: 0,
    bottomMax: 3,
    bobDurationBase: 3.0,
    bobAmount: 3,
    swayDeg: 0.8,
  })

  // Tier 3: Foreground Crowd (All moving, detailed, crisp, dynamic speed)
  const fgCount = isMobile ? 10 : isTablet ? 16 : 25
  addMovingTier({
    count: fgCount,
    layer: 'fg',
    baseDuration: 24,
    scaleMin: 0.95,
    scaleMax: 1.10,
    blur: 0,
    opacity: 1.0,
    zBase: 60,
    bottomMin: -2,
    bottomMax: 1,
    bobDurationBase: 2.5,
    bobAmount: 3,
    swayDeg: 0.8,
  })

  persons.value = list
}

// Fallback if SVG fails to load
const handleSvgError = (person, event) => {
  if (person._hasRetried) {
    if (event?.target) event.target.style.opacity = '0'
    return
  }
  person._hasRetried = true
  const nextIndex = ((person.svgIndex + 3) % TOTAL_SVGS) + 1
  person.svgIndex = nextIndex
  person.svgUrl = getSvgUrl(nextIndex)
}

// Gentle mouse parallax
const stageStyle = computed(() => {
  if (reducedMotion.value) return {}
  const shiftX = mouseOffsetX.value * 12
  const shiftY = mouseOffsetY.value * 5
  return {
    transform: `translate3d(${shiftX}px, ${shiftY}px, 0)`,
  }
})

// Styles per person wrapper - continuous infinite keyframe motion
const getPersonWrapperStyle = (p) => {
  // OpenPeeps native SVG viewBox is 240x324
  const baseWidth = 240
  const baseHeight = 324
  const w = Math.round(baseWidth * p.scale)
  const h = Math.round(baseHeight * p.scale)

  const style = {
    position: 'absolute',
    left: '0',
    bottom: `${p.bottomPercent}%`,
    width: `${w}px`,
    height: `${h}px`,
    zIndex: p.zIndex,
    pointerEvents: 'none',
  }

  if (!reducedMotion.value) {
    style.animationDuration = `${p.duration}s`
    style.animationDelay = `-${p.staggerDelay.toFixed(2)}s`
  }

  return style
}

// Bobbing & swaying
const getEntityStyle = (p) => {
  return {
    animationDuration: `${p.bobDuration}s`,
    animationDelay: `-${p.bobDelay}s`,
    '--bob-y': `${p.bobAmount}px`,
    '--sway-deg': `${p.swayDeg}deg`,
  }
}

// Image appearance
const getImageStyle = (p) => {
  const flip = p.flip ? -1 : 1
  return {
    filter: p.blur > 0 ? `blur(${p.blur.toFixed(1)}px)` : 'none',
    opacity: p.opacity,
    transform: `scaleX(${flip})`,
    width: '100%',
    height: '100%',
    display: 'block',
  }
}

const activePersons = computed(() => persons.value)

// Scroll handler: triggers gate-opening exit animation ONCE from middle to left and right
const handleScroll = () => {
  if (typeof window === 'undefined') return
  if (isDismissed.value) return

  const scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0
  const threshold = (window.innerHeight || 800) * 0.15
  if (scrollY > threshold) {
    // 1. Mark permanently dismissed
    isDismissed.value = true
    isExiting.value = true

    // 2. Gate Opening: Split characters left & right from the middle
    const midX = window.innerWidth / 2
    const wrappers = containerRef.value?.querySelectorAll('.person-wrapper')
    wrappers?.forEach((wrapper) => {
      const rect = wrapper.getBoundingClientRect()
      const charCenter = rect.left + rect.width / 2
      const wing = wrapper.querySelector('.person-gate-wing')
      if (wing) {
        if (charCenter < midX) {
          wing.classList.add('gate-exit-left')
        } else {
          wing.classList.add('gate-exit-right')
        }
      }
    })

    // 3. Remove listeners immediately so scroll never runs again
    window.removeEventListener('scroll', handleScroll)
    window.removeEventListener('mousemove', handleMouseMove)

    // 4. After gate animation completes (950ms), completely unmount from DOM
    setTimeout(() => {
      isCompletelyGone.value = true
    }, 950)
  }
}

// Mouse parallax handler
const handleMouseMove = (e) => {
  if (reducedMotion.value || isDismissed.value) return
  const { innerWidth, innerHeight } = window
  mouseOffsetX.value = e.clientX / innerWidth - 0.5
  mouseOffsetY.value = e.clientY / innerHeight - 0.5
}

// Window resize handler
let resizeTimer = null
const handleResize = () => {
  if (isDismissed.value) return
  if (resizeTimer) clearTimeout(resizeTimer)
  resizeTimer = setTimeout(() => {
    generateCrowd()
  }, 250)
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)')
    reducedMotion.value = media.matches
    media.addEventListener?.('change', (e) => {
      reducedMotion.value = e.matches
    })

    generateCrowd()

    // If page loaded/restored already scrolled down, dismiss immediately
    const initialScrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0
    const threshold = (window.innerHeight || 800) * 0.22
    if (initialScrollY > threshold) {
      isDismissed.value = true
      isExiting.value = true
      isCompletelyGone.value = true
    } else {
      window.addEventListener('scroll', handleScroll, { passive: true })
      window.addEventListener('mousemove', handleMouseMove, { passive: true })
      window.addEventListener('resize', handleResize, { passive: true })
    }
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', handleScroll)
    window.removeEventListener('mousemove', handleMouseMove)
    window.removeEventListener('resize', handleResize)
    if (resizeTimer) clearTimeout(resizeTimer)
  }
})
</script>

<style scoped>
.crowd-illustration-root {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  max-width: 100vw;
  height: 58vh;
  min-height: 480px;
  max-height: 640px;
  overflow-x: clip;
  overflow-y: visible;
  pointer-events: none;
  z-index: 1000;
  transition: transform 0.8s cubic-bezier(0.2, 0.9, 0.3, 1), opacity 0.65s ease, filter 0.65s ease;
  will-change: transform, opacity, filter;
}

/* Exit state */
.crowd-illustration-root.is-exiting {
  pointer-events: none;
}

/* Person Gate Wing: smooth sliding left/right from middle */
.person-gate-wing {
  width: 100%;
  height: 100%;
  will-change: transform, opacity;
}

.person-gate-wing.gate-exit-left {
  animation: gate-open-left 0.9s cubic-bezier(0.2, 0.85, 0.25, 1) forwards !important;
}

.person-gate-wing.gate-exit-right {
  animation: gate-open-right 0.9s cubic-bezier(0.2, 0.85, 0.25, 1) forwards !important;
}

@keyframes gate-open-left {
  0% {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
  65% {
    opacity: 0.85;
  }
  100% {
    transform: translate3d(-100vw, 0, 0);
    opacity: 0;
  }
}

@keyframes gate-open-right {
  0% {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
  65% {
    opacity: 0.85;
  }
  100% {
    transform: translate3d(100vw, 0, 0);
    opacity: 0;
  }
}

.crowd-stage {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform;
}

.person-wrapper {
  transform-origin: center bottom;
  user-select: none;
  -webkit-user-select: none;
}

/* ALL characters continuously move via GPU compositor thread across full width */
.motion-walk-ltr {
  animation-name: crowd-walk-ltr;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  will-change: transform;
}

.motion-walk-rtl {
  animation-name: crowd-walk-rtl;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  will-change: transform;
}

@keyframes crowd-walk-ltr {
  0% {
    transform: translate3d(-350px, 0, 0);
  }
  100% {
    transform: translate3d(calc(100vw + 350px), 0, 0);
  }
}

@keyframes crowd-walk-rtl {
  0% {
    transform: translate3d(calc(100vw + 350px), 0, 0);
  }
  100% {
    transform: translate3d(-350px, 0, 0);
  }
}

.person-entity {
  width: 100%;
  height: 100%;
  will-change: transform;
}

/* Organic vertical bobbing & sway */
.animate-bob {
  animation-name: organic-bob;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

@keyframes organic-bob {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  30% {
    transform: translateY(calc(var(--bob-y, 4px) * -1)) rotate(var(--sway-deg, 0.8deg));
  }
  70% {
    transform: translateY(calc(var(--bob-y, 4px) * 0.35)) rotate(calc(var(--sway-deg, 0.8deg) * -1));
  }
}

.person-svg {
  filter: drop-shadow(0 4px 12px rgba(10, 28, 23, 0.22));
  image-rendering: optimizeQuality;
}

/* Responsive tuning */
@media (max-width: 768px) {
  .crowd-illustration-root {
    height: 46vh;
    min-height: 360px;
    max-height: 460px;
  }
}

@media (max-width: 480px) {
  .crowd-illustration-root {
    height: 42vh;
    min-height: 320px;
    max-height: 400px;
  }
}
</style>
