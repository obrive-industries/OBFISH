<template>
  <footer class="landing-footer">
    <!-- Final CTA Banner -->
    <div class="footer-cta-section">
      <div class="cta-glow"></div>
      <div class="cta-inner">
        <h2 class="footer-cta-title">
          The Future Has Many Possibilities. <span class="gradient-text">Explore Them.</span>
        </h2>

        <p class="footer-cta-sub">
          Make room for new perspectives. Challenge your assumptions. Explore what could happen next.
        </p>

        <div class="footer-cta-btn-wrap">
          <router-link to="/console" class="btn-primary-large">
            <span>Predict Now</span>
            <span class="arrow">→</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Main Footer Links & Brand -->
    <div class="footer-main">
      <div class="footer-grid">
        <!-- Brand Column -->
        <div class="footer-col brand-col">
          <div class="footer-brand">
            <img src="../../assets/logo/obrive-white-logo.svg" alt="Obrive Industries" class="footer-logo" />
            <span class="brand-name">OBMIND</span>
          </div>
          <p class="footer-slogan">
            Simulate Possibilities. Make Smarter Decisions.
          </p>
          <div class="social-links">
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="LinkedIn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.45a1.64 1.64 0 0 0-1.64 1.64 1.64 1.64 0 0 0 1.64 1.64 1.64 1.64 0 0 0 1.64-1.64A1.64 1.64 0 0 0 7.83 6.45Z"/></svg>
            </a>
            <a href="https://x.com" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Twitter">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Instagram">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            </a>
          </div>
        </div>

        <!-- Links Column 1: Platform -->
        <div class="footer-col">
          <h4 class="col-title">Platform</h4>
          <ul class="col-links">
            <li><router-link to="/console">Engine Console</router-link></li>
            <li><a href="#workflow">How It Works</a></li>
            <li><a href="#use-cases">Explore Use Cases</a></li>
            <li><a href="#faq">FAQ</a></li>
          </ul>
        </div>

        <!-- Links Column 2: Ecosystem -->
        <div class="footer-col">
          <h4 class="col-title">Obrive Ecosystem</h4>
          <ul class="col-links">
            <li><a href="https://obrive.com" target="_blank" rel="noopener noreferrer">Obrive Industries ↗</a></li>
            <li><a href="https://obrive.com" target="_blank" rel="noopener noreferrer">Predictive AI Suite</a></li>
            <li><a href="https://obmind.obrive.com/ai" target="_blank" rel="noopener noreferrer">obmind.obrive.com/ai ↗</a></li>
          </ul>
        </div>

        <!-- Links Column 3: Trust & Legal -->
        <div class="footer-col">
          <h4 class="col-title">Legal & Security</h4>
          <ul class="col-links">
            <li><span class="static-link">Privacy Policy</span></li>
            <li><span class="static-link">Terms of Service</span></li>
            <li><span class="static-link">BYOK Security</span></li>
          </ul>
        </div>
      </div>

      <!-- Legal Disclaimer from docx -->
      <div class="footer-disclaimer">
        <p>
          Simulated results are exploratory, not guaranteed forecasts or substitutes for real-world evidence, professional judgement, or validated research.
        </p>
      </div>

      <!-- Bottom Copyright Bar -->
      <div class="footer-bottom">
        <p class="copyright-text">
          Simulate Possibilities. Make Smarter Decisions. &copy; {{ currentYear }} Obrive Industries. All rights reserved.
        </p>
        <span class="power-tag">Powered by Obrive AI</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.landing-footer {
  background: #05080a;
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.footer-cta-section {
  position: relative;
  padding: 100px 24px;
  background: radial-gradient(circle at 50% 0%, rgba(7, 65, 57, 0.5) 0%, rgba(5, 8, 10, 0.95) 75%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.cta-glow {
  position: absolute;
  top: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(ellipse, rgba(0, 229, 163, 0.25) 0%, transparent 70%);
  pointer-events: none;
  filter: blur(80px);
}

.cta-inner {
  max-width: 860px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 2;
}

.footer-cta-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.4rem, 4.5vw, 3.8rem);
  font-weight: 800;
  color: #ffffff;
  line-height: 1.15;
  margin: 0 0 20px 0;
}

.gradient-text {
  background: linear-gradient(135deg, #00E5A3 0%, #a2f1df 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-cta-sub {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #94a3b8;
  max-width: 640px;
  margin: 0 auto 36px;
}

.btn-primary-large {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #00E5A3 0%, #074139 100%);
  color: #05080a;
  padding: 16px 40px;
  border-radius: 12px;
  font-size: 1.15rem;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 10px 30px rgba(0, 229, 163, 0.4);
  transition: all 0.25s ease;
}

.btn-primary-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 40px rgba(0, 229, 163, 0.6);
  color: #000;
}

.btn-primary-large:hover .arrow {
  transform: translateX(4px);
}

.arrow {
  transition: transform 0.2s ease;
}

.footer-main {
  max-width: 1240px;
  margin: 0 auto;
  padding: 80px 24px 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 60px;
}

.brand-col {
  display: flex;
  flex-direction: column;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.footer-logo {
  height: 28px;
  width: auto;
}

.brand-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 2px;
}

.footer-slogan {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.6;
  margin: 0 0 24px 0;
  max-width: 320px;
}

.social-links {
  display: flex;
  gap: 14px;
}

.social-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  text-decoration: none;
}

.social-icon:hover {
  border-color: #00E5A3;
  color: #00E5A3;
  background: rgba(0, 229, 163, 0.1);
  transform: translateY(-2px);
}

.col-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 20px 0;
  letter-spacing: 0.5px;
}

.col-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.col-links a,
.col-links .static-link {
  color: #94a3b8;
  font-size: 0.9rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.col-links a:hover {
  color: #00E5A3;
}

.col-links .static-link {
  cursor: default;
}

.footer-disclaimer {
  padding: 24px;
  background: rgba(12, 18, 22, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  margin-bottom: 40px;
}

.footer-disclaimer p {
  margin: 0;
  font-size: 0.8rem;
  line-height: 1.55;
  color: #64748b;
  text-align: center;
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.85rem;
  color: #64748b;
  flex-wrap: wrap;
  gap: 12px;
}

.copyright-text {
  margin: 0;
}

.power-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #00E5A3;
}

@media (max-width: 900px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 36px;
  }
}

@media (max-width: 600px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>
