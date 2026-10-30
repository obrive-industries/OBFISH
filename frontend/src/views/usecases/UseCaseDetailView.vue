<template>
  <div class="usecase-detail-root">
    <!-- Header -->
    <LandingHeader @open-auth="openAuthModal" />

    <main class="usecase-main">
      <div class="container-main" v-if="scenario">
        <!-- Breadcrumb -->
        <nav class="breadcrumb-nav" aria-label="Breadcrumb">
          <router-link to="/use-cases" class="bc-link">← All Use Cases</router-link>
          <span class="bc-sep">/</span>
          <span class="bc-curr">{{ scenario.title }}</span>
        </nav>

        <!-- Hero Section -->
        <section class="detail-hero">
          <div class="eyebrow-pill">
            <span class="pulse-dot"></span>
            <span>{{ scenario.categoryLabel }}</span>
          </div>

          <h1 class="detail-title">
            {{ scenario.title.toUpperCase() }}
          </h1>

          <p class="detail-lead">
            {{ scenario.heroLead }}
          </p>

          <div class="hero-actions">
            <AnimatedButton
              type="button"
              variant="primary"
              size="default"
              :iconSize="13"
              arrowColor="default"
              @click="launchConsole"
            >
              Run In Console
            </AnimatedButton>
            <AnimatedButton
              href="#architecture"
              variant="outline"
              size="default"
              :iconSize="13"
              arrowColor="primary"
            >
              Engine Anatomy
            </AnimatedButton>
          </div>

          <div class="disclaimer-note">
            {{ scenario.disclaimer }}
          </div>
        </section>

        <!-- Section 1: Evidence Inputs -->
        <section class="content-section">
          <div class="section-badge">01 // EVIDENCE INPUTS</div>
          <h2 class="section-heading">{{ scenario.evidenceHeading }}</h2>
          <p class="section-intro">
            {{ scenario.evidenceIntro }}
          </p>

          <div class="evidence-grid">
            <div
              v-for="card in scenario.evidenceCards"
              :key="card.title"
              class="evidence-card"
            >
              <div class="card-icon">{{ card.icon }}</div>
              <h3 class="evidence-title">{{ card.title }}</h3>
              <p class="evidence-text">{{ card.text }}</p>
            </div>
          </div>
        </section>

        <!-- Section 2: Key Decision Contexts -->
        <section class="content-section">
          <div class="section-badge">02 // DECISION SCENARIOS</div>
          <h2 class="section-heading">{{ scenario.decisionHeading }}</h2>

          <div class="decisions-grid">
            <div
              v-for="card in scenario.decisionCards"
              :key="card.title"
              class="decision-card"
            >
              <span class="decision-num">{{ card.num }}</span>
              <h3 class="decision-title">{{ card.title }}</h3>
              <p class="decision-text">{{ card.text }}</p>
            </div>
          </div>
        </section>

        <!-- Section 3: Architecture Timeline -->
        <section id="architecture" class="content-section">
          <div class="section-badge">03 // ENGINE ARCHITECTURE</div>
          <h2 class="section-heading">How Does The Multi-Agent Swarm Run The Scenario?</h2>
          <p class="section-intro">
            Obrive Brain maps your inputs into a dynamic actor ecosystem rather than a single synthetic prediction:
          </p>

          <div class="timeline-steps">
            <div
              v-for="step in scenario.timelineSteps"
              :key="step.step"
              class="timeline-item"
            >
              <div class="timeline-marker">{{ step.step }}</div>
              <div class="timeline-content">
                <h4 class="timeline-title">{{ step.title }}</h4>
                <p class="timeline-desc">{{ step.desc }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 4: What The Report Delivers -->
        <section class="content-section">
          <div class="section-badge">04 // DELIVERABLE REPORT</div>
          <h2 class="section-heading">What The Simulation Report Exposes</h2>

          <div class="report-features-grid">
            <div
              v-for="sig in scenario.reportSignals"
              :key="sig.title"
              class="report-feat-card"
            >
              <h3 class="report-feat-title">{{ sig.title }}</h3>
              <p class="report-feat-desc">{{ sig.desc }}</p>
            </div>
          </div>
        </section>

        <!-- Section 5: Why Multi-Agent Outperforms Chatbots -->
        <section class="content-section">
          <div class="section-badge">05 // STRUCTURAL ADVANTAGE</div>
          <h2 class="section-heading">Why Multi-Agent Simulation Beats Single Chatbots</h2>

          <div class="comparison-table-wrapper">
            <table class="comparison-table">
              <thead>
                <tr>
                  <th>Dimension</th>
                  <th>Single Prompt / Chatbot</th>
                  <th>Obrive Brain Multi-Agent Swarm</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in scenario.comparisonRows" :key="row.dimension">
                  <td class="dim-label">{{ row.dimension }}</td>
                  <td>{{ row.chatbot }}</td>
                  <td class="highlight-cell">{{ row.swarm }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Pre-Loaded Simulation Prompt Launcher -->
        <section class="prompt-launcher-section">
          <div class="launcher-card">
            <div class="launcher-header">
              <span class="launcher-tag">PRE-LOADED SIMULATION PROMPT</span>
              <span class="launcher-ready">Ready for Execution</span>
            </div>
            <div class="prompt-code-box">
              <p class="prompt-text">
                "{{ scenario.preloadedPrompt }}"
              </p>
            </div>
            <div class="launcher-actions">
              <AnimatedButton
                type="button"
                variant="primary"
                size="default"
                :iconSize="13"
                arrowColor="default"
                @click="launchConsole"
              >
                Launch Simulation In Console
              </AnimatedButton>
            </div>
          </div>
        </section>
      </div>

      <!-- Fallback 404 State -->
      <div class="container-main not-found-state" v-else>
        <h2 class="not-found-title">Use Case Scenario Not Found</h2>
        <p class="not-found-text">
          The requested simulation scenario does not exist or has been relocated.
        </p>
        <AnimatedButton
          to="/use-cases"
          variant="primary"
          size="default"
          :iconSize="13"
          arrowColor="default"
        >
          Return to All Use Cases
        </AnimatedButton>
      </div>
    </main>

    <!-- Footer -->
    <LandingFooter />

    <!-- Auth Modal -->
    <AuthModal
      :is-open="showAuthModal"
      @close="showAuthModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LandingHeader from '../../components/landing/LandingHeader.vue'
import LandingFooter from '../../components/landing/LandingFooter.vue'
import AuthModal from '../../components/AuthModal.vue'
import AnimatedButton from '../../components/common/AnimatedButton.vue'
import { useCasesRegistry } from '../../data/useCasesRegistry.js'

const route = useRoute()
const router = useRouter()
const showAuthModal = ref(false)

const openAuthModal = () => {
  showAuthModal.value = true
}

const scenario = computed(() => {
  const slug = route.params.slug
  return useCasesRegistry[slug] || null
})

const launchConsole = () => {
  if (!scenario.value) return
  router.push({
    path: '/console',
    query: {
      prompt: scenario.value.preloadedPrompt,
      useCase: scenario.value.slug
    }
  })
}
</script>

<style scoped>
.usecase-detail-root {
  min-height: 100vh;
  background-color: #A2F1DF;
  color: #073933;
  display: flex;
  flex-direction: column;
}

.usecase-main {
  flex: 1;
  padding-top: 6rem;
  padding-bottom: 4rem;
}

.container-main {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

@media (min-width: 1024px) {
  .container-main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

/* Breadcrumb */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  margin-bottom: 1.5rem;
}

.bc-link {
  color: #073933;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}

.bc-link:hover {
  opacity: 0.75;
}

.bc-sep {
  color: rgba(7, 57, 51, 0.4);
}

.bc-curr {
  color: #2d554c;
}

/* Hero */
.detail-hero {
  text-align: center;
  max-width: 58rem;
  margin-left: auto;
  margin-right: auto;
  padding-top: 1rem;
  padding-bottom: 3.5rem;
}

.eyebrow-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 9999px;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  letter-spacing: 0.18em;
  color: #073933;
  margin-bottom: 1.5rem;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00e5a3;
  box-shadow: 0 0 6px #00e5a3;
}

.detail-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.6rem, 3.2vw, 2.25rem);
  line-height: 1.18;
  color: #073933;
  margin-bottom: 1.25rem;
  letter-spacing: 0.02em;
}

.detail-lead {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 15px;
  line-height: 26px;
  color: #163830;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.primary-action-btn {
  padding: 0.85rem 1.75rem;
  background: #073933;
  color: #ffffff;
  border: 1px solid #073933;
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.2);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.primary-action-btn:hover {
  background: #042823;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(7, 57, 51, 0.3);
}

.secondary-action-btn {
  padding: 0.85rem 1.75rem;
  background: rgba(255, 255, 255, 0.65);
  color: #073933;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.secondary-action-btn:hover {
  background: #ffffff;
  border-color: #073933;
}

.disclaimer-note {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  line-height: 18px;
  color: #2d554c;
  max-width: 42rem;
  margin: 0 auto;
}

/* Content Sections */
.content-section {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  margin-bottom: 2.5rem;
}

.section-badge {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: #2d554c;
  margin-bottom: 0.5rem;
}

.section-heading {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.15rem, 2.2vw, 1.45rem);
  color: #073933;
  line-height: 1.25;
  margin-bottom: 1rem;
}

