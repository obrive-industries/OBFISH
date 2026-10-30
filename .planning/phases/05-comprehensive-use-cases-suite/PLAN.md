# Phase 05: Comprehensive Use Cases Suite — Execution Plan

## Goal
Build full-fidelity, dedicated detail pages for all remaining use cases on the platform, matching Obrive's signature UI/UX, mint background (`#A2F1DF`), `Microgramma` and `Michroma` typography, and explicit scoped CSS. Update `UseCasesView.vue` so that every scenario card features both an active `Explore View →` link and a `Run Simulation ⚡` CTA.

---

## Task 1: Comprehensive Use Cases Data Registry
**Files:**
- `frontend/src/data/useCasesRegistry.js` (New)

**Implementation Details:**
1. Create a rich, strongly-typed scenario dataset containing complete domain configurations for:
   - `stakeholder-simulation-ai` (Stakeholder Simulation AI)
   - `pricing-strategy-simulation` (Pricing Strategy & Elasticity Simulation)
   - `business-war-gaming-ai` (AI Business War Gaming)
   - `crisis-simulation-ai` (Crisis PR & Incident Simulation)
   - `synthetic-users` (Synthetic User Research & Personas)
   - `policy-impact-simulation-ai` (Policy Impact Simulation AI)
   - `scenario-planning-engine` (Scenario Planning & Bull Shock Engine)
   - `go-to-market-testing` (Go-To-Market Testing & Launch Readiness)
   - `narrative-forecasting-ai` (Narrative Forecasting & Story Worlds)
   - `decision-simulation-ai` (AI Decision Simulation)
   - `organizational-change-simulation` (Organizational Change Simulation)
   - `competitive-war-gaming` (Competitive War Gaming)
   - `customer-journey-research` (Customer Journey Research & Friction)
   - `financial-forecasting` (Financial Runway & Macro Shock Simulation)
   - `consumer-sentiment-analysis` (Consumer Sentiment & Review Analysis)
2. Each scenario object must include:
   - `slug`: Unique URL parameter
   - `title`: H1 title (`Microgramma Bold`)
   - `category`: Category identifier (`market`, `opinion`, `strategy`, `sports`)
   - `categoryLabel`: Eyebrow tag label
   - `badgeClass`: Color theme modifier for badge
   - `heroLead`: Executive value proposition summary
   - `disclaimer`: Contextual guidance statement
   - `evidenceInputs`: 4 structured cards (`icon`, `title`, `text`)
   - `decisionScenarios`: 4 actionable decision contexts (`number`, `title`, `text`)
   - `engineSteps`: 3 multi-agent architecture milestones
   - `reportSignals`: 4 key analytical deliverables
   - `comparisonRows`: 4 comparative dimensions vs. naive chatbots
   - `preloadedPrompt`: Exact analytical brief for `/console?prompt=...`

---

## Task 2: Universal Scenario Detail View Component
**Files:**
- `frontend/src/views/usecases/UseCaseDetailView.vue` (New)

**Implementation Details:**
1. Create `UseCaseDetailView.vue` with native Obrive styling:
   - Dynamic route binding via `vue-router` (`/use-cases/:slug`).
   - Breadcrumb navigation (`← All Use Cases / {Scenario Title}`).
   - Header with `LandingHeader` and footer with `LandingFooter`.
   - Hero section with pulse indicator, category eyebrow, H1 title, lead text, and action buttons:
     - `Run Simulation in Console ⚡` (links to `/console?prompt={encodedPrompt}&useCase={slug}`).
     - `Explore Architecture ↓` (smooth scroll to engine section).
   - Section 1: **Evidence Requirements** (4 responsive cards with icon, title, description).
   - Section 2: **Key Decision Scenarios** (4 numbered cards).
   - Section 3: **Multi-Agent Simulation Architecture** (3-step timeline).
   - Section 4: **Deliverable Report Anatomy** (4 signal cards).
   - Section 5: **Why Multi-Agent Outperforms Simple Chatbots** (Comparison table).
   - Section 6: **Pre-loaded Simulation Prompt Box** with 1-click execution.
   - Fallback / 404 state if unknown slug is accessed, with a clean button back to `/use-cases`.
   - All styling explicitly encapsulated in `<style scoped>` (no reliance on uncompiled Tailwind utility classes).

---

## Task 3: Router Integration for Dynamic Scenario Routing
**Files:**
- `frontend/src/router/index.js`

**Implementation Details:**
1. Register `/use-cases/:slug` route pointing to `UseCaseDetailView.vue`:
   - Keep specialized routes (`market-simulation-ai`, `public-opinion-simulation-ai`, `world-cup-prediction`) registered first so they take precedence.
   - Route `/use-cases/:slug` catches all other use case slugs dynamically.
2. Verify route transitions and scroll behavior (scrolls smoothly to top on navigation).

---

## Task 4: Hub View Card Updates (`UseCasesView.vue`)
**Files:**
- `frontend/src/views/UseCasesView.vue`

**Implementation Details:**
1. Import `useCasesRegistry` or link all scenario objects in `scenarios` array to their respective `/use-cases/:slug` routes.
2. Mark `isDedicatedPage: true` on all cards.
3. Verify that every single scenario card displays both:
   - `Explore View →` (links to `/use-cases/:slug`)
   - `Run Simulation ⚡` (launches in console with pre-loaded prompt)
4. Ensure search filtering and category pills seamlessly filter the expanded card directory.

---

## Task 5: Build Verification, Headless Screenshots & Git Hygiene
**Implementation Details:**
1. Run `npm --prefix frontend run build` to verify clean production compilation (0 errors).
2. Capture headless Chromium screenshots of:
   - `/use-cases` (showing `Explore View →` active on all cards).
   - `/use-cases/stakeholder-simulation-ai`
   - `/use-cases/business-war-gaming-ai`
   - `/use-cases/pricing-strategy-simulation`
   - `/use-cases/crisis-simulation-ai`
3. Verify backend test suite remains green (`PYTHONPATH=. uv run pytest tests`).
4. **STRICT DIRECTIVE**: Do NOT push to git (`git push` held until explicit approval).
