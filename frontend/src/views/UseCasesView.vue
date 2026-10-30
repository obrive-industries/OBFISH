<template>
  <div class="usecases-page-root">
    <!-- Header -->
    <LandingHeader @open-auth="openAuthModal" />

    <main class="usecases-main">
      <div class="container-main">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="eyebrow-pill">
            <span class="pulse-dot"></span>
            <span>SIMULATION USE CASES &amp; SCENARIO ENGINE</span>
          </div>

          <h1 class="hero-title">
            EXPLORE REAL-WORLD<br />SIMULATION PATHS
          </h1>

          <p class="hero-subtitle">
            Pick the kind of future you want to stress-test. Every path runs on the same evidence-grounded MiroFish multi-agent simulation engine: bring source material, generate actor graphs, observe multi-round interaction dynamics, and extract decision reports.
          </p>

          <!-- Interactive Search & Filter Controls -->
          <div class="controls-card">
            <div class="search-box">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search scenarios (e.g. pricing, launch, crisis, sports, policy)..."
                class="search-input"
              />
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="clear-search-btn"
                title="Clear search"
              >
                ✕
              </button>
            </div>

            <div class="filter-pills">
              <button
                v-for="cat in categories"
                :key="cat.id"
                @click="activeCategory = cat.id"
                class="filter-pill-btn"
                :class="{ active: activeCategory === cat.id }"
              >
                {{ cat.label }}
              </button>
            </div>
          </div>
        </section>

        <!-- Featured Flagship Use Cases -->
        <section class="featured-section" v-if="activeCategory === 'all' && !searchQuery">
          <div class="section-label-row">
            <span class="section-tag">FLAGSHIP USE CASES</span>
            <span class="section-hint">Deep interactive workflows &amp; specialized models</span>
          </div>

          <div class="featured-grid">
            <!-- Market Simulation -->
            <router-link to="/use-cases/market-simulation-ai" class="featured-card">
              <div class="card-badge market-badge">MARKET &amp; GTM</div>
              <h2 class="featured-card-title">Market Simulation AI</h2>
              <p class="featured-card-desc">
                Stress-test product launches, pricing changes, competitor counter-strategies, and consumer adoption before the public story forms around the decision.
              </p>
              <div class="card-features">
                <span>• Pricing Elasticity</span>
                <span>• Competitor War Gaming</span>
                <span>• Buyer Persona Friction</span>
              </div>
              <div class="card-action">
                <span>Deep Dive Specification</span>
                <span class="arrow-icon">→</span>
              </div>
            </router-link>

            <!-- Public Opinion -->
            <router-link to="/use-cases/public-opinion-simulation-ai" class="featured-card">
              <div class="card-badge opinion-badge">REPUTATION &amp; CRISIS</div>
              <h2 class="featured-card-title">Public Opinion Simulation AI</h2>
              <p class="featured-card-desc">
                Model how media, regulators, institutions, and online communities reshape an incident, policy change, or corporate statement over multi-round cascades.
              </p>
              <div class="card-features">
                <span>• Multi-Round Narrative Cascades</span>
                <span>• De-escalation Vectors</span>
                <span>• Trust Risk Auditing</span>
              </div>
              <div class="card-action">
                <span>Deep Dive Specification</span>
                <span class="arrow-icon">→</span>
              </div>
            </router-link>

            <!-- World Cup Prediction Lab -->
            <router-link to="/use-cases/world-cup-prediction" class="featured-card featured-highlight">
              <div class="card-badge sports-badge">SPORTS &amp; FORECASTING</div>
              <h2 class="featured-card-title">2026 World Cup Prediction Lab</h2>
              <p class="featured-card-desc">
                Construct an evidence-led tournament forecast from tactical scouting, squad depth, and tournament pressure with our live interactive match builder.
              </p>
              <div class="card-features">
                <span>• Interactive Fixture Builder</span>
                <span>• Turning Point Modeling</span>
                <span>• Tactical Narrative Paths</span>
              </div>
              <div class="card-action">
                <span>Launch Prediction Lab</span>
                <span class="arrow-icon">→</span>
              </div>
            </router-link>
          </div>
        </section>

        <!-- Full Scenario Library Grid -->
        <section class="library-section">
          <div class="section-label-row">
            <span class="section-tag">SCENARIO DIRECTORY ({{ filteredScenarios.length }})</span>
            <span class="section-hint">Select any scenario to inspect or launch in the engine</span>
          </div>

          <div v-if="filteredScenarios.length === 0" class="empty-state">
            <p>No scenarios found matching "{{ searchQuery }}".</p>
            <button @click="resetFilters" class="reset-filter-btn">Reset Filters</button>
          </div>

          <div v-else class="scenarios-grid">
            <div
              v-for="item in filteredScenarios"
              :key="item.id"
              class="scenario-card"
            >
              <div class="scenario-card-header">
                <span class="scenario-tag">{{ item.categoryLabel }}</span>
                <span v-if="item.isDedicatedPage" class="dedicated-pill">Interactive View</span>
              </div>

              <h3 class="scenario-title">{{ item.title }}</h3>
              <p class="scenario-desc">{{ item.description }}</p>

              <div class="scenario-footer">
                <AnimatedButton
                  v-if="item.customRoute"
                  :to="item.customRoute"
                  variant="outline"
                  size="sm"
                  :iconSize="11"
                  arrowColor="primary"
                >
                  Explore View
                </AnimatedButton>

                <AnimatedButton
                  type="button"
                  variant="primary"
                  size="sm"
                  :iconSize="11"
                  arrowColor="default"
                  class="flex-1"
                  @click="launchInConsole(item.prompt)"
                >
                  Run Simulation
                </AnimatedButton>
              </div>
            </div>
          </div>
        </section>

        <!-- 4-Step MiroFish Engine Workflow Banner -->
        <section class="workflow-banner">
          <div class="workflow-header">
            <span class="workflow-eyebrow">THE SIMULATION ARCHITECTURE</span>
            <h2 class="workflow-title">Every Use Case Follows The Same Grounded Engine</h2>
            <p class="workflow-desc">
              The scenario changes the question. The engine executes through rigorous multi-agent evidence grounding.
            </p>
          </div>

          <div class="workflow-steps-grid">
            <div class="workflow-step-card">
              <div class="step-num">01</div>
              <h3 class="step-title">Source Evidence Packet</h3>
              <p class="step-desc">
                Input your brief, memo, transcripts, public URL, or raw data. The engine extracts verifiable claims and explicit constraints.
              </p>
            </div>

            <div class="workflow-step-card">
              <div class="step-num">02</div>
              <h3 class="step-title">Actor Graph Construction</h3>
              <p class="step-desc">
                Generates specialized agent personas with bounded incentives, psychological profiles, and asymmetric information access.
              </p>
            </div>

            <div class="workflow-step-card">
              <div class="step-num">03</div>
              <h3 class="step-title">Multi-Round Simulation</h3>
              <p class="step-desc">
                Agents interact across sequential rounds. Memory, social feedback loops, and second-order reactions emerge organically.
              </p>
            </div>

            <div class="workflow-step-card">
              <div class="step-num">04</div>
              <h3 class="step-title">Analytical Report</h3>
              <p class="step-desc">
                Extracts consensus paths, vulnerable assumptions, decisive turning points, and new evidence required to reverse outcomes.
              </p>
            </div>
          </div>
        </section>

        <!-- Bottom CTA -->
        <section class="cta-section">
          <div class="cta-inner">
            <h2 class="cta-title">Turn Your Strategic Questions Into Inspectable Paths</h2>
            <p class="cta-text">
              Rehearse complex real-world decisions before public execution. Get started with our live multi-agent simulation console.
            </p>
            <div class="cta-btn-group">
              <AnimatedButton
                to="/console"
                variant="accent"
                size="default"
                :iconSize="13"
                arrowColor="primary"
              >
                Launch Live Console
              </AnimatedButton>
              <AnimatedButton
                to="/pricing"
                variant="outline-white"
                size="default"
                :iconSize="13"
                arrowColor="white"
              >
                View Access Plans
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import LandingHeader from '../components/landing/LandingHeader.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'
import AuthModal from '../components/AuthModal.vue'
import AnimatedButton from '../components/common/AnimatedButton.vue'