.section-intro {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 22px;
  color: #163830;
  margin-bottom: 2rem;
  max-width: 52rem;
}

/* Evidence Grid */
.evidence-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .evidence-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .evidence-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.evidence-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.card-icon {
  font-size: 1.75rem;
  margin-bottom: 0.75rem;
}

.evidence-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.evidence-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
}

/* Decisions Grid */
.decisions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .decisions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.decision-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.decision-num {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 24px;
  line-height: 36px;
  color: rgb(7, 57, 51);
  display: block;
  margin-bottom: 0.5rem;
}

.decision-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.decision-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
}

/* Timeline */
.timeline-steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.timeline-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #073933;
  color: #A2F1DF;
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.timeline-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #073933;
  margin-bottom: 0.35rem;
}

.timeline-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
  margin: 0;
}

/* Report Features */
.report-features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .report-features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.report-feat-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.report-feat-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.report-feat-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
}

/* Comparison Table */
.comparison-table-wrapper {
  overflow-x: auto;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
}

.comparison-table th {
  text-align: left;
  padding: 1rem;
  background: rgba(7, 57, 51, 0.08);
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.1em;
  color: #073933;
  border-bottom: 2px solid rgba(7, 57, 51, 0.2);
}

.comparison-table td {
  padding: 1.15rem 1rem;
  border-bottom: 1px solid rgba(7, 57, 51, 0.1);
  line-height: 18px;
  vertical-align: top;
}

