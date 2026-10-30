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
          <span class="bc-curr">Public Opinion Simulation AI</span>
        </nav>

        <!-- Hero Section -->
        <section class="detail-hero">
          <div class="eyebrow-pill">
            <span class="pulse-dot"></span>
            <span>REPUTATION, INCIDENTS &amp; POLICY</span>
          </div>

          <h1 class="detail-title">
            PUBLIC OPINION SIMULATION AI FOR CRISIS &amp; POLICY
          </h1>

          <p class="detail-lead">
            Simulate how media publications, industry regulators, affected users, and online audiences reshape an incident, policy announcement, or corporate statement over multi-round cascade loops.
          </p>

          <div class="hero-actions">
            <AnimatedButton
              type="button"
              variant="primary"
              size="default"
              :iconSize="13"
              arrowColor="default"
              @click="launchOpinionConsole"
            >
              Test Incident Reaction
            </AnimatedButton>
            <AnimatedButton
              href="#cascade-dynamics"
              variant="outline"
              size="default"
              :iconSize="13"
              arrowColor="primary"
            >
              Cascade Dynamics
            </AnimatedButton>
          </div>

          <div class="disclaimer-note">
            Built for scenario stress-testing and strategic rehearsal, not absolute sentiment certainty. Always evaluate simulation trajectories alongside legal counsel and communications leadership.
          </div>
        </section>

        <!-- Section 1: Bring The Defining Material -->
        <section class="content-section">
          <div class="section-badge">01 // SOURCE EVIDENCE</div>
          <h2 class="section-heading">Bring The Material That Defines The Public Question</h2>
          <p class="section-intro">
            Public opinion simulation works best when grounded in concrete facts rather than vague hypothetical summaries. Provide the actual documents your leadership is reviewing:
          </p>

          <div class="evidence-grid">
            <div class="evidence-card">
              <div class="card-icon">⏱️</div>
              <h3 class="evidence-title">Chronological Incident Timeline</h3>
              <p class="evidence-text">
                When events occurred, when detection happened, when executives were notified, and the known impact surface across customer accounts.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">📜</div>
              <h3 class="evidence-title">Proposed Public Statement</h3>
              <p class="evidence-text">
                The exact draft communication, press release, blog announcement, or customer email planned for release.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">⚖️</div>
              <h3 class="evidence-title">Regulatory &amp; Legal Context</h3>
              <p class="evidence-text">
                Compliance mandates, mandatory reporting obligations, contractual SLA liabilities, and precedent cases in your industry.
              </p>
            </div>

            <div class="evidence-card">
              <div class="card-icon">👥</div>
              <h3 class="evidence-title">Affected Stakeholders</h3>
              <p class="evidence-text">
                Specific customer segments, internal employees, partner vendors, industry analysts, and online community leaders.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 2: Opinion is a System of Interpretation -->
        <section class="content-section">
          <div class="section-badge">02 // COGNITIVE ARCHITECTURE</div>
          <h2 class="section-heading">Public Opinion Is A System Of Interpretation, Not A Score</h2>
          <p class="section-intro">
            Traditional sentiment tools reduce complex public events to a simplistic positive/negative percentage. Obrive Brain treats public reaction as an ecosystem of competing interpretive frames:
          </p>

          <div class="frames-grid">
            <div class="frame-card">
              <div class="frame-tag">FRAME 1</div>
              <h3 class="frame-title">Harm &amp; Vulnerability</h3>
              <p class="frame-desc">
                Did customers or vulnerable groups suffer financial, privacy, or emotional damage? How is empathy perceived in leadership responses?
              </p>
            </div>

            <div class="frame-card">
              <div class="frame-tag">FRAME 2</div>
              <h3 class="frame-title">Responsibility &amp; Deflection</h3>
              <p class="frame-desc">
                Does the organization acknowledge root causality, or does it attempt to shift blame to third-party vendors, rogue actors, or ambiguous glitches?
              </p>
            </div>

            <div class="frame-card">
              <div class="frame-tag">FRAME 3</div>
              <h3 class="frame-title">Competence &amp; Systemic Risk</h3>
              <p class="frame-desc">
                Was this an unavoidable black-swan event or gross operational negligence? Does the market doubt long-term technical competence?
              </p>
            </div>

            <div class="frame-card">
              <div class="frame-tag">FRAME 4</div>
              <h3 class="frame-title">Fairness &amp; Remedies</h3>
              <p class="frame-desc">
                Are proposed refunds, credits, and remediation measures perceived as generous, adequate, or insulting deflections?
              </p>
            </div>
          </div>
        </section>

        <!-- Section 3: Multi-Round Cascade Dynamics -->
        <section id="cascade-dynamics" class="content-section">
          <div class="section-badge">03 // SEQUENTIAL CASCADES</div>
          <h2 class="section-heading">Find The Reaction Path Across Multi-Round Cascades</h2>
          <p class="section-intro">
            The first official corporate release is rarely the final word. Obrive Brain simulates how the story develops over three distinct temporal phases:
          </p>

          <div class="cascade-flow">
            <div class="cascade-stage">
              <div class="cascade-header">
                <span class="stage-num">ROUND 01</span>
                <span class="stage-time">0h - 12h Post-Event</span>
              </div>
              <h3 class="stage-title">Initial Shock &amp; Information Asymmetry</h3>
              <p class="stage-text">
                Directly impacted customers react on social channels and support queues. Unanswered questions breed speculation. Early defenders clash with affected users.
              </p>
            </div>

            <div class="cascade-stage">
              <div class="cascade-header">
                <span class="stage-num">ROUND 02</span>
                <span class="stage-time">12h - 48h Post-Event</span>
              </div>
              <h3 class="stage-title">Media Amplification &amp; Institutional Scrutiny</h3>
              <p class="stage-text">
                Tech reporters, security researchers, and industry competitors analyze executive statements for contradictions. Regulatory inquiries and class-action inquiries emerge.
              </p>
            </div>

            <div class="cascade-stage">
              <div class="cascade-header">
                <span class="stage-num">ROUND 03</span>
                <span class="stage-time">48h - 120h Post-Event</span>
              </div>
              <h3 class="stage-title">Consensus Crystallization &amp; Churn Fallout</h3>
              <p class="stage-text">
                The lasting public narrative sets in. Enterprise procurement reviews, contract cancellation notices, and long-term brand equity adjustments take hold.
              </p>
            </div>
          </div>
        </section>

        <!-- Section 4: What the Stress-Test Report Shows -->
        <section class="content-section">
          <div class="section-badge">04 // REPORT SIGNALS</div>
          <h2 class="section-heading">The Stress-Test Report Exposes The Pressure Structure</h2>

          <div class="signals-grid">
            <div class="signal-card">
              <h3 class="signal-title">Vulnerable Leadership Commitments</h3>
              <p class="signal-text">
                Highlights specific sentences in your draft statement that promise outcomes or timelines that could backfire if future facts contradict them.
              </p>
            </div>

            <div class="signal-card">
              <h3 class="signal-title">De-escalation Levers</h3>
              <p class="signal-text">
                Identifies which specific proactive concessions (e.g. independent audits, transparent post-mortems, full refunds) neutralize media outrage most effectively.
              </p>
            </div>

            <div class="signal-card">
              <h3 class="signal-title">Media Framing Vectors</h3>
              <p class="signal-text">
                Anticipates the exact headlines, interview angles, and investigative hooks trade publications will pursue based on the current evidence packet.
              </p>
            </div>

            <div class="signal-card">
              <h3 class="signal-title">Internal Employee Morale Fallout</h3>
              <p class="signal-text">
                Models how engineering, customer support, and sales teams interpret executive handling, surfacing internal dissent and retention risks early.
              </p>
            </div>
          </div>
        </section>

        <!-- Prompt Launcher -->
        <section class="prompt-launcher-section">
          <div class="launcher-card">
            <div class="launcher-header">
              <span class="launcher-tag">PRE-LOADED CRISIS / POLICY PROMPT</span>
              <span class="launcher-ready">Ready for Execution</span>
            </div>
            <div class="prompt-code-box">
              <p class="prompt-text">
                "Simulate public, media, and enterprise customer reactions across 3 rounds to our upcoming data retention policy update. Model 20 distinct agents representing Enterprise Security Officers, Tech Privacy Advocates, Financial Regulators, and Trade Journalists. Evaluate our draft announcement statement, identify wording that triggers regulatory scrutiny, and suggest 3 de-escalation modifications."
              </p>
            </div>
            <div class="launcher-actions">
              <AnimatedButton
                type="button"
                variant="primary"
                size="default"
                :iconSize="13"
                arrowColor="default"
                @click="launchOpinionConsole"
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

const launchOpinionConsole = () => {
  router.push({
    path: '/console',
    query: {
      prompt: 'Simulate public opinion, media amplification, and regulatory reaction to an incident announcement across 3 temporal rounds.',
      useCase: 'public-opinion'
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
  background: #dc2626;
  box-shadow: 0 0 6px #dc2626;
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

/* Frames Grid */
.frames-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .frames-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.frame-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.frame-tag {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  letter-spacing: 0.15em;
  color: #2d554c;
  margin-bottom: 0.5rem;
}

.frame-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.frame-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
}

/* Cascade Flow */
.cascade-flow {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cascade-stage {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.75rem;
}

.cascade-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.stage-num {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 13px;
  letter-spacing: 0.1em;
  color: #073933;
}

.stage-time {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  background: rgba(7, 57, 51, 0.08);
  color: #073933;
  padding: 3px 8px;
  border-radius: 4px;
}

.stage-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.stage-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 20px;
  color: #163830;
  margin: 0;
}

/* Signals Grid */
.signals-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .signals-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.signal-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.signal-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.signal-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
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
