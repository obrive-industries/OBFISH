# Phase 02: Research — Landing Wishlist Conversion & Admin Lead Management

## 1. Context & User Intent
The user wants to re-introduce the wishlist/waitlist email capture directly underneath the hero CTA buttons (`Predict Now` / `Explore Obrive`), with custom copy matching their product positioning:
- **Heading**: `Join the Wishlist to get notified about offers !` (using the cursive / Caveat style seen in MiroFish reference `media_1792944175187_58891199.png`).
- **Subtitle**: `Proposed product positioning. Capabilities should be enabled and validated before being presented as live features.`
- **Action**: Enter email -> click "Send" -> store email in backend database -> show positive feedback.
- **Admin Access**:
  - In the email login (`AuthModal.vue`), add a button/link in the footer.
  - Clicking this button opens a dedicated admin view where all submitted wishlist emails are displayed in an organized, searchable table with count and CSV export.

---

## 2. Technical Inventory

### Frontend
1. **Hero Form (`frontend/src/components/landing/LandingHero.vue`)**:
   - Needs the cursive heading (`font-family: 'Caveat', cursive`).
   - Clean email input and Send button.
   - Reactive state: `email`, `submitting`, `statusMessage`, `isSuccess`.
   - Google Font `Caveat` loaded in `frontend/index.html` or `@import`.
2. **Auth Modal Footer Button (`frontend/src/components/AuthModal.vue`)**:
   - Add a footer link at the bottom of the login modal: `View Wishlist Submissions (Admin)`.
   - On click: Closes the modal and routes to `/admin/wishlist`.
3. **Admin Wishlist View (`frontend/src/views/AdminWishlistView.vue`)**:
   - Route: `/admin/wishlist`.
   - Authenticated view:
     - If authenticated as admin (`role === 'admin'`), fetches `/api/wishlist/subscribers`.
     - Displays total count, search filter, table (Email, Date Submitted, Source, Status).
     - "Copy All Emails" button (one-click copy to clipboard for newsletters).
     - "Export CSV" button.
     - If not logged in, displays an embedded admin login form so the user can easily log in with `ai@obrive.com` without being redirected away.

### Backend
1. **Model (`backend/app/models/wishlist.py`)**:
   - Table `wishlist_subscribers`:
     - `id`: Integer primary key (autoincrement)
     - `email`: String(255), unique, indexed, case-insensitive lowercase
     - `source`: String(100), default 'landing_hero'
     - `created_at`: DateTime(timezone=True), default UTC now
     - `status`: String(50), default 'active'
2. **Blueprint API (`backend/app/api/wishlist.py`)**:
   - `POST /api/wishlist/subscribe`:
     - Public endpoint with rate limit / validation.
     - Accepts JSON `{"email": "..."}`.
     - Normalizes email (`email.strip().lower()`).
     - Duplicate detection: If already subscribed, returns HTTP 200 with friendly message.
     - Inserts record into database and commits.
   - `GET /api/wishlist/subscribers`:
     - Admin-protected endpoint (`@require_auth` + verify admin role).
     - Returns JSON `{ "success": true, "total": N, "subscribers": [...] }`.
   - `GET /api/wishlist/export`:
     - Admin-protected endpoint returning CSV stream for download.
3. **App Registration (`backend/app/__init__.py`)**:
   - Register `wishlist_bp` under `/api/wishlist`.
   - Ensure `db.create_all()` creates the `wishlist_subscribers` table automatically.

---

## 3. Security & Anti-Spam Safeguards
- Basic email regex validation on both client and server.
- SQL injection safety via SQLAlchemy ORM.
- Case normalization (`user@example.com` vs `User@EXAMPLE.com`).
- Admin endpoints protected by JWT bearer token requiring `role == 'admin'`.
