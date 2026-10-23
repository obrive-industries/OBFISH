<template>
  <footer class="landing-footer" aria-label="Site footer">
    <div class="footer-container">
      <!-- 1. High Impact Pre-Footer Card (Matched to Obrive PrimaryFooterCard.tsx) -->
      <section class="footer-cta-wrapper">
        <div class="primary-footer-card">
          <div class="card-top-row">
            <h2 class="card-cta-title font-microgramma">
              The Future Has Many Possibilities.<br />
              <span class="text-accent-mint">Explore Them.</span>
            </h2>

            <div class="card-cta-button">
              <AnimatedButton
                to="/console"
                variant="accent"
                size="lg"
                :iconSize="16"
                arrowColor="primary"
              >
                Predict Now
              </AnimatedButton>
            </div>
          </div>

          <div class="card-bottom-row">
            <p class="card-cta-sub">
              Make room for new perspectives. Challenge your assumptions. Explore what could happen next with multi-agent predictive intelligence.
            </p>
            <div class="card-ai-badge font-microgramma">
              <span class="badge-dot"></span>
              <span>ENGINE READY // ALL SYSTEMS NOMINAL</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. Obrive Main Links Section with 5-Column Grid -->
      <section class="footer-links-section">
        <!-- Obrive Brand Row -->
        <div class="footer-brand-row">
          <div class="footer-brand-left">
            <a
              href="https://obrive.com"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-obrive-brand"
              title="Visit Obrive Industries"
            >
              <img
                src="../../assets/logo/obrive-main-logo.svg"
                alt="Obrive Industries"
                class="footer-main-logo"
              />
            </a>
            <span class="footer-brand-sep">/</span>
            <router-link to="/" class="footer-product-pill font-microgramma" title="ObMind Home">
              <span class="product-name">OBMIND</span>
              <span class="product-tag">PREDICTIVE AI</span>
            </router-link>
          </div>
          <span class="footer-brand-motto font-microgramma">
            SIMULATE POSSIBILITIES. MAKE SMARTER DECISIONS.
          </span>
        </div>

        <!-- 5-Column Obrive Cell Grid (All real Obrive links) -->
        <div class="footer-cell-grid">
          <!-- Column 1: Products -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Products
            </div>
            <a
              href="https://obrive.com/products/obpark"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obpark
            </a>
            <a
              href="https://obrive.com/products/obcrew"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obcrew
            </a>
            <a
              href="https://obrive.com/products/obnavi"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obnavi
            </a>
            <a
              href="https://obrive.com/products/obnest"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obnest
            </a>
            <a
              href="https://obrive.com/products/obmove"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obmove
            </a>
            <a
              href="https://obrive.com/resources"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell footer-bottom-link font-microgramma"
            >
              <span>Obrive Resources</span>
              <span class="link-arrow">↗</span>
            </a>
          </div>

          <!-- Column 2: What We Build -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              What We Build
            </div>
            <a
              href="https://obrive.com/services/spatial-computing-app-development"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Spatial Computing
            </a>
            <a
              href="https://obrive.com/services/augmented-reality-development"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              AR Development
            </a>
            <a
              href="https://obrive.com/services/virtual-reality-development"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              VR Development
            </a>
            <a
              href="https://obrive.com/services/mixed-reality-development"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              MR Development
            </a>
            <a
              href="https://obrive.com/services/3d-design-development"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              3D Development
            </a>
            <a
              href="https://obrive.com/support/help-center"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell footer-bottom-link font-microgramma"
            >
              <span>Obrive Help Desk</span>
              <span class="link-arrow">↗</span>
            </a>
          </div>

          <!-- Column 3: Industries -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Industries
            </div>
            <a
              href="https://obrive.com/industries/real-estate"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Real Estate
            </a>
            <a
              href="https://obrive.com/industries/automotive"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Automotive
            </a>
            <a
              href="https://obrive.com/industries/retail"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Retail
            </a>
            <a
              href="https://obrive.com/industries/manufacturing"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Manufacturing
            </a>
            <a
              href="https://obrive.com/industries/healthcare"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Healthcare
            </a>
            <a
              href="https://obrive.com/legal"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell footer-bottom-link font-microgramma"
            >
              <span>Obrive Legal</span>
              <span class="link-arrow">↗</span>
            </a>
          </div>

          <!-- Column 4: Company -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Company
            </div>
            <a
              href="https://obrive.com/about"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              About Obrive
            </a>
            <a
              href="https://obrive.com/partners"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              White Label Partners
            </a>
            <a
              href="https://obrive.com/career"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Join the Otters
            </a>
            <a
              href="https://obrive.com/community-forum"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Community Forum
            </a>
            <a
              href="https://obrive.com/site-map"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Site Map
            </a>
            <a
              href="https://obrive.com/global"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell footer-bottom-link font-microgramma"
            >
              <span>Global Market</span>
              <span class="link-arrow">↗</span>
            </a>
          </div>

          <!-- Column 5: Contact & Offices (Matched to Obrive FooterContact.tsx) -->
          <div class="footer-column footer-column-contact">
            <a
              href="https://obrive.com/contact"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-col-header font-microgramma"
            >
              <span>Contact</span>
              <span class="header-arrow">↗</span>
            </a>
            <a
              href="tel:+918884774300"
              class="footer-cell obrive-cell"
              dir="ltr"
              title="Call Obrive"
            >
              +91-888-477-4300
            </a>
            <a
              href="mailto:info@obrive.com"
              class="footer-cell obrive-cell"
              dir="ltr"
              title="Email Obrive"
            >
              info@obrive.com
            </a>
            <div class="footer-cell obrive-cell" title="Bengaluru Office">
              Bengaluru, India
            </div>
            <div class="footer-cell obrive-cell" title="Mumbai Office">
              Mumbai, India
            </div>
            <div class="footer-cell obrive-cell" title="Ahmedabad Office">
              Ahmedabad, India
            </div>

            <!-- Social Links Cell (Matches 6th bottom slot) -->
            <div class="footer-social-cell" aria-label="Social Media Links">
              <a
                href="https://www.linkedin.com/company/obrive-industries"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="LinkedIn"
                title="LinkedIn"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.45a1.64 1.64 0 0 0-1.64 1.64 1.64 1.64 0 0 0 1.64 1.64 1.64 1.64 0 0 0 1.64-1.64A1.64 1.64 0 0 0 7.83 6.45Z"/></svg>
              </a>
              <a
                href="https://www.instagram.com/obrive.inc"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Instagram"
                title="Instagram"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              </a>
              <a
                href="https://www.facebook.com/obriveindustries/"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Facebook"
                title="Facebook"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </a>
              <a
                href="https://x.com/obriveinc"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Twitter"
                title="X (Twitter)"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </a>
              <a
                href="https://medium.com/@obrive.inc"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Medium"
                title="Medium"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/></svg>
              </a>
            </div>
          </div>
        </div>

        <!-- 3. Bottom Legal & Copyright Bar (Matched to Obrive Footer.tsx) -->
        <div class="footer-bottom-bar">
          <div class="bottom-legal-links">
            <a
              href="https://obrive.com/legal"
              target="_blank"
              rel="noopener noreferrer"
              class="legal-item"
            >
              Legal Notice
            </a>
            <span class="legal-sep">•</span>
            <a
              href="https://obrive.com/terms-accessibility"
              target="_blank"
              rel="noopener noreferrer"
              class="legal-item"
            >
              Terms &amp; Accessibility
            </a>
            <span class="legal-sep">•</span>
            <a
              href="https://obrive.com/legal"
              target="_blank"
              rel="noopener noreferrer"
              class="legal-item"
            >
              Privacy Policy
            </a>
            <span class="legal-sep">•</span>
            <a
              href="https://obrive.com"
              target="_blank"
              rel="noopener noreferrer"
              class="legal-item link-url"
            >
              obrive.com ↗
            </a>
          </div>

          <div class="bottom-copyright">
            <p>
              Simulate Possibilities. Make Smarter Decisions. &copy; {{ currentYear }} Obrive Industries. All rights reserved.
            </p>
          </div>
        </div>
      </section>
    </div>
  </footer>
