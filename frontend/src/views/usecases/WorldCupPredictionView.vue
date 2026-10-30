<template>
  <div class="usecase-detail-root">
    <!-- Header -->
    <LandingHeader @open-auth="openAuthModal" />

    <main class="usecase-main">
      <div class="container-main">
        <!-- Breadcrumb -->
        <nav class="breadcrumb-nav" aria-label="Breadcrumb">
          <router-link to="/use-cases" class="bc-link">← All Use Cases</router-link>
          <span class="bc-sep">/</span>
          <span class="bc-curr">World Cup 2026 Prediction Lab</span>
        </nav>

        <!-- Hero Section -->
        <section class="detail-hero">
          <div class="eyebrow-pill">
            <span class="pulse-dot"></span>
            <span>SPORTS, SCENARIOS &amp; EVENT FORECASTING</span>
          </div>

          <h1 class="detail-title">
            BUILD A WORLD CUP PREDICTION FROM YOUR OWN EVIDENCE
          </h1>

          <p class="detail-lead">
            Choose a 2026 matchup, configure scouting context and tactical pressure, and run an Obrive Brain simulation to inspect plausible trajectories and turning points before kickoff.
          </p>

          <div class="hero-actions">
            <AnimatedButton
              href="#prediction-lab"
              variant="primary"
              size="default"
              :iconSize="13"
              arrowColor="default"
            >
              Configure Fixture
            </AnimatedButton>
            <AnimatedButton
              to="/console"
              variant="outline"
              size="default"
              :iconSize="13"
              arrowColor="primary"
            >
              Direct Console
            </AnimatedButton>
          </div>

          <div class="disclaimer-note">
            Predictions are exploratory multi-agent scenario simulations, not gambling or betting advice. No live scores or bookmaker odds.
          </div>
        </section>

        <!-- Interactive Prediction Lab -->
        <section id="prediction-lab" class="lab-section">
          <div class="lab-card">
            <div class="lab-header">
              <div class="lab-badge">INTERACTIVE SIMULATION LAB</div>
              <h2 class="lab-title">Create Your 2026 World Cup Prediction</h2>
              <p class="lab-desc">
                Define the fixture first. Then adjust the focus and evidence parameters to generate an inspectable simulation brief for the engine.
              </p>
            </div>

            <div class="lab-grid">
              <!-- Left: Controls -->
              <div class="lab-controls">
                <!-- Tournament Stage -->
                <div class="control-group">
                  <label class="control-label">Tournament Stage</label>
                  <select v-model="selectedStage" class="control-select">
                    <option v-for="stage in stages" :key="stage" :value="stage">
                      {{ stage }}
                    </option>
                  </select>
                </div>

                <!-- Fixture Teams -->
                <div class="control-group">
                  <label class="control-label">Match Fixture</label>
                  <div class="teams-input-row">
                    <div class="team-input-box">
                      <span class="team-label">Team 1</span>
                      <input
                        v-model="teamA"
                        type="text"
                        placeholder="e.g. Argentina"
                        class="team-input"
                      />
                    </div>
                    <span class="vs-badge">VS</span>
                    <div class="team-input-box">
                      <span class="team-label">Team 2</span>
                      <input
                        v-model="teamB"
                        type="text"
                        placeholder="e.g. France"
                        class="team-input"
                      />
                    </div>
                  </div>

                  <!-- Quick Select Pills -->
                  <div class="quick-teams">
                    <span class="quick-title">Quick Picks:</span>
                    <button
                      v-for="pair in quickMatchups"
                      :key="pair.label"
                      type="button"
                      @click="setQuickMatchup(pair.teamA, pair.teamB)"
                      class="quick-team-btn"
                    >
                      {{ pair.label }}
                    </button>
                  </div>
                </div>

                <!-- Prediction Focus -->
                <div class="control-group">
                  <label class="control-label">Prediction Focus</label>
                  <div class="focus-pills">
                    <button
                      v-for="focus in focusOptions"
                      :key="focus.id"
                      type="button"
                      @click="selectedFocus = focus.id"
                      class="focus-btn"
                      :class="{ active: selectedFocus === focus.id }"
                    >
                      <span class="focus-btn-title">{{ focus.title }}</span>
                      <span class="focus-btn-sub">{{ focus.desc }}</span>
                    </button>
                  </div>
                </div>

                <!-- Extra Context (Optional) -->
                <div class="control-group">
                  <label class="control-label">Tactical Context &amp; Notes (Optional)</label>
                  <textarea
                    v-model="extraContext"
                    placeholder="e.g. Team A has key midfield suspension; Team B switching to 3-5-2 high pressing block; altitude advantage..."
                    rows="3"
                    class="context-textarea"
                  ></textarea>
                </div>
              </div>

              <!-- Right: Live Brief Preview & Launcher -->
              <div class="lab-preview-col">
                <div class="preview-box">
                  <div class="preview-header">
                    <span class="preview-tag">LIVE SIMULATION BRIEF</span>
                    <span class="preview-status">Auto-Constructed</span>
                  </div>

                  <div class="preview-content">
                    <p class="preview-text">{{ generatedBrief }}</p>
                  </div>

                  <div class="preview-footer">
                    <AnimatedButton
                      type="button"
                      variant="primary"
                      size="default"
                      :iconSize="13"
                      arrowColor="default"
                      class="w-full justify-center"
                      @click="launchPrediction"
                    >
                      Run This Prediction In Console
                    </AnimatedButton>
                    <p class="run-hint">
                      Transfers this structured analytical brief directly into the MiroFish / Obrive Brain simulation engine.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 1: What a Robust Prediction Explains -->
        <section class="content-section">
          <div class="section-badge">01 // FORECAST METHODOLOGY</div>
          <h2 class="section-heading">What A World Cup Simulation Should Explain</h2>
          <p class="section-intro">
            A useful tournament forecast is far more than a single predicted scoreline. It exposes the underlying tactical mechanisms, psychological pressure points, and conditionality:
          </p>

          <div class="method-grid">
            <div class="method-card">
              <span class="method-num">01</span>
              <h3 class="method-title">Phase-by-Phase Match Trajectory</h3>
              <p class="method-text">
                Traces the contest from opening tactical setups to late-game fatigue, modeling how high presses decay and how spaces open up in extra time.
              </p>
            </div>

            <div class="method-card">
              <span class="method-num">02</span>
              <h3 class="method-title">Decisive Tactical Turning Points</h3>
              <p class="method-text">
                Identifies which specific substitutions, red-card risks, or tactical formation pivots will destabilize the favorite's defensive structure.
              </p>
            </div>

            <div class="method-card">
              <span class="method-num">03</span>
              <h3 class="method-title">Conditional Confidence Parameters</h3>
              <p class="method-text">
                Explicitly documents what structural assumptions the forecast depends on (e.g. holding midfielder starting, weather conditions).
              </p>
            </div>

            <div class="method-card">
              <span class="method-num">04</span>
              <h3 class="method-title">Reversal Catalysts</h3>
              <p class="method-text">
                Details the exact new scouting information or lineup changes that would overturn the simulated win probability.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 2: From Match Brief to Multi-Agent Forecast -->
        <section class="content-section">
          <div class="section-badge">02 // AGENT MODELING</div>
          <h2 class="section-heading">From Match Brief To Evidence-Led Forecast</h2>

          <div class="steps-row">
            <div class="step-col">
              <div class="step-bubble">1</div>
              <h4 class="step-head">Tactical &amp; Squad Context</h4>
              <p class="step-body">
                Add current squad lists, recent international form, set-piece xG ratings, injury reports, and tournament rest days.
              </p>
            </div>

            <div class="step-col">
              <div class="step-bubble">2</div>
              <h4 class="step-head">Multi-Agent Simulation</h4>
              <p class="step-body">
                Obrive Brain assigns personas to Head Coaches, Tactical Analysts, Key Playmakers, VAR Officials, and Tournament Media.
              </p>
            </div>

            <div class="step-col">
              <div class="step-bubble">3</div>
              <h4 class="step-head">Full Scenario Report</h4>
              <p class="step-body">
                Receive an analytical match forecast with tactical heatmaps, turning points, penalty shootout probabilities, and narrative fallout.
              </p>
            </div>
          </div>
        </section>

        <!-- FAQ Section -->
        <section class="content-section">
          <div class="section-badge">03 // FAQ &amp; GOVERNANCE</div>
          <h2 class="section-heading">Frequently Asked Questions</h2>

          <div class="faq-list">
            <div class="faq-item">
              <h3 class="faq-question">Does this tool offer sports betting advice or odds?</h3>
              <p class="faq-answer">
                No. Obrive Brain is an exploratory analytical simulation engine for qualitative and tactical scenario planning. It does not scrape bookmaker odds, provide betting tips, or guarantee sports gambling outcomes.
              </p>
            </div>

            <div class="faq-item">
              <h3 class="faq-question">Can I upload my own scouting reports or tactical PDFs?</h3>
              <p class="faq-answer">
                Yes! When you run the brief in the Simulation Console, you can upload scouting dossiers, match statistics, or player fitness reports (PDF, Markdown, or TXT) to ground the multi-agent swarm in proprietary data.
              </p>
            </div>

            <div class="faq-item">
              <h3 class="faq-question">How does multi-agent simulation differ from statistical Monte Carlo models?</h3>
              <p class="faq-answer">
                Monte Carlo models sample historic numerical averages. Obrive Brain simulates human behavioral reactions—coach tactical adjustments, player fatigue under high-stakes tournament pressure, psychological momentum, and referee controversy.
              </p>
            </div>
          </div>
        </section>
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
import { useRouter } from 'vue-router'
import LandingHeader from '../../components/landing/LandingHeader.vue'
import LandingFooter from '../../components/landing/LandingFooter.vue'
import AuthModal from '../../components/AuthModal.vue'
import AnimatedButton from '../../components/common/AnimatedButton.vue'