const router = useRouter()
const showAuthModal = ref(false)
const searchQuery = ref('')
const activeCategory = ref('all')

const openAuthModal = () => {
  showAuthModal.value = true
}

const categories = [
  { id: 'all', label: 'All Scenarios' },
  { id: 'market', label: 'Market & GTM' },
  { id: 'opinion', label: 'Public Opinion & PR' },
  { id: 'sports', label: 'Sports & Forecasting' },
  { id: 'strategy', label: 'Strategic Planning' }
]

const scenarios = [
  {
    id: 'market-simulation',
    title: 'Market Simulation AI',
    category: 'market',
    categoryLabel: 'Market & GTM',
    description: 'Stress-test launches, pricing models, competitors, and market entry before the public story forms around your brand.',
    customRoute: '/use-cases/market-simulation-ai',
    isDedicatedPage: true,
    prompt: 'Conduct a market simulation on our upcoming product launch, evaluating buyer resistance and competitor reaction.'
  },
  {
    id: 'public-opinion',
    title: 'Public Opinion Simulation AI',
    category: 'opinion',
    categoryLabel: 'Public Opinion & PR',
    description: 'Model how media, regulators, institutions, and online audiences reshape an incident or policy change.',
    customRoute: '/use-cases/public-opinion-simulation-ai',
    isDedicatedPage: true,
    prompt: 'Simulate public and media reaction across 3 rounds to our revised terms of service and data policy.'
  },
  {
    id: 'world-cup',
    title: 'World Cup 2026 Prediction Lab',
    category: 'sports',
    categoryLabel: 'Sports & Forecasting',
    description: 'Build an evidence-led tournament forecast from tactical scouting reports, squad depth, and tournament pressure.',
    customRoute: '/use-cases/world-cup-prediction',
    isDedicatedPage: true,
    prompt: 'Forecast the tactical match path and decisive turning points between Argentina and France in the 2026 knockout stage.'
  },
  {
    id: 'stakeholder-simulation',
    title: 'Stakeholder Simulation AI',
    category: 'strategy',
    categoryLabel: 'Strategic Planning',
    description: 'Rehearse how executives, board members, employees, partners, and regulators react to major strategic shifts.',
    customRoute: '/use-cases/stakeholder-simulation-ai',
    isDedicatedPage: true,
    prompt: 'Model executive and employee reactions to an organizational restructuring and remote work policy update.'
  },
  {
    id: 'pricing-elasticity',
    title: 'Pricing Strategy & Elasticity Simulation',
    category: 'market',
    categoryLabel: 'Market & GTM',
    description: 'Simulate buyer objections, package migration risk, discount elasticity, and competitor price counter-positioning.',
    customRoute: '/use-cases/pricing-strategy-simulation',
    isDedicatedPage: true,
    prompt: 'Evaluate buyer willingness to pay and churn risk if we migrate from flat pricing to usage-based billing tiers.'
  },
  {
    id: 'business-war-gaming',
    title: 'AI Business War Gaming',
    category: 'strategy',
    categoryLabel: 'Strategic Planning',
    description: 'Rehearse evidence-grounded moves, counter-moves, and defensive response triggers across several strategic rounds.',
    customRoute: '/use-cases/business-war-gaming-ai',
    isDedicatedPage: true,
    prompt: 'Execute a multi-round business war game modeling competitor reactions to our new enterprise AI offering.'
  },
  {
    id: 'crisis-pr-simulation',
    title: 'Crisis PR & Incident Simulation',
    category: 'opinion',
    categoryLabel: 'Public Opinion & PR',
    description: 'Stress-test incident statements, spokesperson messaging, journalist inquiries, and social escalation paths.',
    customRoute: '/use-cases/crisis-simulation-ai',
    isDedicatedPage: true,
    prompt: 'Stress-test our emergency PR response to a service disruption affecting enterprise SLA clients.'
  },
  {
    id: 'synthetic-users',
    title: 'Synthetic User Research & Personas',
    category: 'market',
    categoryLabel: 'Market & GTM',
    description: 'Ground AI actors in customer interviews and review logs to rehearse user research questions prior to fieldwork.',
    customRoute: '/use-cases/synthetic-users',
    isDedicatedPage: true,
    prompt: 'Generate synthetic B2B enterprise personas to evaluate onboarding friction in our new dashboard.'
  },
  {
    id: 'policy-impact',
    title: 'Policy Impact Simulation AI',
    category: 'opinion',
    categoryLabel: 'Public Opinion & PR',
    description: 'Test stakeholder interpretation, compliance friction, fairness narratives, and rollout gaps before policy release.',
    customRoute: '/use-cases/policy-impact-simulation-ai',
    isDedicatedPage: true,
    prompt: 'Assess stakeholder impact and compliance hurdles for our new global content moderation policy.'
  },
  {
    id: 'scenario-planning',
    title: 'Scenario Planning & Bull Shock Engine',
    category: 'strategy',
    categoryLabel: 'Strategic Planning',
    description: 'Compare multiple future paths, inject catalyst shocks, and inspect prediction market sensitivities.',
    customRoute: '/use-cases/scenario-planning-engine',
    isDedicatedPage: true,
    prompt: 'Model baseline vs bull shock scenarios for renewable energy regulatory adoption over the next 24 months.'
  },
  {
    id: 'gtm-launch',
    title: 'Go-To-Market Testing & Launch Readiness',
    category: 'market',
    categoryLabel: 'Market & GTM',
    description: 'Simulate audience sequence, messaging proof gaps, channel friction, and early adopter conversion velocity.',
    customRoute: '/use-cases/go-to-market-testing',
    isDedicatedPage: true,
    prompt: 'Stress-test our go-to-market rollout across developer channels and identify our top three messaging blind spots.'
  },
  {
    id: 'narrative-forecasting',
    title: 'Narrative Forecasting & Story Worlds',
    category: 'sports',
    categoryLabel: 'Sports & Forecasting',
    description: 'Treat complex narratives and cultural events as graphs of motives, memory, and tension to test trajectory shifts.',
    customRoute: '/use-cases/narrative-forecasting-ai',
    isDedicatedPage: true,
    prompt: 'Forecast how a surprise trade or transfer deadline move will shift team chemistry and fan sentiment.'
  }
]