</template>

<script setup>
import AnimatedButton from '../common/AnimatedButton.vue'

const currentYear = new Date().getFullYear()
</script>

<style scoped>
.landing-footer {
  background: #ffffff;
  padding: 72px 24px 44px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 64px;
}

/* 1. High Impact Pre-Footer Card */
.footer-cta-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.primary-footer-card {
  width: 100%;
  background-color: #074139;
  border-radius: 20px;
  color: #ffffff;
  padding: 44px 44px 36px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 260px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 45px -10px rgba(7, 65, 57, 0.35);
}

.primary-footer-card::before {
  content: '';
  position: absolute;
  top: -80px;
  right: -80px;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(162, 241, 223, 0.16), transparent 70%);
  pointer-events: none;
}

.card-top-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
}

.card-cta-title {
  font-size: clamp(1.8rem, 3.2vw, 2.5rem);
  font-weight: 700;
  line-height: 1.18;
  letter-spacing: -0.01em;
  margin: 0;
  color: #ffffff;
}

.text-accent-mint {
  color: #caede5;
}

.card-cta-button {
  flex-shrink: 0;
}

.card-bottom-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  padding-top: 32px;
}

.card-cta-sub {
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  max-width: 540px;
  margin: 0;
}

.card-ai-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #caede5;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 6px 14px;
  border-radius: 9999px;
  white-space: nowrap;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00E5A3;
  box-shadow: 0 0 6px #00E5A3;
}

