# Phase 04: Native Use Cases Suite & Scalable Footer Architecture — Execution Plan

## Goal
Design and implement dedicated, native MiroFish/Obrive Brain simulation use case pages matching the platform's visual design system, typography (`Microgramma` for headings, `Michroma` for body), and color palette (`#073933`, `#A2F1DF`, `#ffffff`). Refactor `LandingFooter.vue` into a scalable 4-column architecture to cleanly display all product, solutions, and legal links without visual clutter.

---

## Task 1: Scalable Multi-Column Footer Architecture
**Files:**
- `frontend/src/components/landing/LandingFooter.vue`

**Implementation Details:**
1. Replace the single cramped horizontal line with a modern 4-column structured grid:
   - **Column 1 (Brand & Mission):**
     - Obrive logo (`/obrive-logo.svg`, 70x50px) + `BRAIN` brand text.
     - Brand mission: "Autonomous multi-agent simulation & predictive intelligence engine."
     - Social icons (LinkedIn, X/Twitter, Instagram) with `#073933` hover transitions.
   - **Column 2 (Solutions & Use Cases):**
     - Column header: `SOLUTIONS` (`Microgramma Bold`, uppercase, 12px, tracking-wider).
     - Links (`Michroma`, 13px, `#163830` with `#073933` hover):
       - All Use Cases (`/use-cases`)
       - Market Simulation AI (`/use-cases/market-simulation-ai`)
       - Public Opinion AI (`/use-cases/public-opinion-simulation-ai`)
       - 2026 Prediction Lab (`/use-cases/world-cup-prediction`)
   - **Column 3 (Platform & Product):**
     - Column header: `PLATFORM`.
     - Links:
       - Pricing & Plans (`/pricing`)
       - FAQs (`/faqs`)
       - Simulation Console (`/console`)
   - **Column 4 (Legal & Governance):**
     - Column header: `LEGAL`.
     - Links:
       - Terms of Service (`/terms`)
       - Privacy Policy (`/privacy`)
       - Refund Policy (`/refund`)
       - Wishlist Leads (`/admin/wishlist`, conditionally rendered for admin users).
2. Add bottom divider and centered copyright bar: `© 2026 Obrive Industries. All rights reserved.`
3. Add explicit scoped CSS rules (`.footer-grid { display: grid; grid-template-columns: repeat(4, 1fr); ... }`) with responsive media query collapsing gracefully to 2 columns on tablet and 1 column on mobile.

---

## Task 2: Use Cases Hub View (`UseCasesView.vue`)
**Files:**
- `frontend/src/views/UseCasesView.vue` (New)
- `frontend/src/router/index.js`

**Implementation Details:**
1. Create `frontend/src/views/UseCasesView.vue` matching the mint background (`#A2F1DF`) / cream card aesthetic:
   - **Header & Navigation**: Reusable `LandingHeader.vue` and `LandingFooter.vue`.
   - **Hero Section**:
     - Eyebrow tag: `USE CASES & SCENARIO ENGINE` (`font-michroma text-xs uppercase tracking-widest text-[#2d554c]`).
     - Headline: `EXPLORE REAL-WORLD SIMULATION PATHS` (`font-microgramma font-bold text-[#073933]`).
     - Subtitle: `Pick the kind of future you want to stress-test. Every path runs on the same evidence-grounded MiroFish multi-agent simulation engine.`
   - **Search & Category Filter Bar**:
     - Interactive filter pills: `All`, `Market & GTM`, `Public Opinion & PR`, `Sports & Forecasting`, `Strategic Planning`.
     - Live search filter allowing users to instantly find scenarios.
   - **Featured Priority Cards (3 Large Cards)**:
     - *Market Simulation AI*: "Stress-test launches, pricing, competitors, and market entry before the public story forms." -> Links to `/use-cases/market-simulation-ai`.
     - *Public Opinion Simulation AI*: "Model how institutions, media, affected groups, and observers reshape an incident or policy." -> Links to `/use-cases/public-opinion-simulation-ai`.
     - *World Cup 2026 Prediction Lab*: "Build an evidence-led match and tournament forecast from scouting reports and team dynamics." -> Links to `/use-cases/world-cup-prediction`.
   - **Expanded Simulation Library Grid (12 Cards)**:
     - Cards for Stakeholder Dynamics, Business War Gaming, Pricing Elasticity, Scenario Planning, Synthetic Users, Policy Impact, Customer Journey, etc.
     - Each card features: Tag, Title (`Microgramma`), Description (`Michroma`), and "Launch in Console" CTA (`/console?prompt=...`).
   - **The MiroFish 4-Step Simulation Engine Workflow Banner**:
     - Step 1: Input Evidence (Brief, PDF, Memo, URL).
     - Step 2: Graph Construction (Actors, Motives, Constraints).
     - Step 3: Multi-Round Agent Simulation (Interactions & Cascades).
     - Step 4: Analytical Synthesis (Turning points, Fragile assumptions, Reversal conditions).
   - **Bottom Call to Action**:
     - "Turn your questions into an inspectable simulation path" with a primary CTA button leading to `/console`.

