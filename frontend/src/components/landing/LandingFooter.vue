<template>
  <footer class="bg-transparent py-12 relative z-10" aria-label="Site footer">
    <div class="container-main">
      <div class="footer-grid">
        <!-- Col 1: Brand & Purpose -->
        <div class="footer-brand-col">
          <router-link to="/" class="logo" aria-label="Brain Home">
            <img src="/obrive-logo.svg" alt="Obrive" class="logo-img" width="70" height="50" />
            <span class="logo-text">BRAIN</span>
          </router-link>
          <p class="brand-tagline">
            Autonomous multi-agent simulation &amp; predictive intelligence engine.
          </p>
          <div class="social-links">
            <a
              href="https://www.linkedin.com/company/obrive-industries"
              target="_blank"
              rel="noopener noreferrer"
              class="social-btn"
              aria-label="LinkedIn"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
              </svg>
            </a>
            <a
              href="https://x.com/obriveinc"
              target="_blank"
              rel="noopener noreferrer"
              class="social-btn"
              aria-label="X"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </a>
            <a
              href="https://www.instagram.com/obrive.inc"
              target="_blank"
              rel="noopener noreferrer"
              class="social-btn"
              aria-label="Instagram"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z" />
              </svg>
            </a>
          </div>
        </div>

        <!-- Col 2: Solutions / Use Cases -->
        <div class="footer-nav-col">
          <h4 class="col-heading">SOLUTIONS</h4>
          <ul class="col-links">
            <li>
              <router-link to="/use-cases">All Use Cases</router-link>
            </li>
            <li>
              <router-link to="/use-cases/market-simulation-ai">Market Simulation AI</router-link>
            </li>
            <li>
              <router-link to="/use-cases/public-opinion-simulation-ai">Public Opinion AI</router-link>
            </li>
            <li>
              <router-link to="/use-cases/world-cup-prediction">2026 Prediction Lab</router-link>
            </li>
          </ul>
        </div>

        <!-- Col 3: Platform -->
        <div class="footer-nav-col">
          <h4 class="col-heading">PLATFORM</h4>
          <ul class="col-links">
            <li>
              <router-link to="/pricing">Pricing &amp; Plans</router-link>
            </li>
            <li>
              <router-link to="/faqs">Frequently Asked Questions</router-link>
            </li>
            <li>
              <router-link to="/console">Simulation Console</router-link>
            </li>
          </ul>
        </div>

        <!-- Col 4: Legal & Trust -->
        <div class="footer-nav-col">
          <h4 class="col-heading">LEGAL</h4>
          <ul class="col-links">
            <li>
              <router-link to="/terms">Terms of Service</router-link>
            </li>
            <li>
              <router-link to="/privacy">Privacy Policy</router-link>
            </li>
            <li>
              <router-link to="/refund">Refund Policy</router-link>
            </li>
            <li v-if="authStore.isAdmin.value">
              <router-link to="/admin/wishlist" class="admin-lead-link">
                <span>📋 Wishlist Leads</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <p class="copyright-text">
          © 2026 Obrive Industries. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import authStore from '../../store/auth'
</script>

<style scoped>
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

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
  align-items: start;
}

@media (min-width: 640px) {
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5rem 2rem;
  }
}

@media (min-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 3rem;
  }
}

.footer-brand-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.85;
}

.logo-img {
  width: 70px;
  height: 50px;
  object-fit: contain;
}

.logo-text {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  letter-spacing: 0.08em;
  color: #073933;
  line-height: 1;
}

.brand-tagline {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  line-height: 20px;
  color: #163830;
  opacity: 0.85;
  max-width: 280px;
  margin: 0;
}

.social-links {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 0.5rem;
}

.social-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(7, 57, 51, 0.08);
  color: #073933;
  transition: all 0.2s ease;
  text-decoration: none;
}

.social-btn:hover {
  background: #073933;
  color: #A2F1DF;
  transform: translateY(-2px);
}

.footer-nav-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.col-heading {
  font-family: 'Microgramma', 'Microgramma Bold', sans-serif;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.14em;
  color: #073933;
  text-transform: uppercase;
  margin: 0;
  padding-bottom: 0.25rem;
}

.col-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.col-links a {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 13px;
  font-weight: 500;
  line-height: 20px;
  color: #163830;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
}

.col-links a:hover {
  color: #073933;
  transform: translateX(2px);
}

.admin-lead-link {
  color: #073933 !important;
  font-weight: 600 !important;
}

.footer-bottom {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(7, 57, 51, 0.15);
  text-align: center;
}

.copyright-text {
  font-family: Michroma, "Michroma Fallback", sans-serif;
  font-size: 12px;
  line-height: 18px;
  color: #2d554c;
  margin: 0;
}
</style>