/* 2. Main Footer Links */
.footer-links-section {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.footer-brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 22px;
  border-bottom: 1px solid rgba(7, 65, 57, 0.14);
}

.footer-brand-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.footer-obrive-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.footer-main-logo {
  height: 28px;
  width: auto;
  display: block;
}

.footer-brand-sep {
  color: rgba(7, 65, 57, 0.25);
  font-size: 1.2rem;
  font-weight: 300;
}

.footer-product-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  background: rgba(7, 65, 57, 0.06);
  border: 1px solid rgba(7, 65, 57, 0.18);
  padding: 4px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.footer-product-pill:hover {
  background: rgba(7, 65, 57, 0.12);
  border-color: #074139;
}

.product-name {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
}

.product-tag {
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.04em;
  background: #074139;
  color: #caede5;
  padding: 1px 4px;
  border-radius: 3px;
}

.footer-brand-motto {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: rgba(7, 65, 57, 0.65);
}

/* 5-Column Grid */
.footer-cell-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.footer-col-header {
  border: 1px solid rgba(7, 65, 57, 0.35);
  padding: 0 14px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #074139;
  border-radius: 8px;
  background: rgba(7, 65, 57, 0.04);
  text-decoration: none;
  transition: all 0.25s ease;
}

.footer-col-header:hover {
  background: rgba(7, 65, 57, 0.1);
  border-color: #074139;
}

.header-arrow {
  font-size: 11px;
  color: rgba(7, 65, 57, 0.5);
  transition: transform 0.2s ease, color 0.2s ease;
}

.footer-col-header:hover .header-arrow {
  color: #074139;
  transform: translate(2px, -2px);
}

.footer-cell {
  padding: 0 14px;
  height: 42px;
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 500;
  color: #074139;
  text-decoration: none;
  border-radius: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.footer-bottom-link {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.02em;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.link-arrow {
  font-size: 11px;
  transition: transform 0.2s ease;
}

.footer-bottom-link:hover .link-arrow {
  transform: translate(2px, -2px);
}

.footer-social-cell {
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 8px;
  padding: 0 14px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
}

.social-link {
  color: #074139;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: transform 0.2s ease, color 0.2s ease, background-color 0.2s ease;
}

.social-link:hover {
  color: #074139;
  background-color: rgba(7, 65, 57, 0.08);
  transform: translateY(-2px);
}

/* 3. Bottom Legal Bar */
.footer-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 22px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
  font-size: 12px;
  color: rgba(7, 65, 57, 0.7);
  flex-wrap: wrap;
  gap: 16px;
}

.bottom-legal-links {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.legal-item {
  color: rgba(7, 65, 57, 0.75);
  text-decoration: none;
  transition: color 0.2s ease;
}

.legal-item:hover {
  color: #074139;
  text-decoration: underline;
}

.legal-sep {
  color: rgba(7, 65, 57, 0.3);
  font-size: 8px;
}

.link-url {
  font-weight: 600;
  color: #074139;
}

.bottom-copyright p {
  margin: 0;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .footer-cell-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }

  .footer-column-contact {
    grid-column: span 2;
  }

  .primary-footer-card {
    padding: 36px 32px;
  }
}

@media (max-width: 768px) {
  .card-top-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-bottom-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .footer-brand-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .footer-bottom-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

@media (max-width: 600px) {
  .footer-cell-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .footer-column-contact {
    grid-column: span 1;
  }

  .footer-brand-left {
    flex-wrap: wrap;
  }
}
</style>
