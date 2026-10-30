# Phase 04: Native Use Cases Suite & Scalable Footer Architecture — Research & Design Analysis

## 1. Context & Objective
The user requested bringing the core simulation use cases from `mirofish.my` into the native Obrive Brain platform, adhering strictly to Obrive's brand identity, typography, visual tokens, and UI/UX conventions, while thoughtfully restructuring the footer to prevent link crowding.

### Target Sources:
1. `https://mirofish.my/use-cases` (Hub / Overview)
2. `https://mirofish.my/use-cases/market-simulation-ai` (Market Simulation)
3. `https://mirofish.my/use-cases/public-opinion-simulation-ai` (Public Opinion & Crisis)
4. `https://mirofish.my/use-cases/world-cup-prediction#prediction-lab` (World Cup Forecast & Interactive Prediction Lab)

---

## 2. Brand & Design System Alignment (Obrive Standards)

### Color Palette
- **Hero / Page Background**: Signature mint `#A2F1DF` or clean white with subtle mint gradients.
- **Primary Brand / Heading Color**: `#073933` (Dark teal) & `#051f1a`.
- **Card Backgrounds**: `rgba(255, 255, 255, 0.75)` to `rgba(255, 255, 255, 0.95)` with `backdrop-filter: blur(16px)` and subtle borders `border: 1px solid rgba(7, 57, 51, 0.12)`.
- **Accent & Active State**: `#073933` with mint highlight (`#A2F1DF`), verified emerald dot (`#00e5a3`).

### Typography Standards
- **Headings (H1, H2, H3)**: `font-family: 'Microgramma', 'Microgramma Bold', sans-serif;` with bold weights and uppercase tracking where appropriate.
- **Body Copy, Paragraphs, Lists**: `font-family: Michroma, 'Michroma Fallback', sans-serif; font-size: 14px; line-height: 22.75px; color: #163830;` or `#374151`.
- **Badges, Eyebrows & Metadata**: `font-family: Michroma; font-size: 11px - 12px; letter-spacing: 0.15em - 0.2em; text-transform: uppercase; color: #2d554c;`.

### CSS Architecture Constraint
- **No Tailwind JIT Runtime**: `index-D-NCNXWW.clean.css` is statically compiled. All layout grids, max-widths, flexbox wraps, paddings, and media queries **must be declared in component `<style scoped>` blocks**.
- Layout container pattern:
  ```css
  .usecases-container {
    max-width: 80rem;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  ```

---

## 3. Footer Restructuring Architecture

### Problem
The current footer (`LandingFooter.vue`) displays all links in a single horizontal flex row:
`[Logo | Socials] ... [Pricing | FAQs | Terms | Privacy | Refund | Wishlist Leads]`
Adding 4 new links (`Use Cases`, `Market Simulation`, `Public Opinion`, `World Cup Lab`) would crowd 10+ items into one row, causing erratic multi-line wraps, bad spacing, and visual clutter.

### Solution: 4-Column SaaS Footer Matrix
Restructure `LandingFooter.vue` into a clean, hierarchical grid that separates concerns:

1. **Column 1: Brand & Identity (Left, ~30% width)**
   - Obrive Logo (`/obrive-logo.svg`, 70x50px) + `BRAIN`
   - Purpose tagline: *"Autonomous multi-agent simulation & predictive intelligence engine."*
   - Social icon links (LinkedIn, X, Instagram)
2. **Column 2: Solutions / Use Cases**
   - Overview (`/use-cases`)
   - Market Simulation AI (`/use-cases/market-simulation-ai`)
   - Public Opinion AI (`/use-cases/public-opinion-simulation-ai`)
   - 2026 Prediction Lab (`/use-cases/world-cup-prediction`)
3. **Column 3: Platform & Product**
   - Pricing & Plans (`/pricing`)
   - Frequently Asked Questions (`/faqs`)
   - Live Simulation Console (`/console`)
4. **Column 4: Legal & Governance**
   - Terms of Service (`/terms`)
   - Privacy Policy (`/privacy`)
   - Refund Policy (`/refund`)
   - Admin Wishlist Leads (`/admin/wishlist`, visible to admin users only)
5. **Bottom Bar**
   - Divider: `border-top: 1px solid rgba(7, 57, 51, 0.12);`
   - Copyright: `© 2026 Obrive Industries. All rights reserved.`

---