const filteredScenarios = computed(() => {
  return scenarios.filter(item => {
    const matchesCat = activeCategory.value === 'all' || item.category === activeCategory.value
    const matchesSearch = !searchQuery.value.trim() ||
      item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.categoryLabel.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCat && matchesSearch
  })
})

const resetFilters = () => {
  searchQuery.value = ''
  activeCategory.value = 'all'
}

const launchInConsole = (promptText) => {
  router.push({
    path: '/console',
    query: { prompt: promptText }
  })
}
</script>

<style scoped>
.usecases-page-root {
  min-height: 100vh;
  background-color: #A2F1DF;
  color: #073933;
  display: flex;
  flex-direction: column;
}

.usecases-main {
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

/* Hero Section */
.hero-section {
  text-align: center;
  padding-top: 2rem;
  padding-bottom: 3.5rem;
  max-width: 58rem;
  margin-left: auto;
  margin-right: auto;
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
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.05);
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00e5a3;
  box-shadow: 0 0 6px #00e5a3;
}

.hero-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.6rem, 3.2vw, 2.25rem);
  line-height: 1.18;
  color: #073933;
  margin-bottom: 1.25rem;
  letter-spacing: 0.02em;
}

.hero-subtitle {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 14px;
  line-height: 24px;
  color: #163830;
  margin-bottom: 2.5rem;
}

