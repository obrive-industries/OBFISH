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
- **Status**: Planned (Awaiting User Review)
- **Goal**: Re-introduce the hero wishlist email capture with customized positioning copy, store incoming lead emails in the database via `/api/wishlist/subscribe`, and provide a dedicated admin lead management view accessible via the email login modal footer.
- **Plans**:
  - `02-landing-wishlist-and-lead-management/PLAN.md`: Full implementation plan for Hero Wishlist form, database model, API endpoints, AuthModal footer button, and `/admin/wishlist` dashboard.