## 4. Page Architecture & Feature Breakdown

### Page 1: Use Cases Hub (`frontend/src/views/UseCasesView.vue`)
- **Route**: `/use-cases`
- **Hero**: Clean Obrive mint aesthetic with headline: *"Real-World Simulation Paths"*, sub-headline explaining evidence-grounded agent modeling.
- **Workflow Strip**: 4-step Obrive engine flow:
  1. *Source Evidence Packet*
  2. *Actor Graph Construction*
  3. *Multi-Round Agent Simulation*
  4. *Evidence-Backed Analytical Synthesis*
- **Interactive Search & Category Filter**:
  - Filter pills: `All`, `Market & GTM`, `Crisis & Public Opinion`, `Sports & Forecasting`, `Strategic Planning`.
  - Search input with real-time card filtering.
- **Featured Hero Cards**:
  - Direct prominent cards for Market Simulation, Public Opinion, and World Cup Prediction Lab.
- **Expanded Grid (12+ curated simulation scenarios)**:
  - Stakeholder Dynamics, Business War Gaming, Pricing Elasticity, Scenario Planning, Synthetic Users, Policy Impact, etc. Each card includes a "Launch in Console" CTA linking to `/console?prompt=...`.

### Page 2: Market Simulation AI (`frontend/src/views/usecases/MarketSimulationView.vue`)
- **Route**: `/use-cases/market-simulation-ai`
- **Focus**: Product launches, pricing changes, GTM testing, and competitor counter-moves.
- **Components & Sections**:
  - Hero with "Stress-Test Before Launch" value proposition & direct CTA button to `/console`.
  - "Evidence Requirements" interactive matrix (Launch briefs, pricing tiers, interview notes, competitor teardowns).
  - "Simulation Dynamics": How Obrive builds the actor graph (buyers, competitors, regulators, influencers).
  - "Anatomy of the Market Report": Explaining Turning Points, Fragile Assumptions, Reversal Catalysts.
  - "Why Multi-Agent Graph Outperforms Single Chatbots".
  - Quick-Launch Scenario Card.

### Page 3: Public Opinion Simulation AI (`frontend/src/views/usecases/PublicOpinionView.vue`)
- **Route**: `/use-cases/public-opinion-simulation-ai`
- **Focus**: Incident response, corporate announcements, policy changes, and PR crisis rehearsal.
- **Components & Sections**:
  - Hero with "Rehearse The Narrative Before It Rehearses You" headline & CTA.
  - "System of Interpretation" vs naive sentiment analysis.
  - "Multi-Round Cascade Simulation" (Round 1 immediate reception, Round 2 media amplification & institutional scrutiny, Round 3 consensus formation).
  - "Report Signals": De-escalation triggers, vulnerable commitments, narrative framing vectors.
  - Real-World Incident Testing Walkthrough.

### Page 4: World Cup & Event Prediction Lab (`frontend/src/views/usecases/WorldCupPredictionView.vue`)
- **Route**: `/use-cases/world-cup-prediction` (with `#prediction-lab` anchor)
- **Key Feature — Interactive Prediction Lab (`#prediction-lab`)**:
  - **Tournament Stage**: Dropdown (`Group Stage`, `Round of 32`, `Round of 16`, `Quarter-final`, `Semi-final`, `Final`).
  - **Team Selectors**: Team A vs Team B with quick-select top contenders (Argentina, France, Brazil, England, Spain, Germany, etc.) and custom inputs.
  - **Prediction Focus**: Radio/Pills (`Match Outcome`, `Turning Points & Tactical Shifts`, `Media & Fan Reaction`).
  - **Evidence Input**: File upload mock/dropzone or URL link for scouting reports/match context.
  - **Live Brief Preview**: Dynamically updates the exact analytical prompt in real-time as user changes inputs!
  - **Run Simulation CTA**: On click, redirects to `/console?prompt=...` passing the constructed simulation brief to the live engine!
  - **Forecasting Methodology & Disclaimers**: Explains qualitative agent-based modeling, confidence parameters, and explicit disclaimer (not sports betting advice).

---

## 5. Routing & Integration
- Update `frontend/src/router/index.js` with lazy-loaded components.
- Add smooth scrolling anchor support for `#prediction-lab`.
- Update `LandingUseCases.vue` on homepage to add a prominent "Explore All Use Cases →" link pointing to `/use-cases`.
