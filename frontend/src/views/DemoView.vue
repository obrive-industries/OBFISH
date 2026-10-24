<template>
  <div class="demo-container">
    <header class="demo-navbar">
      <router-link to="/" class="brand-link">
        <span class="brand-name">BRAIN</span>
      </router-link>
      <div class="nav-right">
        <router-link to="/console" class="nav-link">Console</router-link>
        <button type="button" class="nav-cta" @click="openPlans">Get a plan</button>
      </div>
    </header>

    <main class="demo-main">
      <div class="demo-meta">
        <span class="sample-badge">SAMPLE REPORT</span>
        <span class="meta-text">Pre-recorded run · 240 agents · 18 rounds · 6 minutes</span>
      </div>

      <h1 class="demo-title">
        How the market reacts to a 20% price increase on a subscription product
      </h1>
      <p class="demo-lead">
        A consumer software company plans to raise prices for the first time in three years.
        Leadership wants to know which segments absorb the change, which churn, and which
        message keeps revenue positive without eroding trust.
      </p>

      <section class="verdict">
        <div class="verdict-label font-mono">HEADLINE PREDICTION</div>
        <p class="verdict-text">
          Revenue holds in the first quarter but net retention drops 6–9 points by month four.
          Churn concentrates in self-serve monthly subscribers acquired on discount, while
          annual and team accounts absorb the increase with limited movement.
        </p>
      </section>

      <section class="demo-section">
        <h2 class="section-heading">Executive summary</h2>
        <div class="summary-grid">
          <article v-for="item in summary" :key="item.label" class="summary-card">
            <div class="summary-value">{{ item.value }}</div>
            <div class="summary-label font-mono">{{ item.label }}</div>
            <p class="summary-copy">{{ item.copy }}</p>
          </article>
        </div>
      </section>

      <section class="demo-section">
        <h2 class="section-heading">What the simulated population did</h2>
        <ul class="finding-list">
          <li v-for="finding in findings" :key="finding.title">
            <div class="finding-title">{{ finding.title }}</div>
            <p class="finding-copy">{{ finding.copy }}</p>
          </li>
        </ul>
      </section>

      <section class="demo-section">
        <h2 class="section-heading">Representative reactions</h2>
        <div class="quote-grid">
          <blockquote v-for="quote in quotes" :key="quote.who" class="quote-card">
            <p class="quote-text">“{{ quote.text }}”</p>
            <footer class="quote-who font-mono">{{ quote.who }}</footer>
          </blockquote>
        </div>
      </section>

      <section class="demo-section">
        <h2 class="section-heading">Recommended actions</h2>
        <ol class="action-list">
          <li v-for="action in actions" :key="action">{{ action }}</li>
        </ol>
      </section>

      <section class="demo-section">
        <h2 class="section-heading">Signposts to watch</h2>
        <div class="signpost-row">
          <span v-for="signpost in signposts" :key="signpost" class="signpost font-mono">
            {{ signpost }}
          </span>
        </div>
      </section>

      <section class="demo-cta">
        <h2 class="cta-heading">Run this on your own material</h2>
        <p class="cta-copy">
          The free demo is read-only. Choose a plan to upload your documents, build the
          ontology, run parallel simulations, and generate a live prediction report.
        </p>
        <div class="cta-actions">
          <button type="button" class="cta-primary" @click="openPlans">Choose a plan</button>
          <router-link to="/console" class="cta-secondary">Back to console</router-link>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import billingStore from '../store/billing'
import authStore from '../store/auth'

const summary = [
  {
    value: '62%',
    label: 'ACCEPT',
    copy: 'Annual and team accounts keep the plan; most cite workflow lock-in over price.'
  },
  {
    value: '24%',
    label: 'DOWNGRADE',
    copy: 'Monthly self-serve users move to the entry tier instead of leaving entirely.'
  },
  {
    value: '14%',
    label: 'CHURN',
    copy: 'Discount-acquired users leave within two renewal cycles, citing value doubt.'
  },
  {
    value: '−6.8 pts',
    label: 'NET RETENTION',
    copy: 'Projected by month four, concentrated in the smallest accounts.'
  }
]

const findings = [
  {
    title: 'Price framing beats price size',
    copy:
      'Agents shown the increase as a per-day cost with feature context accepted it at nearly twice the rate of agents shown the percentage alone.'
  },
  {
    title: 'Legacy discount cohorts are the real risk',
    copy:
      'Accounts acquired during the launch promotion treated the increase as a broken promise, independent of their usage level.'
  },
  {
    title: 'Team accounts negotiate, they do not leave',
    copy:
      'Admin buyers asked for annual terms or added seats rather than cancelling when the increase was paired with a clear migration window.'
  },
  {
    title: 'Support load spikes in week two',
    copy:
      'Billing questions clustered two weeks after the announcement, not on day one, and doubled the expected support volume.'
  }
]

const quotes = [
  {
    who: 'MONTHLY SELF-SERVE · LOW USAGE',
    text: 'I signed up at the intro price and use it twice a month. Twenty percent is a different product than the one I bought.'
  },
  {
    who: 'ANNUAL TEAM ADMIN · 14 SEATS',
    text: 'The increase is fine if the renewal date stays and I can add seats mid-term. I need a number before I brief finance.'
  },
  {
    who: 'POWER USER · DAILY USAGE',
    text: 'I care about the workflow, not the line item. Tell me what changed and I will keep paying.'
  }
]