/* Controls Card */
.controls-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.25rem;
  padding: 1.25rem;
  box-shadow: 0 8px 30px rgba(7, 57, 51, 0.08);
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  width: 18px;
  height: 18px;
  color: #2d554c;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.85rem 2.8rem 0.85rem 3rem;
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 0.75rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  color: #073933;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: #073933;
  box-shadow: 0 0 0 3px rgba(7, 57, 51, 0.12);
}

.clear-search-btn {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  font-size: 14px;
  color: #2d554c;
  cursor: pointer;
}

.filter-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.filter-pill-btn {
  padding: 0.45rem 1rem;
  border-radius: 9999px;
  border: 1px solid rgba(7, 57, 51, 0.15);
  background: rgba(255, 255, 255, 0.6);
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  letter-spacing: 0.08em;
  color: #163830;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill-btn:hover {
  background: #ffffff;
  border-color: #073933;
}

.filter-pill-btn.active {
  background: #073933;
  color: #ffffff;
  border-color: #073933;
}

/* Section Header */
.section-label-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(7, 57, 51, 0.15);
  padding-bottom: 0.75rem;
}

.section-tag {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.14em;
  color: #073933;
}

.section-hint {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  color: #2d554c;
}

/* Featured Section */
.featured-section {
  margin-bottom: 4rem;
}

.featured-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .featured-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.featured-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.25rem;
  padding: 1.75rem;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(7, 57, 51, 0.05);
}

.featured-card:hover {
  transform: translateY(-4px);
  border-color: #073933;
  box-shadow: 0 12px 32px rgba(7, 57, 51, 0.15);
}

