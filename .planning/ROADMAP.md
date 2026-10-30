# Project Roadmap

## Phase 1: Simulation Engine Remediation & Slowness Optimization
- **Status**: Completed & Verified
- **Goal**: Resolve all structural failure points, crashes, silent fallbacks, token budget exhaustion, and execution slowness across the entire pipeline from Graph Construction to Report Generation.
- **Plans Executed & Verified**:
  - `01-01-PLAN-llm-layer-and-failover.md`: Resilient LLM client with multi-key rotation, 429 backoff, truncated token retry without restrictive caps, and error payload extraction.
  - `01-02-PLAN-step1-step2-optimization.md`: Slashed OASIS persona prompt bloat from 2000 words to 100-150 words; added token caps; eliminated 401 crashes on comma-separated keys.
  - `01-03-PLAN-step3-simulation-execution-speed.md`: Enabled SQLite WAL mode (`PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`), unbuffered subprocess pipes (`PYTHONUNBUFFERED=1`), and rate-limit retries with backoff in round loops.
  - `01-04-PLAN-step4-report-generation-integrity.md`: Removed fake dummy fallback text (`Preliminary synthesis for this section indicates key behavioral patterns...`); added direct analytical synthesis fallback; guarded cache against corrupted dummy files.
  - `01-05-PLAN-e2e-verification.md`: 176 backend unit/integration tests passing (100% green); Vite frontend production build clean.

## Phase 2: Landing Wishlist Conversion & Admin Lead Management
- **Status**: Completed & Verified
- **Goal**: Re-introduce the hero wishlist email capture with customized positioning copy, store incoming lead emails in the database via `/api/wishlist/subscribe`, and provide a dedicated admin lead management view accessible via the email login modal footer.
- **Plans**:
  - `02-landing-wishlist-and-lead-management/PLAN.md`: Full implementation plan for Hero Wishlist form, database model, API endpoints, AuthModal footer button, and `/admin/wishlist` dashboard.

## Phase 3: Obrive Visual System Alignment & Typography Polish
- **Status**: Completed & Verified
- **Goal**: Align logo branding (remove `/`), match hero title sizing to `obrive.com`'s "Owning the Future", standardize headings, subheadings, and buttons across Landing, Console, FAQs, and Admin Wishlist, and purge legacy orange accents.
- **Plans**:
  - `03-obrive-visual-system-alignment/PLAN.md`: Complete execution plan for logo divider removal, typography scaling, button harmonization, and view-level styling.

## Phase 4: Native Use Cases Suite & Scalable Footer Architecture
- **Status**: Completed & Verified
- **Goal**: Build dedicated native Obrive simulation use case pages (`/use-cases`, `/use-cases/market-simulation-ai`, `/use-cases/public-opinion-simulation-ai`, `/use-cases/world-cup-prediction#prediction-lab`) matching our visual design system, typography (`Microgramma` and `Michroma`), and mint/teal styling. Refactor `LandingFooter.vue` into a scalable 4-column architecture to organize all links cleanly without visual overcrowding.
- **Plans Executed & Verified**:
  - `04-use-cases-suite-and-footer-architecture/PLAN.md`: Full implementation of 4-column footer restructuring, Use Cases Hub view, Market Simulation view, Public Opinion view, interactive World Cup Prediction Lab, routing, and headless Chromium quality verification.

## Phase 5: Comprehensive Use Cases Suite
- **Status**: Completed & Verified
- **Goal**: Build full-fidelity dedicated pages for all remaining use cases on the platform via a structured domain registry and universal dynamic detail view (`/use-cases/:slug`), matching Obrive brand standards. Update `UseCasesView.vue` so every card features active `Explore View →` navigation.
- **Plans Executed & Verified**:
  - `05-comprehensive-use-cases-suite/PLAN.md`: Complete implementation of useCasesRegistry.js (scraped authentic domain data from mirofish.my), universal UseCaseDetailView.vue, dynamic router mapping (`/use-cases/:slug`), hub card activation (`Explore View →` on all cards), and headless Chromium quality verification.