const actions = [
  'Announce the change 45 days before renewal and hold existing annual contracts at the current rate.',
  'Move legacy discount cohorts to a loyalty price for one term instead of applying the full increase.',
  'Lead with per-day cost and a concrete feature delta in every customer-facing message.',
  'Staff support two weeks after the announcement, when billing questions cluster.'
]

const signposts = [
  'Support ticket mix',
  'Monthly-to-annual conversions',
  'Downgrade rate at renewal',
  'Referral volume from discount cohorts'
]

const openPlans = () => {
  if (!authStore.isAuthenticated.value) {
    authStore.openAuthModal('login', 'Sign in to choose a plan and run your own simulation.')
    return
  }
  billingStore.openPricing({ resume: false })
}
</script>

<style scoped>
.demo-container {
  min-height: 100vh;
  background: #ffffff;
  color: #000000;
  font-family: var(--font-sans, 'Space Grotesk', system-ui, sans-serif);
}

.demo-navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 32px;
  background: #000000;
  color: #ffffff;
}

.brand-link {
  text-decoration: none;
  color: #ffffff;
}

.brand-name {
  font-family: var(--font-display, 'Space Grotesk', sans-serif);
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.22em;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 18px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.74rem;
  text-decoration: none;
}

.nav-link:hover {
  color: #ffffff;
}

.nav-cta {
  padding: 8px 16px;
  border: 1px solid #ffffff;
  border-radius: 999px;
  background: transparent;
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
}

.nav-cta:hover {
  background: #ffffff;
  color: #000000;
}

.demo-main {
  max-width: 880px;
  margin: 0 auto;
  padding: 56px 24px 96px;
}

.demo-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
}

.sample-badge {
  padding: 4px 10px;
  border: 1px solid #000000;
  border-radius: 999px;
  font-family: var(--font-mono, monospace);
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.meta-text {
  color: #888888;
  font-family: var(--font-mono, monospace);
  font-size: 0.66rem;
  letter-spacing: 0.04em;
}

.demo-title {
  margin: 0 0 18px;
  font-size: clamp(1.9rem, 4vw, 2.7rem);
  font-weight: 600;
  line-height: 1.14;
  letter-spacing: -0.03em;
}

.demo-lead {
  margin: 0 0 36px;
  max-width: 680px;
  color: #555555;
  font-size: 0.98rem;
  line-height: 1.65;
}

.verdict {
  padding: 24px 26px;
  border-left: 3px solid #000000;
  background: #f7f7f7;
}

.verdict-label {
  margin-bottom: 10px;
  color: #888888;
  font-size: 0.64rem;
  letter-spacing: 0.12em;
}

.verdict-text {
  margin: 0;
  font-size: 1.02rem;
  line-height: 1.6;
}

.demo-section {
  margin-top: 48px;
}

.section-heading {
  margin: 0 0 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e5e5;
  font-size: 1.15rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
}

.summary-card {
  padding: 18px;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
}

.summary-value {
  font-size: 1.75rem;
  font-weight: 600;
  letter-spacing: -0.03em;
}

.summary-label {
  margin: 4px 0 10px;
  color: #888888;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
}

.summary-copy {
  margin: 0;
  color: #666666;
  font-size: 0.78rem;
  line-height: 1.5;
}

.finding-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.finding-list li {
  padding: 18px 0;
  border-bottom: 1px solid #eeeeee;
}

.finding-title {
  margin-bottom: 6px;
  font-size: 0.92rem;
  font-weight: 600;
}

.finding-copy {
  margin: 0;
  color: #666666;
  font-size: 0.84rem;
  line-height: 1.6;
}

.quote-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.quote-card {
  margin: 0;
  padding: 18px;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
}

.quote-text {
  margin: 0 0 12px;
  font-size: 0.84rem;
  line-height: 1.6;
}

.quote-who {
  color: #999999;
  font-size: 0.58rem;
  letter-spacing: 0.06em;
}

.action-list {
  margin: 0;
  padding-left: 20px;
  color: #333333;
  font-size: 0.86rem;
  line-height: 1.7;
}

.action-list li + li {
  margin-top: 8px;
}

.signpost-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.signpost {
  padding: 6px 11px;
  border: 1px solid #dddddd;
  border-radius: 999px;
  color: #555555;
  font-size: 0.64rem;
  letter-spacing: 0.03em;
}

.demo-cta {
  margin-top: 64px;
  padding: 32px;
  border-radius: 14px;
  background: #000000;
  color: #ffffff;
}

.cta-heading {
  margin: 0 0 10px;
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.cta-copy {
  margin: 0 0 22px;
  max-width: 560px;
  color: rgba(255, 255, 255, 0.66);
  font-size: 0.86rem;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.cta-primary {
  padding: 12px 22px;
  border: 1px solid #ffffff;
  border-radius: 999px;
  background: #ffffff;
  color: #000000;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.cta-secondary {
  display: inline-flex;
  align-items: center;
  padding: 12px 22px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 999px;
  color: #ffffff;
  font-size: 0.8rem;
  text-decoration: none;
}

.cta-secondary:hover {
  border-color: #ffffff;
}

@media (max-width: 560px) {
  .demo-navbar {
    padding: 0 18px;
  }

  .demo-main {
    padding: 36px 18px 72px;
  }

  .demo-cta {
    padding: 24px 20px;
  }
}
</style>
