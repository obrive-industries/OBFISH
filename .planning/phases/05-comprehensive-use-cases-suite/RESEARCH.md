# Phase 05: Comprehensive Use Cases Suite — Research & Architecture Analysis

## 1. Context & User Directive
The user uploaded a screenshot of the Use Cases Hub (`/use-cases`), highlighting that while the flagship 3 use cases (Market Simulation, Public Opinion, World Cup Prediction) have dedicated `Explore View →` deep-dive pages, the other 9+ use cases in the grid only feature `Run Simulation ⚡`.

The user request:
> *"ye jo baki use cases hai unke bhi pages bana do /gsd-plan-phase"*

Every single use case must have its own dedicated detail page with:
- `Explore View →` link active on every card on `/use-cases`.
- Full-fidelity deep dive page matching Obrive's brand system:
  - Signature mint background `#A2F1DF`
  - `font-microgramma` / `Microgramma Bold` for headings
  - `Michroma` for body copy, badges, and metadata
  - Explicit scoped CSS for all layout containers, grids, and responsive media queries
  - Structured sections:
    1. Breadcrumb navigation (`← All Use Cases / [Use Case Title]`)
    2. Hero with category eyebrow, value proposition, and dual CTAs (`Run in Console ⚡`, `Explore Architecture ↓`)
    3. Evidence Input Matrix (4 structured domain cards)
    4. Key Decision Scenarios (4 actionable contexts)
    5. Multi-Agent Engine Architecture Timeline (3 sequential phases)
    6. Deliverable Report Signals (Consensus Trajectory, Fragile Assumptions, Turning Points, Reversal Conditions)
    7. Multi-Agent Swarm vs Single Chatbot comparison table
    8. Interactive pre-loaded simulation prompt launcher connecting directly to `/console?prompt=...`

---

## 2. Architectural Design: Registry + Dynamic Detail View Pattern

### The Anti-Pattern to Avoid: 15+ Duplicate Static Files
Creating 15 separate `.vue` files with identical markup layout leads to:
- 15x CSS duplication (over 10,000 lines of repetitive scoped CSS)
- High risk of desynchronized design updates
- Huge maintenance overhead

### The Scalable Pattern: Specialized Views + Universal Detail View
1. **Specialized Views (Existing)**:
   - `MarketSimulationView.vue` (`/use-cases/market-simulation-ai`)
   - `PublicOpinionView.vue` (`/use-cases/public-opinion-simulation-ai`)
   - `WorldCupPredictionView.vue` (`/use-cases/world-cup-prediction`, includes `#prediction-lab`)
2. **Centralized Data Registry (`frontend/src/data/useCasesRegistry.js`)**:
   Contains rich, strongly typed data for all use cases:
   - `stakeholder-simulation-ai` (Stakeholder Simulation AI)
   - `pricing-strategy-simulation` (Pricing Strategy & Elasticity Simulation)
   - `business-war-gaming-ai` (AI Business War Gaming)
   - `crisis-simulation-ai` (Crisis PR & Incident Simulation)
   - `synthetic-users` (Synthetic User Research & Personas)
   - `policy-impact-simulation-ai` (Policy Impact Simulation AI)
   - `scenario-planning-engine` (Scenario Planning & Bull Shock Engine)
   - `gtm-launch` / `go-to-market-testing` (Go-To-Market Testing & Launch Readiness)
   - `narrative-forecasting-ai` (Narrative Forecasting & Story Worlds)
   - Plus expanded catalog: `decision-simulation-ai`, `organizational-change-simulation`, `competitive-war-gaming`, `customer-journey-research`, `financial-forecasting`, `consumer-sentiment-analysis`.
3. **Universal Detail View (`frontend/src/views/usecases/UseCaseDetailView.vue`)**:
   - Dynamic route: `/use-cases/:slug`
   - Evaluates `route.params.slug`, retrieves data from `useCasesRegistry`, and renders the complete Obrive-styled page.
   - If an invalid slug is passed, displays a friendly "Scenario Not Found" state with a button back to `/use-cases`.
4. **Router Configuration (`frontend/src/router/index.js`)**:
   - `/use-cases/market-simulation-ai` -> `MarketSimulationView.vue`
   - `/use-cases/public-opinion-simulation-ai` -> `PublicOpinionView.vue`
   - `/use-cases/world-cup-prediction` -> `WorldCupPredictionView.vue`
   - `/use-cases/:slug` -> `UseCaseDetailView.vue` (handles all other use cases seamlessly).

---

## 3. Hub View Integration (`UseCasesView.vue`)
- Update every scenario in `scenarios` array with `customRoute: /use-cases/${item.slug}` and `isDedicatedPage: true`.
- Every card in the grid will now render both:
  - `Explore View →` (linking to its dedicated deep-dive page)
  - `Run Simulation ⚡` (launching directly in Console)

---

## 4. Verification Gates
1. Vite production build passes with 0 errors.
2. Headless Chromium screenshots of multiple dynamic use cases (`/use-cases/stakeholder-simulation-ai`, `/use-cases/business-war-gaming-ai`, `/use-cases/pricing-strategy-simulation`, `/use-cases/crisis-simulation-ai`).
3. Screenshot of updated `/use-cases` grid demonstrating `Explore View →` active on all cards.
4. Backend automated test suite remains 100% passing.
5. Strict adherence to Git Hygiene: **NO GIT PUSH**.
