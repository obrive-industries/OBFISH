# Phase 02: Landing Wishlist Conversion & Admin Lead Management — Execution Plan

## Goal
Implement the hero wishlist email capture form with customized product positioning copy, store submissions in the database, and provide a dedicated admin viewer accessible via a footer button in the email login modal.

---

## Task 1: Backend Database Model & Wishlist Subscription API
**Files:**
- `backend/app/models/wishlist.py` (New)
- `backend/app/models/__init__.py`
- `backend/app/api/wishlist.py` (New)
- `backend/app/__init__.py`
- `backend/tests/test_wishlist_api.py` (New)

**Implementation Details:**
1. Create `WishlistSubscriber` model:
   - Fields: `id`, `email` (unique index, lowercase), `source`, `created_at`, `status`.
2. Implement `wishlist_bp` in `backend/app/api/wishlist.py`:
   - `POST /api/wishlist/subscribe`: Public endpoint validating email format and saving unique email with timestamp. Returns friendly success message even on duplicates ("You're already on the list!").
   - `GET /api/wishlist/subscribers`: Admin-only endpoint returning all subscribers sorted by newest first.
   - `GET /api/wishlist/export`: Admin-only endpoint returning a CSV file of all submissions.
3. Register blueprint in `backend/app/__init__.py`.
4. Write pytest test suite `backend/tests/test_wishlist_api.py` verifying subscription creation, duplicates, format validation, and admin auth protection.

---

## Task 2: Frontend Hero Wishlist Form with Cursive Headline
**Files:**
- `frontend/index.html` (Import Google Font `Caveat`)
- `frontend/src/components/landing/LandingHero.vue`
- `frontend/src/api/wishlist.js` (New)

**Implementation Details:**
1. In `frontend/index.html`, add `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&display=swap">`.
2. In `LandingHero.vue`:
   - Below the CTA buttons, add the wishlist block matching the MiroFish screenshot aesthetic:
     - Heading: `Join the Wishlist to get notified about offers !` with `font-family: 'Caveat', cursive;`
     - Subtitle: `Proposed product positioning. Capabilities should be enabled and validated before being presented as live features.`
     - Clean responsive form with email input (`bg-transparent border border-gray-600 rounded-lg text-white`) and Send button (`bg-white text-black hover:bg-gray-200`).
     - Real-time submit handler calling `wishlistApi.subscribe(email)`.
     - Inline success/error feedback banner.

---

## Task 3: Login Modal Footer Button & Admin Wishlist Management Page
**Files:**
- `frontend/src/components/AuthModal.vue`
- `frontend/src/views/AdminWishlistView.vue` (New)
- `frontend/src/router/index.js`

**Implementation Details:**
1. In `AuthModal.vue`:
   - Add a footer link at the very bottom of the modal:
     `<div class="modal-admin-footer"><button type="button" class="admin-wishlist-link" @click="openAdminWishlist">📋 View Wishlist Submissions (Admin)</button></div>`
   - Closes the modal and navigates to `/admin/wishlist`.
2. In `AdminWishlistView.vue`:
   - Route `/admin/wishlist`.
   - Header with back to home/console link, stats (Total Subscribers, Latest Submission).
   - Search filter to search emails.
   - Action buttons: "Copy All Emails", "Export CSV".
   - Clean data table listing: Email, Date, Status, Source.
   - If not signed in as admin, provides an instant in-page admin login card so the admin can sign in directly with `ai@obrive.com` and load data immediately.
3. In `frontend/src/router/index.js`:
   - Register route `/admin/wishlist`.

---

## Verification Plan
1. **Automated Backend Tests:**
   ```bash
   uv run --directory backend pytest backend/tests/test_wishlist_api.py
   uv run --directory backend pytest
   ```
2. **Frontend Production Build:**
   ```bash
   npm run build --prefix frontend
   ```
3. **End-to-End Functional Check:**
   - Submit a test email from the hero section wishlist form; verify 200 OK and database entry.
   - Open email login modal; verify "View Wishlist Submissions" button in footer.
   - Click to `/admin/wishlist`; sign in as `ai@obrive.com`; verify table displays the submitted email.
