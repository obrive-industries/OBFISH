# Phase 03: Obrive Visual System Alignment & Typography Polish — Execution Plan

## Goal
Align the visual identity across the entire MiroFish platform with the official Obrive web design system (`/home/yash/Obrive/Obrive`):
1. Remove the `/` divider between the logo icon and `BRAIN` brand name in the header, footer, and navigation.
2. Scale down the `Predictive Intelligence` hero headline to match the exact font size of `"Owning the Future"` from `obrive.com` (`text-4xl sm:text-5xl md:text-5xl lg:text-6xl`).
3. Harmonize all headings (`Microgramma Bold`, `#073933`), subheadings (`Michroma` / `#163830`), and buttons (`rounded-xl`, uppercase tracking, `#073933` primary & `#074139` outline) across Landing, Console, FAQs, and Admin Wishlist views.
4. Purge legacy orange accents (`#FF4500`) in favor of Obrive's signature teal and mint design palette.

---

## Task 1: Header & Footer Logo Polish (Remove Slash)
**Files:**
- `frontend/src/components/landing/LandingHeader.vue`
- `frontend/src/components/landing/LandingFooter.vue`

**Implementation Details:**
1. In `LandingHeader.vue`:
   - Remove `<span class="logo-divider">/</span>` between `<img src="/obrive-logo.svg" ... />` and `<span class="logo-text">BRAIN</span>`.
   - Ensure clean horizontal gap (`gap-3`) and baseline vertical alignment.
2. In `LandingFooter.vue`:
   - Remove `<span class="logo-divider">/</span>` between the logo image and brand name text.
3. Verify brand consistency across responsive desktop and mobile viewports.

---

## Task 2: Predictive Intelligence Headline & Landing Component Harmonization
**Files:**
- `frontend/src/components/landing/LandingHero.vue`
- `frontend/src/components/landing/LandingDecisionDynamics.vue`
- `frontend/src/components/landing/LandingFeatures.vue`
- `frontend/src/components/landing/LandingUseCases.vue`
- `frontend/src/components/landing/LandingPhilosophy.vue`

**Implementation Details:**
1. In `LandingHero.vue`:
   - Change `Predictive Intelligence` heading classes from `text-5xl sm:text-6xl md:text-7xl lg:text-8xl` to `text-4xl sm:text-5xl md:text-5xl lg:text-6xl` (exact match with `"Owning the Future"` in `Obrive/src/app/(public)/page.tsx:190`).
   - Style CTA buttons to match Obrive button architecture:
     - Primary button (`Predict Now`): `bg-[#073933] text-white hover:bg-[#074139] rounded-xl px-6 py-3 font-semibold text-xs tracking-wider uppercase transition-all shadow-sm`.
     - Outline button (`Explore Obrive`): `bg-transparent border border-[#074139] text-[#074139] hover:bg-[#074139]/10 rounded-xl px-6 py-3 font-semibold text-xs tracking-wider uppercase transition-all`.
     - Wishlist submit button: `rounded-xl`, uppercase tracking, `#073933` background with `#042823` hover.
2. In `LandingDecisionDynamics.vue`:
   - Section heading: `text-2xl sm:text-3xl lg:text-4xl font-microgramma text-[#073933]`.
   - Eyebrow tag: `font-michroma text-xs tracking-[0.2em] uppercase text-[#2d554c]`.
   - Number badges (`1`, `2`): `font-michroma text-xs font-bold`.
3. In `LandingFeatures.vue` & `LandingUseCases.vue`:
   - Section titles: `text-2xl sm:text-3xl lg:text-4xl font-microgramma text-[#073933]`.
   - Step counters & tags: `font-michroma text-xs tracking-[0.15em] uppercase text-[#2d554c]`.
   - Card titles: `font-microgramma text-lg sm:text-xl font-bold text-[#073933]`.
4. In `LandingPhilosophy.vue`:
   - Section heading: `font-microgramma text-[#073933]`.
   - Subheadings & list labels: `font-michroma text-sm text-[#073933]`.