const router = useRouter()
const showAuthModal = ref(false)

const openAuthModal = () => {
  showAuthModal.value = true
}

const stages = [
  'Group Stage',
  'Round of 32',
  'Round of 16',
  'Quarter-final',
  'Semi-final',
  'Third-place match',
  'Final'
]

const selectedStage = ref('Quarter-final')
const teamA = ref('Argentina')
const teamB = ref('France')
const selectedFocus = ref('outcome')
const extraContext = ref('')

const quickMatchups = [
  { label: 'Argentina vs France', teamA: 'Argentina', teamB: 'France' },
  { label: 'Brazil vs Germany', teamA: 'Brazil', teamB: 'Germany' },
  { label: 'Spain vs England', teamA: 'Spain', teamB: 'England' },
  { label: 'Portugal vs Netherlands', teamA: 'Portugal', teamB: 'Netherlands' }
]

const setQuickMatchup = (a, b) => {
  teamA.value = a
  teamB.value = b
}

const focusOptions = [
  {
    id: 'outcome',
    title: 'Match Outcome & Path',
    desc: 'Forecast likely scoreline trajectory and regulation/extra-time outcome.'
  },
  {
    id: 'tactics',
    title: 'Turning Points & Subs',
    desc: 'Identify tactical substitutions and critical second-half formation shifts.'
  },
  {
    id: 'narrative',
    title: 'Tournament Narrative',
    desc: 'Trace how match results reshape global media coverage and manager scrutiny.'
  }
]