---

## Task 3: Market Simulation AI View (`MarketSimulationView.vue`)
**Files:**
- `frontend/src/views/usecases/MarketSimulationView.vue` (New)
- `frontend/src/router/index.js`

**Implementation Details:**
1. Create `MarketSimulationView.vue` with native Obrive styling:
   - **Hero Section**:
     - Eyebrow: `SOLUTIONS / MARKET INTELLIGENCE`.
     - Title: `MARKET SIMULATION AI`.
     - Value proposition: Rehearse launches, pricing, competitive positioning, and consumer reception before capital deployment.
     - Action CTAs: `Run Market Simulation` (links to `/console?prompt=Market%20Simulation`) and `Explore Workflow`.
   - **Evidence Input Matrix (4 Interactive Cards)**:
     - 1. *Product Brief & Positioning*: Value props, target ICP, features, messaging angle.
     - 2. *Competitive Landscape*: Direct rivals, substitute products, pricing benchmarks.
     - 3. *Customer Voice & Research*: Interviews, review sentiment, price sensitivity signals.
     - 4. *Go-To-Market Plan*: Channels, launch timeline, promotional strategies.
   - **When to Use Market Simulation AI (4 Scenarios)**:
     - New Product Launch Readiness.
     - Pricing Model & Tier Changes.
     - Category / Regional Market Expansion.
     - Defensive Competitive Response.
   - **Simulation Engine Anatomy Section**:
     - Visual diagram of Agent Graph (Prospective Buyers, Incumbent Competitors, Tech Critics, Channel Partners) interacting over multiple rounds.
   - **Report Breakdown (What Obrive Brain Delivers)**:
     - Detailed explanation of Report sections: (1) Consensus Trajectory, (2) Vulnerable Assumptions, (3) Decisive Turning Points, (4) Catalyst Reversals.
   - **Difference vs Simple LLM Chatbots**:
     - Single Prompt LLM (superficial, hallucinated agreement, static) vs Obrive Brain Multi-Agent Swarm (competing incentives, private memory, multi-round debates, emergent dynamics).
   - **Direct Simulation Launcher**:
     - Interactive pre-filled simulation prompt card with 1-click launch into `/console`.

---

## Task 4: Public Opinion Simulation AI View (`PublicOpinionView.vue`)
**Files:**
- `frontend/src/views/usecases/PublicOpinionView.vue` (New)
- `frontend/src/router/index.js`

**Implementation Details:**
1. Create `PublicOpinionView.vue` matching Obrive visual tokens:
   - **Hero Section**:
     - Eyebrow: `SOLUTIONS / REPUTATION & CRISIS`.
     - Title: `PUBLIC OPINION SIMULATION AI`.
     - Subtitle: `Model how media, institutions, affected groups, and online communities may react to an incident, policy change, or public announcement.`
     - CTA: `Test Public Reaction` (`/console?prompt=Public%20Opinion%20Simulation`).
   - **Public Opinion as a System of Interpretation**:
     - Explains why simple sentiment analysis (positive/negative score) fails during complex events.
     - Focuses on narrative framing, responsibility attribution, institutional scrutiny, and virality vectors.
   - **Multi-Round Cascade Breakdown**:
     - *Round 1: Initial Reception & Information Void*: How initial messaging is received by directly affected parties.
     - *Round 2: Media Amplification & Expert Scrutiny*: Regulatory response, journalist inquiries, and opinion-leader framing.
     - *Round 3: Narrative Consensus & Secondary Backlash*: Emergence of lasting public sentiment and customer retention impact.
   - **Core Use Cases**:
     - Incident Response & Crisis Management.
     - Policy & Terms of Service Rollouts.
     - Leadership & Corporate Restructuring Announcements.
     - Brand Safety & Controversy Stress-Testing.
   - **Anatomy of the Stress-Test Report**:
     - Pressure structures, credibility risks, de-escalation triggers, and recommended mitigation actions.
   - **Interactive Quick-Test Card**:
     - Pre-configured policy/incident scenario with 1-click launch into `/console`.

