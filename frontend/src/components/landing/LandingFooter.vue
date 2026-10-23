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
              Make room for new perspectives. Challenge your assumptions. Explore what could happen next.
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
        <!-- Obrive Logo Header -->
        <div class="footer-brand-row">
          <router-link to="/" class="footer-brand-link">
            <img
              src="../../assets/icons/obrive-logo.svg"
              alt="Obrive Logo"
              class="footer-obrive-logo"
            />
            <span class="footer-brand-title font-microgramma">OBMIND</span>
          </router-link>
          <span class="footer-brand-motto font-microgramma">
            SIMULATE POSSIBILITIES. MAKE SMARTER DECISIONS.
          </span>
        </div>

        <!-- 5-Column Obrive Cell Grid -->
        <div class="footer-cell-grid">
          <!-- Column 1: Platform -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Platform
            </div>
            <router-link to="/console" class="footer-cell obrive-cell">
              Engine Console
            </router-link>
            <a href="#overview" class="footer-cell obrive-cell">
              Scenario Ingestion
            </a>
            <a href="#workflow" class="footer-cell obrive-cell">
              Graph Builder
            </a>
            <a href="#workflow" class="footer-cell obrive-cell">
              Simulation Swarm
            </a>
            <div class="footer-cell-empty"></div>
          </div>

          <!-- Column 2: Solutions -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Solutions
            </div>
            <a href="#use-cases" class="footer-cell obrive-cell">
              Startups & Strategy
            </a>
            <a href="#use-cases" class="footer-cell obrive-cell">
              Brand Intelligence
            </a>
            <a href="#use-cases" class="footer-cell obrive-cell">
              Public Opinion & PR
            </a>
            <a href="#use-cases" class="footer-cell obrive-cell">
              Fiction & Creative
            </a>
            <div class="footer-cell-empty"></div>
          </div>

          <!-- Column 3: Resources -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Resources
            </div>
            <a href="#uncertainty" class="footer-cell obrive-cell">
              Decision Dynamics
            </a>
            <a href="#workflow" class="footer-cell obrive-cell">
              5-Step Workflow
            </a>
            <a href="#about" class="footer-cell obrive-cell">
              Vision & Sandbox
            </a>
            <a href="#faq" class="footer-cell obrive-cell">
              Knowledge Base
            </a>
            <div class="footer-cell-empty"></div>
          </div>

          <!-- Column 4: Ecosystem -->
          <div class="footer-column">
            <div class="footer-col-header font-microgramma">
              Ecosystem
            </div>
            <a
              href="https://obrive.com"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              Obrive Industries ↗
            </a>
            <a
              href="https://obmind.obrive.com/ai"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-cell obrive-cell"
            >
              obmind.obrive.com/ai ↗
            </a>
            <span class="footer-cell obrive-cell">
              Privacy Policy
            </span>
            <span class="footer-cell obrive-cell">
              Terms of Service
            </span>
            <div class="footer-cell-empty"></div>
          </div>

          <!-- Column 5: Contact & Offices (Matched to FooterContact.tsx) -->
          <div class="footer-column">
            <a
              href="https://obrive.com/contact"
              target="_blank"
              rel="noopener noreferrer"
              class="footer-col-header font-microgramma text-center sm:text-start"
            >
              Contact
            </a>
            <div class="footer-cell obrive-cell" dir="ltr">
              +91-888-477-4300
            </div>
            <a
              href="mailto:ai@obrive.com"
              class="footer-cell obrive-cell"
              dir="ltr"
            >
              ai@obrive.com
            </a>
            <div class="footer-cell obrive-cell">
              Bengaluru, Karnataka, India
            </div>
            <div class="footer-cell obrive-cell">
              Mumbai, Maharashtra, India
            </div>
            <div class="footer-cell obrive-cell">
              Ahmedabad, Gujarat, India
            </div>

            <!-- Social Links Cell -->
            <div class="footer-social-cell">
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="LinkedIn"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.45a1.64 1.64 0 0 0-1.64 1.64 1.64 1.64 0 0 0 1.64 1.64 1.64 1.64 0 0 0 1.64-1.64A1.64 1.64 0 0 0 7.83 6.45Z"/></svg>
              </a>
              <a
                href="https://x.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Twitter"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </a>
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                aria-label="Instagram"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              </a>
            </div>
          </div>
        </div>

        <!-- 3. Bottom Legal & Copyright Bar (Matched to Obrive Footer.tsx) -->
        <div class="footer-bottom-bar">
          <div class="bottom-legal-links">
            <span class="legal-item">Legal Notice</span>
            <span class="legal-item">Terms &amp; Accessibility</span>
            <a href="https://obmind.obrive.com/ai" class="legal-item link-url">
              obmind.obrive.com/ai
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
  padding: 80px 24px 48px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
}

.footer-container {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 72px;
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
  padding: 48px 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 280px;
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
  font-size: clamp(1.8rem, 3.2vw, 2.6rem);
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
  padding-top: 36px;
}

.card-cta-sub {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  max-width: 520px;
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
  gap: 40px;
}

.footer-brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(7, 65, 57, 0.14);
}

.footer-brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #074139;
}

.footer-obrive-logo {
  height: 32px;
  width: auto;
}

.footer-brand-title {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #074139;
}

.footer-brand-motto {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: rgba(7, 65, 57, 0.7);
}

/* 5-Column Grid */
.footer-cell-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-col-header {
  border: 1px solid rgba(7, 65, 57, 0.4);
  padding: 10px 14px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #074139;
  border-radius: 8px;
  background: rgba(7, 65, 57, 0.04);
  text-decoration: none;
}

.footer-cell {
  padding: 10px 14px;
  font-size: 12px;
  color: #074139;
  text-decoration: none;
  cursor: pointer;
  display: block;
}

.footer-cell-empty {
  border: 1px solid rgba(7, 65, 57, 0.15);
  border-radius: 8px;
  padding: 18px;
  background: rgba(7, 65, 57, 0.015);
}

.footer-social-cell {
  border: 1px solid rgba(7, 65, 57, 0.22);
  border-radius: 8px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: #ffffff;
}

.social-link {
  color: #074139;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, color 0.2s ease;
}

.social-link:hover {
  color: #0d5c52;
  transform: translateY(-2px);
}

/* 3. Bottom Legal Bar */
.footer-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24px;
  border-top: 1px solid rgba(7, 65, 57, 0.12);
  font-size: 12px;
  color: rgba(7, 65, 57, 0.7);
  flex-wrap: wrap;
  gap: 16px;
}

.bottom-legal-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.legal-item {
  color: rgba(7, 65, 57, 0.7);
  text-decoration: none;
  transition: color 0.2s ease;
}

.legal-item:hover {
  color: #074139;
}

.link-url {
  font-weight: 600;
  color: #074139;
}

.bottom-copyright p {
  margin: 0;
}

@media (max-width: 1024px) {
  .footer-cell-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .primary-footer-card {
    padding: 36px 32px;
  }
}

@media (max-width: 768px) {
  .card-top-row {
    flex-direction: column;
  }

  .card-bottom-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-brand-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .footer-cell-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