const generatedBrief = computed(() => {
  const tA = teamA.value.trim() || 'Team A'
  const tB = teamB.value.trim() || 'Team B'
  const stg = selectedStage.value
  const focusObj = focusOptions.find(f => f.id === selectedFocus.value)
  const focusText = focusObj ? focusObj.title : 'Match Outcome'

  let brief = `Build an evidence-led 2026 World Cup prediction for the ${stg} match between ${tA} and ${tB}. `
  brief += `Primary simulation focus: ${focusText}. `
  if (extraContext.value.trim()) {
    brief += `Key tactical context provided: "${extraContext.value.trim()}". `
  }
  brief += `Use attached tactical scouting context as primary evidence. Return: (1) likely match trajectory and tactical phases, (2) three decisive head-to-head factors, (3) plausible turning points and substitution catalysts, (4) confidence conditions, and (5) evidence most likely to invert the forecast. Do not present gambling certainty or betting odds.`

  return brief
})

const launchPrediction = () => {
  router.push({
    path: '/console',
    query: {
      prompt: generatedBrief.value,
      useCase: 'world-cup-prediction'
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
  max-width: 60rem;
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

/* Lab Section */
.lab-section {
  margin-bottom: 4rem;
}

.lab-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  border: 2px solid #073933;
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  box-shadow: 0 16px 40px rgba(7, 57, 51, 0.12);
}

.lab-header {
  margin-bottom: 2rem;
  text-align: center;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
}

.lab-badge {
  display: inline-block;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: #073933;
  background: rgba(162, 241, 223, 0.6);
  padding: 4px 12px;
  border-radius: 9999px;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.lab-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.2rem, 2.5vw, 1.55rem);
  color: #073933;
  margin-bottom: 0.75rem;
  line-height: 1.25;
}

.lab-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 22px;
  color: #163830;
}

.lab-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .lab-grid {
    grid-template-columns: 1.2fr 1fr;
  }
}