.dim-label {
  font-weight: 600;
  color: #073933;
}

.highlight-cell {
  background: rgba(162, 241, 223, 0.25);
  font-weight: 600;
  color: #073933;
}

/* Prompt Launcher */
.prompt-launcher-section {
  margin-bottom: 2.5rem;
}

.launcher-card {
  background: #073933;
  color: #ffffff;
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  box-shadow: 0 16px 40px rgba(7, 57, 51, 0.25);
}

.launcher-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.launcher-tag {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.15em;
  color: #A2F1DF;
}

.launcher-ready {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  background: rgba(0, 229, 163, 0.2);
  color: #00e5a3;
  padding: 3px 8px;
  border-radius: 4px;
}

.prompt-code-box {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 1rem;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.prompt-text {
  font-family: 'Space Grotesk', monospace;
  font-size: 13px;
  line-height: 22px;
  color: #e2e8f0;
  margin: 0;
  font-style: italic;
}

.launcher-actions {
  display: flex;
  justify-content: flex-end;
}

.launcher-btn {
  padding: 0.85rem 1.75rem;
  background: #A2F1DF;
  color: #073933;
  border: none;
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.launcher-btn:hover {
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(162, 241, 223, 0.4);
}

.not-found-state {
  text-align: center;
  padding: 6rem 1rem;
}

.not-found-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 2rem;
  color: #073933;
  margin-bottom: 1rem;
}

.not-found-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 14px;
  color: #163830;
  margin-bottom: 2rem;
}
</style>