---

## Task 3: FAQs Page (`FaqView.vue`) Harmonization with Obrive FAQ Design
**Files:**
- `frontend/src/views/FaqView.vue`

**Implementation Details:**
1. Replace legacy dark black background with Obrive's signature mint layout (`background-color: #A2F1DF`), matching `FAQMainClientLayout.tsx` in `/home/yash/Obrive/Obrive`.
2. Header typography:
   - Eyebrow pill: `font-michroma text-xs tracking-[0.2em] text-[#073933] bg-white/60 border border-[#073933]/15`.
   - Title: `Frequently Asked Questions` in `font-microgramma text-4xl sm:text-5xl lg:text-6xl text-[#073933] uppercase tracking-widest leading-tight mb-4`.
   - Subtitle: `text-[#163830] text-base sm:text-lg max-w-2xl mx-auto leading-relaxed`.
3. Accordion cards:
   - Clean glass/white styling: `background: rgba(255, 255, 255, 0.75); border: 1px solid rgba(7, 57, 51, 0.15); border-radius: 1rem;`
   - Question numbering: `font-michroma text-xs font-bold text-[#2d554c]`.
   - Question text: `font-semibold text-base sm:text-lg text-[#073933]`.
   - Answer copy: `text-sm sm:text-base text-[#163830] leading-relaxed`.
4. CTA section:
   - Obrive primary button: `bg-[#073933] text-white hover:bg-[#074139] rounded-xl px-6 py-3 font-semibold text-xs tracking-wider uppercase transition-all shadow-sm`.

---

## Task 4: Console & Admin Wishlist Theme & Button System Alignment
**Files:**
- `frontend/src/views/ConsoleView.vue`
- `frontend/src/views/AdminWishlistView.vue`
- `frontend/src/App.vue`

**Implementation Details:**
1. In `App.vue`:
   - Remap global tokens `--color-orange: #073933;` and `--color-orange-hover: #074139;` so legacy component styles inherit Obrive teal instead of orange.
2. In `ConsoleView.vue`:
   - `start-engine-btn`: Update border-radius to `12px` (`rounded-xl`), font to `font-microgramma`, background `#073933`, hover `#074139` with Obrive teal glow (`box-shadow: 0 6px 20px rgba(7, 57, 51, 0.35)`), replacing all legacy `#FF4500` references.
   - Plan action button (`VIEW PLANS →` / `MANAGE`): Style with Obrive rounded-xl outline button variant.
   - Verify banner buttons (`Enter Code`, `Resend Code`): Style with Obrive button tokens.
   - Section headers & workflow metrics: Align fonts to Microgramma Bold and Michroma.
3. In `AdminWishlistView.vue`:
   - Header: `Wishlist & Waitlist Leads` in `font-microgramma text-[#073933]` (or clean dark card on dark mode), `Admin Portal` tag in `font-michroma`.
   - Action buttons (`← Back to Home`, `Console`, `Sign In as Admin`, `Refresh`, `Export CSV`): Style with `rounded-xl`, uppercase tracking, Obrive teal `#073933` and hover states.
   - Status indicators and metrics: Use Obrive teal and mint accents.

---

## Verification & Quality Gates
1. **Visual Verification**:
   - Verify `http://localhost:3000`: Confirm `/` is removed from logo header and footer.
   - Verify `Predictive Intelligence` title matches `"Owning the Future"` scale (`text-4xl sm:text-5xl md:text-5xl lg:text-6xl`).
   - Verify button styles across Landing, Console, FAQs, and Admin Wishlist pages.
2. **Automated Verification**:
   - `npm run build --prefix frontend`: Production build must pass with 0 errors.
   - `backend/.venv/bin/pytest`: Backend tests must pass (18/18).
3. **Git Hygiene**:
   - Keep changes atomic and local.
   - **DO NOT PUSH** to remote without explicit user permission.