.lab-controls {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-label {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.12em;
  color: #073933;
  text-transform: uppercase;
}

.control-select {
  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  color: #073933;
  outline: none;
}

.control-select:focus {
  border-color: #073933;
}

.teams-input-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.team-input-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.team-label {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  color: #2d554c;
}

.team-input {
  width: 100%;
  padding: 0.75rem 0.85rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  color: #073933;
  outline: none;
}

.team-input:focus {
  border-color: #073933;
}

.vs-badge {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 12px;
  background: #073933;
  color: #A2F1DF;
  padding: 6px 10px;
  border-radius: 8px;
  margin-top: 1rem;
}

.quick-teams {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.quick-title {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  color: #2d554c;
}

.quick-team-btn {
  background: rgba(7, 57, 51, 0.08);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 9999px;
  padding: 3px 10px;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  color: #073933;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-team-btn:hover {
  background: #073933;
  color: #ffffff;
}

.focus-pills {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.focus-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 0.75rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.focus-btn:hover {
  border-color: #073933;
}

.focus-btn.active {
  background: #073933;
  border-color: #073933;
}

.focus-btn-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.08em;
  color: #073933;
  margin-bottom: 2px;
}

.focus-btn.active .focus-btn-title {
  color: #A2F1DF;
}

.focus-btn-sub {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  color: #163830;
}

.focus-btn.active .focus-btn-sub {
  color: rgba(255, 255, 255, 0.85);
}

.context-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  color: #073933;
  outline: none;
  resize: vertical;
}

.context-textarea:focus {
  border-color: #073933;
}

/* Lab Preview */
.lab-preview-col {
  display: flex;
  flex-direction: column;
}

.preview-box {
  background: #073933;
  color: #ffffff;
  border-radius: 1.25rem;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-shadow: 0 12px 32px rgba(7, 57, 51, 0.2);
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.preview-tag {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.15em;
  color: #A2F1DF;
}

.preview-status {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  background: rgba(0, 229, 163, 0.2);
  color: #00e5a3;
  padding: 2px 8px;
  border-radius: 4px;
}

.preview-content {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 0.75rem;
  padding: 1.25rem;
  flex-grow: 1;
  margin-bottom: 1.5rem;
}

.preview-text {
  font-family: 'Space Grotesk', monospace;
  font-size: 12px;
  line-height: 22px;
  color: #e2e8f0;
  margin: 0;
  white-space: pre-wrap;
}

.preview-footer {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.run-lab-btn {
  width: 100%;
  padding: 0.9rem;
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
  text-align: center;
}

.run-lab-btn:hover {
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(162, 241, 223, 0.4);
}

.run-hint {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  line-height: 16px;
  color: rgba(255, 255, 255, 0.65);
  text-align: center;
  margin: 0;
}

/* Methodology Grid */
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

.method-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .method-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.method-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.method-num {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 24px;
  line-height: 36px;
  color: rgb(7, 57, 51);
  display: block;
  margin-bottom: 0.5rem;
}

.method-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.method-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
}

/* Steps Row */
.steps-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .steps-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

.step-col {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
  text-align: center;
}

.step-bubble {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #073933;
  color: #A2F1DF;
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.step-head {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.step-body {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
  margin: 0;
}

/* FAQ List */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.faq-question {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.faq-answer {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
  margin: 0;
}
</style>