---

## Task 5: World Cup Prediction Lab View (`WorldCupPredictionView.vue`)
**Files:**
- `frontend/src/views/usecases/WorldCupPredictionView.vue` (New)
- `frontend/src/router/index.js`

**Implementation Details:**
1. Create `WorldCupPredictionView.vue` with the interactive prediction lab:
   - **Hero Section**:
     - Eyebrow: `SOLUTIONS / EVENT FORECASTING`.
     - Title: `2026 WORLD CUP PREDICTION TOOL`.
     - Value proposition: `Build an evidence-led tournament forecast from tactical scouting, squad depth, and tournament pressure.`
     - Disclaimer notice: `Exploratory analytical simulation only. No live scores, bookmaker odds, or gambling advice.`
   - **Interactive Prediction Lab Component (`#prediction-lab`)**:
     - **Tournament Stage**: Interactive selector (`Group Stage`, `Round of 32`, `Round of 16`, `Quarter-final`, `Semi-final`, `Final`).
     - **Team Selection**: Team A vs Team B inputs with quick-select pills (Argentina, France, Brazil, England, Spain, Germany, Portugal, Netherlands, USA, Japan).
     - **Prediction Focus**: Options for `Match Outcome & Scoreline Path`, `Tactical Turning Points & Subs`, `Media & Fan Reaction Narrative`.
     - **Evidence Input**: Mock file dropzone ("Upload Match Brief or Tactical Notes") + source URL text input.
     - **Live Dynamic Simulation Brief Generator**:
       - Reactive preview box that continuously constructs the analytical simulation prompt as the user adjusts stage, teams, and focus!
     - **"Run in Simulation Engine" CTA**:
       - Navigates to `/console?prompt=${encodeURIComponent(dynamicBrief)}&useCase=world-cup` so the user can immediately execute the simulation in Obrive Brain!
   - **What a Robust Match Forecast Explains**:
     - 1. Match Trajectory (opening tactical shape vs second-half fatigue).
     - 2. Three Decisive Match Factors.
     - 3. Plausible Turning Points (injuries, VAR calls, tactical substitutions).
     - 4. Reversal Conditions (what new evidence or lineup changes would invert the forecast).
   - **Methodology & Sports Analytics FAQ**:
     - Accordion items answering how multi-agent modeling evaluates sports dynamics vs simple statistical averages.

---

## Task 6: Routing, Cross-Linking & Landing Integration
**Files:**
- `frontend/src/router/index.js`
- `frontend/src/components/landing/LandingUseCases.vue`

**Implementation Details:**
1. In `frontend/src/router/index.js`:
   - Register route `/use-cases` -> `UseCasesView.vue`.
   - Register route `/use-cases/market-simulation-ai` -> `MarketSimulationView.vue`.
   - Register route `/use-cases/public-opinion-simulation-ai` -> `PublicOpinionView.vue`.
   - Register route `/use-cases/world-cup-prediction` -> `WorldCupPredictionView.vue`.
   - Add alias `/world-cup-prediction` -> redirect to `/use-cases/world-cup-prediction`.
   - Ensure router's `scrollBehavior` handles hash links (`#prediction-lab`) smoothly.
2. In `LandingUseCases.vue` on homepage:
   - Add an elegant CTA banner below the 6 preview cards:
     `Explore All 100+ Specialized Simulation Use Cases →` linking directly to `/use-cases`.
3. Verify that `/console` handles incoming query parameters (`?prompt=...`) to pre-populate the input field.

---

## Task 7: Build Verification, Headless Browser Screenshots & Git Hygiene
**Implementation Details:**
1. Run `npm --prefix frontend run build` to verify clean compilation with 0 errors.
2. Test responsive layouts on mobile (375px), tablet (768px), and desktop (1280px).
3. Capture headless browser screenshots of:
   - `/use-cases`
   - `/use-cases/market-simulation-ai`
   - `/use-cases/public-opinion-simulation-ai`
   - `/use-cases/world-cup-prediction#prediction-lab`
   - Redesigned 4-column footer on all pages.
4. Verify backend remains fully operational (`http://localhost:5001`).
5. **STRICT DIRECTIVE**: Do NOT run `git push`. Keep all changes local and atomic.
