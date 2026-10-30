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
          <span class="bc-curr">Market Simulation AI</span>
        </nav>

        <!-- Hero Section -->
        <section class="detail-hero">
          <div class="eyebrow-pill">
            <span class="pulse-dot"></span>
            <span>MARKET INTELLIGENCE &amp; GTM</span>
          </div>

          <h1 class="detail-title">
            MARKET SIMULATION AI FOR LAUNCHES &amp; PRICING
          </h1>

          <p class="detail-lead">
            Test how prospective buyers, incumbents, channel partners, and market critics react to a launch, pricing update, or market entry before the public story forms around your brand.
          </p>

          <div class="hero-actions">
            <AnimatedButton
              type="button"
              variant="primary"
              size="default"
              :iconSize="13"
              arrowColor="default"
              @click="launchMarketConsole"
            >
              Run In Console
            </AnimatedButton>
            <AnimatedButton
              href="#how-it-works"
              variant="outline"
              size="default"
              :iconSize="13"
              arrowColor="primary"
            >
              Engine Anatomy
            </AnimatedButton>
          </div>

          <div class="disclaimer-note">
            Built for market narrative simulation and hypothesis testing, not statistical certainty. Every scenario should be verified against real customer evidence.
          </div>
        </section>

        <!-- Section 1: What Evidence to Bring -->
        <section class="content-section">
          <div class="section-badge">01 // EVIDENCE INPUTS</div>
          <h2 class="section-heading">What Evidence Should You Bring To Market Simulation AI?</h2>
          <p class="section-intro">
            A useful market simulation is honest about its inputs. Obrive Brain works best when grounded in the real documentation and research your team already has:
          </p>

          <div class="evidence-grid">
            <div class="evidence-card">
              <div class="card-icon">📄</div>
              <h3 class="evidence-title">Product Brief &amp; Positioning</h3>
              <p class="evidence-text">
                Target audience (ICP), feature notes, differentiation pillars, messaging angles, and the exact story your team wants the market to believe.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">⚔️</div>
              <h3 class="evidence-title">Competitive Context</h3>
              <p class="evidence-text">
                Direct competitors, legacy substitutes, price points, defensive claims, and recent feature releases from rival companies.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">🎙️</div>
              <h3 class="evidence-title">Customer Voice &amp; Objections</h3>
              <p class="evidence-text">
                Interview transcripts, churn notes, sales objections, review feedback, and willingness-to-pay friction points from prospects.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">🚀</div>
              <h3 class="evidence-title">Go-To-Market Plan</h3>
              <p class="evidence-text">
                Distribution channels, launch sequencing, promotional offers, partnership commitments, and planned PR announcements.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 2: When Teams Use It -->
        <section class="content-section">
          <div class="section-badge">02 // DECISION CONTEXTS</div>
          <h2 class="section-heading">When Should Teams Use Market Simulation AI?</h2>

          <div class="decisions-grid">
            <div class="decision-card">
              <span class="decision-num">01</span>
              <h3 class="decision-title">Product Launch Readiness</h3>
              <p class="decision-text">
                Model how buyers, reviewers, and competitor sales teams interpret your launch brief. Discover messaging blind spots before public rollout.
              </p>
            </div>

            <div class="decision-card">
              <span class="decision-num">02</span>
              <h3 class="decision-title">Pricing &amp; Packaging Changes</h3>
              <p class="decision-text">
                Stress-test tier boundaries, usage limits, grandfathering rules, and public communication of price hikes before customer pushback.
              </p>
            </div>

            <div class="decision-card">
              <span class="decision-num">03</span>
              <h3 class="decision-title">New Market or Regional Expansion</h3>
              <p class="decision-text">
                Evaluate regional buyer urgency, incumbent barriers, local channel resistance, and category perception in unfamiliar territories.
              </p>
            </div>

            <div class="decision-card">
              <span class="decision-num">04</span>
              <h3 class="decision-title">Defensive War Gaming</h3>
              <p class="decision-text">
                Simulate how key rivals may imitate, discount, launch smear campaigns, or bundle offerings when you release a breakthrough capability.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 3: How MiroFish Runs Market Simulation -->
        <section id="how-it-works" class="content-section">
          <div class="section-badge">03 // ENGINE ARCHITECTURE</div>
          <h2 class="section-heading">How Does The Multi-Agent Engine Run The Simulation?</h2>
          <p class="section-intro">
            Instead of a single chatbot guess, Obrive Brain builds an interactive agent ecosystem with diverse incentives and constraints:
          </p>

          <div class="timeline-steps">
            <div class="timeline-item">
              <div class="timeline-marker">1</div>
              <div class="timeline-content">
                <h4 class="timeline-title">Actor Graph &amp; Persona Instantiation</h4>
                <p class="timeline-desc">
                  Extracts distinct stakeholder agents: Enterprise Buyers, Tech Skeptics, Incumbent Reps, Budget Holders, and Tech Media Critics. Each actor receives independent background memory and private incentives.
                </p>
              </div>
            </div>

            <div class="timeline-item">
              <div class="timeline-marker">2</div>
              <div class="timeline-content">
                <h4 class="timeline-title">Multi-Round Interaction Swarm</h4>
                <p class="timeline-desc">
                  Actors debate, negotiate, and react across 3 to 5 discrete interaction rounds. One agent's objection influences peer consensus, creating emergent second-order consequences.
                </p>
              </div>
            </div>

            <div class="timeline-item">
              <div class="timeline-marker">3</div>
              <div class="timeline-content">
                <h4 class="timeline-title">Analytical Report Extraction</h4>
                <p class="timeline-desc">
                  The engine synthesizes round logs into a structured executive report highlighting turning points, consensus trajectories, fragile assumptions, and testable hypotheses.
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 4: What The Report Delivers -->
        <section class="content-section">
          <div class="section-badge">04 // DELIVERABLE REPORT</div>
          <h2 class="section-heading">What A Market Simulation Report Shows</h2>

          <div class="report-features-grid">
            <div class="report-feat-card">
              <h3 class="report-feat-title">Consensus Trajectory</h3>
              <p class="report-feat-desc">
                The most probable market story that forms after launch, mapping where audience excitement concentrates and where indifference sets in.
              </p>
            </div>

            <div class="report-feat-card">
              <h3 class="report-feat-title">Fragile Assumptions</h3>
              <p class="report-feat-desc">
                The unstated beliefs in your product brief that are most susceptible to breaking upon first contact with skeptical buyers.
              </p>
            </div>

            <div class="report-feat-card">
              <h3 class="report-feat-title">Plausible Turning Points</h3>
              <p class="report-feat-desc">
                The specific events (e.g. competitor matching price, onboarding failure, viral tweet) that could abruptly shift customer sentiment.
              </p>
            </div>

            <div class="report-feat-card">
              <h3 class="report-feat-title">Reversal Conditions</h3>
              <p class="report-feat-desc">
                The precise new data, evidence, or testimonial proof points required to invert a skeptical prospect segment into an active buyer.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 5: Why Multi-Agent vs Chatbots -->
        <section class="content-section">
          <div class="section-badge">05 // COMPARATIVE ADVANTAGE</div>
          <h2 class="section-heading">Why Multi-Agent Simulation Outperforms Simple Chatbots</h2>

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
                <tr>
                  <td class="dim-label">Stakeholder Perspective</td>
                  <td>Single compressed perspective that hallucinates agreement</td>
                  <td class="highlight-cell">Dozens of autonomous agents with competing commercial incentives</td>
                </tr>
                <tr>
                  <td class="dim-label">Dynamics</td>
                  <td>Static response; no sequential chain of reaction</td>
                  <td class="highlight-cell">Multi-round cascade loops where actor A's objection alters actor B's stance</td>
                </tr>
                <tr>
                  <td class="dim-label">Assumption Visibility</td>
                  <td>Implicit assumptions hidden in persuasive prose</td>
                  <td class="highlight-cell">Explicitly scored fragile assumptions and falsification criteria</td>
                </tr>
                <tr>
                  <td class="dim-label">Evidence Grounding</td>
                  <td>Generic training weights with no boundary verification</td>
                  <td class="highlight-cell">Grounded in uploaded documents, memos, and verified facts</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Pre-Loaded Simulation Prompt Launcher -->
        <section class="prompt-launcher-section">
          <div class="launcher-card">
            <div class="launcher-header">
              <span class="launcher-tag">PRE-LOADED MARKET PROMPT</span>
              <span class="launcher-ready">Ready for Execution</span>
            </div>
            <div class="prompt-code-box">
              <p class="prompt-text">
                "Run a multi-round market simulation evaluating our upcoming B2B SaaS product tier launch. Model 15 distinct personas across Enterprise IT Buyers, Mid-Market CFOs, and Competitor Sales Engineers. Focus on: (1) Pricing resistance at $499/mo, (2) Feature clarity of our real-time audit log, and (3) Reversal catalysts required to close procurement objections."
              </p>
            </div>
            <div class="launcher-actions">
              <AnimatedButton
                type="button"
                variant="primary"
                size="default"
                :iconSize="13"
                arrowColor="default"
                @click="launchMarketConsole"
              >
                Launch Simulation In Console
              </AnimatedButton>
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
import { ref } from 'vue'
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

const launchMarketConsole = () => {
  router.push({
    path: '/console',
    query: {
      prompt: 'Run a multi-round market simulation evaluating our upcoming B2B SaaS product launch. Model buyer personas, competitor counter-moves, and pricing elasticity.',
      useCase: 'market-simulation'
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
</style>