.featured-highlight {
  border: 2px solid #073933;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
}

.card-badge {
  align-self: flex-start;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  letter-spacing: 0.12em;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
  margin-bottom: 1rem;
}

.market-badge {
  background: rgba(7, 57, 51, 0.1);
  color: #073933;
}

.opinion-badge {
  background: rgba(220, 38, 38, 0.1);
  color: #991b1b;
}

.sports-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #065f46;
}

.featured-card-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #073933;
  margin-bottom: 0.75rem;
  line-height: 1.25;
}

.featured-card-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 20px;
  color: #163830;
  flex-grow: 1;
  margin-bottom: 1.25rem;
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  color: #2d554c;
  margin-bottom: 1.5rem;
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid rgba(7, 57, 51, 0.1);
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #073933;
}

.arrow-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.featured-card:hover .arrow-icon {
  transform: translateX(4px);
}

/* Library Section */
.library-section {
  margin-bottom: 4rem;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 640px) {
  .scenarios-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .scenarios-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.scenario-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.scenario-card:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(7, 57, 51, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(7, 57, 51, 0.08);
}

.scenario-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.scenario-tag {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 10px;
  letter-spacing: 0.12em;
  color: #2d554c;
  text-transform: uppercase;
  font-weight: 600;
}

.dedicated-pill {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 9px;
  background: #073933;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 4px;
}

.scenario-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  color: #073933;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.scenario-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
  flex-grow: 1;
  margin-bottom: 1.25rem;
}

.scenario-footer {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(7, 57, 51, 0.08);
}

.scenario-btn {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  border-radius: 0.5rem;
  padding: 0.4rem 0.75rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
  text-align: center;
}

.view-btn {
  background: transparent;
  color: #073933;
  border: 1px solid #073933;
}

.view-btn:hover {
  background: rgba(7, 57, 51, 0.08);
}

.console-btn {
  background: #073933;
  color: #ffffff;
  border: 1px solid #073933;
  flex-grow: 1;
}

.console-btn:hover {
  background: #042823;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
}

.reset-filter-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.25rem;
  background: #073933;
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  cursor: pointer;
}

/* Workflow Banner */
.workflow-banner {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(7, 57, 51, 0.15);
  border-radius: 1.5rem;
  padding: 3rem 2rem;
  margin-bottom: 4rem;
}

.workflow-header {
  text-align: center;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 2.5rem;
}

.workflow-eyebrow {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 11px;
  letter-spacing: 0.2em;
  color: #2d554c;
  display: block;
  margin-bottom: 0.5rem;
}

.workflow-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.2rem, 2.2vw, 1.55rem);
  color: #073933;
  line-height: 1.25;
  margin-bottom: 0.75rem;
}

.workflow-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 22px;
  color: #163830;
}

.workflow-steps-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 640px) {
  .workflow-steps-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .workflow-steps-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.workflow-step-card {
  background: #ffffff;
  border: 1px solid rgba(7, 57, 51, 0.12);
  border-radius: 1rem;
  padding: 1.5rem;
}

.step-num {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 24px;
  line-height: 36px;
  color: rgb(7, 57, 51);
  margin-bottom: 0.75rem;
}

.step-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #073933;
  margin-bottom: 0.5rem;
}

.step-desc {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 19px;
  color: #163830;
}

/* CTA Section */
.cta-section {
  text-align: center;
  background: #073933;
  border-radius: 1.5rem;
  padding: 3.5rem 2rem;
  color: #ffffff;
  box-shadow: 0 16px 40px rgba(7, 57, 51, 0.25);
}

.cta-inner {
  max-width: 44rem;
  margin-left: auto;
  margin-right: auto;
}

.cta-title {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: clamp(1.25rem, 2.5vw, 1.75rem);
  line-height: 1.25;
  margin-bottom: 1rem;
  color: #ffffff;
}

.cta-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 22px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}

.cta-btn-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.cta-primary-btn {
  display: inline-flex;
  align-items: center;
  padding: 0.85rem 1.75rem;
  background: #A2F1DF;
  color: #073933;
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: 0.75rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-primary-btn:hover {
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(162, 241, 223, 0.4);
}

.cta-secondary-btn {
  display: inline-flex;
  align-items: center;
  padding: 0.85rem 1.75rem;
  background: transparent;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.4);
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: 0.75rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}
</style>
