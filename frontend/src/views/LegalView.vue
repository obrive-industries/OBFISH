<template>
  <div class="legal-page-root">
    <div class="legal-container">
      <!-- Obrive Primary Logo directly above content (matches Obrive CompanyInfo layout) -->
      <div class="legal-logo-row">
        <router-link to="/" class="legal-logo-link" aria-label="Obrive Home">
          <img
            src="/obrive-logo.svg"
            alt="Obrive Logo Primary"
            class="legal-logo-img"
          />
        </router-link>
      </div>

      <!-- Document Header (matches Obrive CompanyInfoHeader.tsx) -->
      <header class="legal-header">
        <h1 class="legal-doc-title">
          {{ activePolicy.title }}
        </h1>

        <div class="legal-meta-row">
          <div class="legal-meta-item">
            <svg
              class="legal-meta-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M18 20a6 6 0 0 0-12 0"></path>
              <circle cx="12" cy="10" r="4"></circle>
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
            <span>{{ activePolicy.company }}</span>
          </div>

          <div class="legal-meta-item">
            <svg
              class="legal-meta-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M8 2v4"></path>
              <path d="M16 2v4"></path>
              <rect width="18" height="18" x="3" y="4" rx="2"></rect>
              <path d="M3 10h18"></path>
              <path d="M10 16h4"></path>
            </svg>
            <span>{{ activePolicy.effectiveDate }}</span>
          </div>
        </div>

        <div class="legal-last-updated">
          <span class="legal-last-updated-label">Last updated: </span>
          <span>{{ activePolicy.lastUpdated }}</span>
        </div>
      </header>

      <!-- Document Sections (matches Obrive CompanyInfoSection & CompanyInfoItem) -->
      <div class="legal-sections-flow">
        <section
          v-for="section in activePolicy.sections"
          :key="section.id || section.num"
          :id="section.id"
          class="legal-section"
        >
          <!-- Section Title (h2 in microgrammaBold) -->
          <h2 v-if="section.title" class="legal-section-title">
            {{ section.title }}
          </h2>

          <!-- Disclaimer / Callout box (matches Obrive CompanyInfoMDX blockquote) -->
          <div v-if="isDisclaimerSection(section.title)" class="legal-callout-wrapper">
            <div class="legal-callout-box">
              <p
                v-for="(item, idx) in section.items"
                :key="idx"
                class="legal-callout-text"
              >
                {{ item.text }}
              </p>
            </div>
          </div>

          <!-- Standard Section Content Flow -->
          <div v-else class="legal-section-body">
            <template v-for="(item, idx) in section.items" :key="idx">
              <!-- Subsection Heading -->
              <div v-if="item.type === 'subsection'" class="legal-subsection-title-wrap">
                <h3 class="legal-subsection-title">
                  {{ item.title }}
                </h3>
              </div>

              <!-- Paragraph Text -->
              <p
                v-else-if="item.text"
                class="legal-paragraph"
              >
                {{ item.text }}
              </p>
            </template>
          </div>
        </section>
      </div>

      <!-- Subtle Policy Navigation & Copyright Footer -->
      <footer class="legal-footer">
        <div class="legal-footer-links">
          <router-link
            to="/terms"
            class="legal-footer-link"
            :class="{ 'legal-footer-link--active': currentPolicyId === 'terms' }"
          >
            Terms of Service
          </router-link>
          <span class="legal-footer-sep">•</span>
          <router-link
            to="/privacy"
            class="legal-footer-link"
            :class="{ 'legal-footer-link--active': currentPolicyId === 'privacy' }"
          >
            Privacy Policy
          </router-link>
          <span class="legal-footer-sep">•</span>
          <router-link
            to="/refund"
            class="legal-footer-link"
            :class="{ 'legal-footer-link--active': currentPolicyId === 'refund' }"
          >
            Refund Policy
          </router-link>
        </div>
        <p class="legal-copyright">
          © 2026 Obrive Industries Private Limited. All rights reserved.
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import legalPoliciesData from '../data/legalPolicies.json'

const route = useRoute()

const currentPolicyId = ref('terms')

const activePolicy = computed(() => {
  return legalPoliciesData[currentPolicyId.value] || legalPoliciesData.terms
})

const isDisclaimerSection = (title) => {
  if (!title) return false
  const t = title.toLowerCase()
  return t.includes('disclaimer') || t.includes('limitation of liability')
}

const syncPolicyFromRoute = () => {
  if (route.path.includes('privacy') || route.query.tab === 'privacy') {
    currentPolicyId.value = 'privacy'
  } else if (route.path.includes('refund') || route.query.tab === 'refund') {
    currentPolicyId.value = 'refund'
  } else {
    currentPolicyId.value = 'terms'
  }
}

watch(() => route.path, () => {
  syncPolicyFromRoute()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

onMounted(() => {
  document.body.style.backgroundColor = '#ffffff'
  syncPolicyFromRoute()
})

onUnmounted(() => {
  document.body.style.backgroundColor = ''
})
</script>

<style scoped>
.legal-page-root {
  background-color: #ffffff;
  color: #111827;
  min-height: 100vh;
  width: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Authentic Obrive max-w-[950px] container centered on page */
.legal-container {
  max-width: 950px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 36px;
  padding-bottom: 96px;
  box-sizing: border-box;
}

@media (min-width: 640px) {
  .legal-container {
    padding-left: 32px;
    padding-right: 32px;
    padding-top: 56px;
    padding-bottom: 96px;
  }
}

@media (min-width: 1024px) {
  .legal-container {
    padding-left: 0;
    padding-right: 0;
    padding-top: 64px;
    padding-bottom: 96px;
  }
}

/* Obrive primary logo above document */
.legal-logo-row {
  margin-bottom: 32px;
}

.legal-logo-link {
  display: inline-block;
  line-height: 0;
  text-decoration: none;
}

.legal-logo-img {
  width: 70px;
  height: 46px;
  object-fit: contain;
  display: block;
  transition: opacity 0.2s ease;
}

.legal-logo-img:hover {
  opacity: 0.85;
}

/* Header component matching CompanyInfoHeader.tsx */
.legal-header {
  margin-bottom: 40px;
}

.legal-doc-title {
  font-family: 'microgrammaBold', 'Microgramma', sans-serif !important;
  font-size: 26px;
  line-height: 34px;
  color: #073933;
  font-weight: 700;
  margin: 0 0 8px 0;
}

@media (min-width: 640px) {
  .legal-doc-title {
    font-size: 30px;
    line-height: 36px;
  }
}

.legal-meta-row {
  display: flex;
  align-items: center;
  gap: 24px;
  font-family: 'Michroma', 'Michroma Fallback', sans-serif;
  font-size: 14px;
  line-height: 20px;
  color: #374151;
  flex-wrap: wrap;
}

.legal-meta-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.legal-meta-icon {
  width: 16px;
  height: 16px;
  color: #4b5563;
  flex-shrink: 0;
}

.legal-last-updated {
  margin-top: 40px;
  font-family: 'Michroma', 'Michroma Fallback', sans-serif;
  font-size: 14px;
  line-height: 20px;
  color: #374151;
}

.legal-last-updated-label {
  font-family: 'microgrammaBold', 'Microgramma', sans-serif !important;
  font-weight: 700;
  color: #073933;
}

/* Section flow matching CompanyInfoSection.tsx */
.legal-sections-flow {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.legal-section {
  display: flex;
  flex-direction: column;
}

.legal-section-title {
  font-family: 'microgrammaBold', 'Microgramma', sans-serif !important;
  font-size: 24px;
  line-height: 32px;
  color: #073933;
  font-weight: 700;
  margin: 0 0 24px 0;
}

@media (min-width: 640px) {
  .legal-section-title {
    font-size: 30px;
    line-height: 36px;
  }
}

.legal-section-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.legal-subsection-title-wrap {
  margin-top: 16px;
  margin-bottom: 4px;
}

.legal-subsection-title {
  font-family: 'microgrammaBold', 'Microgramma', sans-serif !important;
  font-size: 18px;
  line-height: 24px;
  color: #073933;
  font-weight: 700;
  margin: 0;
}

.legal-paragraph {
  font-family: 'Michroma', 'Michroma Fallback', sans-serif;
  font-size: 14px;
  line-height: 22.75px;
  color: #374151;
  margin: 0;
  white-space: pre-line;
}

/* Disclaimer / Blockquote callout box matching Obrive CompanyInfoMDX blockquote */
.legal-callout-wrapper {
  margin-top: 24px;
  margin-bottom: 24px;
  padding-right: 0;
}

@media (min-width: 640px) {
  .legal-callout-wrapper {
    padding-right: 48px;
  }
}

@media (min-width: 1024px) {
  .legal-callout-wrapper {
    padding-right: 96px;
  }
}

.legal-callout-box {
  background-color: #073933;
  color: #A2F1DF;
  border-radius: 12px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

@media (min-width: 640px) {
  .legal-callout-box {
    padding: 48px;
  }
}

.legal-callout-text {
  font-family: 'microgrammaBold', 'Microgramma', sans-serif !important;
  font-size: 16px;
  line-height: 26px;
  color: #A2F1DF;
  margin: 0;
  white-space: pre-line;
}

@media (min-width: 640px) {
  .legal-callout-text {
    font-size: 18px;
    line-height: 28px;
  }
}

/* Subtle footer */
.legal-footer {
  margin-top: 80px;
  padding-top: 32px;
  border-top: 1px solid #f3f4f6;
  text-align: center;
  font-family: 'Michroma', 'Michroma Fallback', sans-serif;
  font-size: 12px;
  line-height: 18px;
  color: #9ca3af;
}

.legal-footer-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.legal-footer-link {
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s ease;
}

.legal-footer-link:hover {
  color: #073933;
  text-decoration: underline;
}

.legal-footer-link--active {
  color: #073933;
  font-weight: 700;
}

.legal-footer-sep {
  color: #d1d5db;
}

.legal-copyright {
  margin-top: 12px;
  font-size: 11px;
  color: #9ca3af;
}
</style>
