<template>
  <Teleport to="body">
    <div
      v-if="state.pricingOpen"
      class="pricing-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Choose a Brain plan"
      @click.self="close"
    >
      <div class="pricing-shell">
        <button class="pricing-close" type="button" aria-label="Close pricing" @click="close">×</button>

        <div class="pricing-top">
          <div class="billing-toggle" role="tablist" aria-label="Billing interval">
            <button
              type="button"
              role="tab"
              :aria-selected="state.interval === 'monthly'"
              class="toggle-option"
              :class="{ active: state.interval === 'monthly' }"
              @click="selectInterval('monthly')"
            >
              Monthly
            </button>
            <button
              type="button"
              role="tab"
              :aria-selected="state.interval === 'annual'"
              class="toggle-option"
              :class="{ active: state.interval === 'annual' }"
              @click="selectInterval('annual')"
            >
              Annually
              <span class="save-pill">SAVE 17%</span>
            </button>
          </div>

          <p class="pricing-subtitle">
            {{ state.interval === 'annual'
              ? 'Best for recurring forecasting and narrative analysis that runs all year.'
              : 'Best for live scenarios, short experiments, and validating fit on real material.' }}
          </p>
        </div>

        <div v-if="state.loading && !state.plans.length" class="pricing-grid" aria-hidden="true">
          <div v-for="n in 3" :key="n" class="price-card skeleton-card">
            <span class="skeleton line short"></span>
            <span class="skeleton line"></span>
            <span class="skeleton line tall"></span>
            <span class="skeleton line"></span>
            <span class="skeleton line"></span>
            <span class="skeleton line"></span>
          </div>
        </div>

        <div v-else class="pricing-grid">
          <article
            v-for="plan in state.plans"
            :key="plan.id"
            class="price-card"
            :class="{ 'price-card--featured': plan.id === 'pro' }"
          >
            <span v-if="plan.badge" class="plan-badge">{{ plan.badge }}</span>

            <h2 class="plan-name">{{ plan.name }}</h2>
            <p class="plan-description">{{ plan.description[state.interval] }}</p>

            <div class="plan-price-row">
              <span class="plan-currency">$</span>
              <span class="plan-amount">{{ billingStore.monthlyPrice(plan) }}</span>
              <span class="plan-period">/ MONTH</span>
            </div>
            <div v-if="state.interval === 'annual'" class="plan-strike">
              ${{ billingStore.strikePrice(plan) }} / MONTH
            </div>

            <div class="included-label">INCLUDED</div>
            <ul class="plan-features">
              <li v-for="feature in plan.features[state.interval]" :key="feature">
                <span class="feature-check" aria-hidden="true">
                  <svg viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="1.4" />
                    <path d="M6.2 10.3 8.7 12.8 13.8 7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
                <span>{{ feature }}</span>
              </li>
            </ul>

            <button
              type="button"
              class="choose-btn"
              :class="{ 'choose-btn--primary': plan.id === 'pro' }"
              :disabled="!state.configured || state.checkoutLoading"
              @click="choose(plan)"
            >
              {{ checkoutLabel(plan) }}
            </button>

            <p class="plan-footnote">{{ plan.footnote[state.interval] }}</p>
          </article>
        </div>

        <div v-if="state.error" class="pricing-error" role="alert">{{ state.error }}</div>
        <p v-else-if="!state.loading && !state.configured" class="pricing-note">
          Card checkout is not configured on this deployment yet. Please contact support to activate a plan.
        </p>

        <p class="pricing-legal">
          Prices in USD. Subscriptions renew automatically until cancelled. Cancel any time from your profile.
        </p>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import billingStore from '../store/billing'
import authStore from '../store/auth'

const state = billingStore.state

const close = () => billingStore.closePricing()

const selectInterval = (interval) => billingStore.setInterval(interval)

const choose = (plan) => {
  if (!state.configured || state.checkoutLoading) return
  if (!authStore.isAuthenticated.value) {
    authStore.openAuthModal('login', 'Please sign in to choose a subscription plan.')
    return
  }
  // Console listeners resume the interrupted Start Engine flow after purchase.
  billingStore.subscribe(plan.id)
}

const checkoutLabel = (plan) => {
  if (state.checkingOutPlan === plan.id) return 'Opening checkout...'
  return plan.cta
}

const onKeydown = (event) => {
  if (event.key === 'Escape' && state.pricingOpen) close()
}

watch(
  () => state.pricingOpen,
  (open) => {
    document.body.style.overflow = open ? 'hidden' : ''
  }
)

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  if (state.pricingOpen) billingStore.ensurePlans()
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.pricing-overlay {
  position: fixed;
  inset: 0;
  z-index: 5000;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  overflow-y: auto;
  padding: 40px 20px 60px;
  background:
    radial-gradient(60% 45% at 50% 0%, rgba(120, 92, 255, 0.16), transparent 70%),
    radial-gradient(45% 30% at 78% 12%, rgba(255, 166, 77, 0.1), transparent 70%),
    #050505;
  color: #f5f5f5;
  font-family: 'Inter', system-ui, sans-serif;
}

.pricing-shell {
  position: relative;
  width: 100%;
  max-width: 1160px;
  margin: auto;
}

.pricing-close {
  position: absolute;
  top: 0;
  right: 0;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  color: #b9b9b9;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.pricing-close:hover {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.35);
}

.pricing-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  margin-bottom: 38px;
}

.billing-toggle {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 4px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: #0d0d0d;
}

.toggle-option {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  height: 38px;
  padding: 0 24px;
  border: none;
  border-radius: 999px;
  background: transparent;
  color: #a3a3a3;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.toggle-option.active {
  background: #f7f7f7;
  color: #0a0a0a;
}

.save-pill {
  padding: 3px 7px;
  border-radius: 999px;
  background: rgba(130, 130, 130, 0.24);
  color: #c9c9c9;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.toggle-option.active .save-pill {
  background: rgba(0, 0, 0, 0.1);
  color: #3f3f3f;
}

.pricing-subtitle {
  margin: 0;
  color: #8b8b8b;
  font-size: 13px;
  text-align: center;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  align-items: stretch;
}

.price-card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 620px;
  padding: 30px 30px 28px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  background: linear-gradient(180deg, #171717 0%, #0d0d0d 100%);
  overflow: hidden;
}

.price-card::before {
  content: '';
  position: absolute;
  inset: -40% 10% auto;
  height: 240px;
  background: radial-gradient(closest-side, rgba(128, 96, 255, 0.16), transparent 75%);
  pointer-events: none;
}

.price-card--featured {
  border-color: rgba(255, 255, 255, 0.2);
  background: linear-gradient(180deg, #1b191d 0%, #0e0d10 100%);
}

.price-card--featured::before {
  background: radial-gradient(closest-side, rgba(145, 108, 255, 0.3), transparent 75%);
}

.price-card--featured::after {
  content: '';
  position: absolute;
  inset: auto 18% -30% auto;
  width: 220px;
  height: 220px;
  background: radial-gradient(closest-side, rgba(255, 170, 90, 0.12), transparent 72%);
  pointer-events: none;
}

.plan-badge {
  position: relative;
  align-self: flex-start;
  margin-bottom: 18px;
  padding: 5px 10px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  color: #bdbdbd;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.09em;
}

.plan-name {
  position: relative;
  margin: 0 0 12px;
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: 27px;
  font-weight: 600;
  letter-spacing: -0.03em;
  color: #ffffff;
}

.plan-description {
  position: relative;
  margin: 0 0 26px;
  min-height: 54px;
  color: #9a9a9a;
  font-size: 13px;
  line-height: 1.55;
}

.plan-price-row {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 2px;
}

.plan-currency {
  margin-top: 6px;
  font-size: 26px;
  font-weight: 600;
  color: #ffffff;
}

.plan-amount {
  font-size: 46px;
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #ffffff;
}

.plan-period {
  align-self: flex-end;
  margin-bottom: 7px;
  margin-left: 6px;
  color: #8c8c8c;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.plan-strike {
  margin-top: 8px;
  color: #6f6f6f;
  font-size: 13px;
  font-weight: 500;
  text-decoration: line-through;
}

.included-label {
  margin: 26px 0 14px;
  color: #8a8a8a;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.plan-features {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 13px;
  margin: 0 0 28px;
  padding: 0;
  list-style: none;
}

.plan-features li {
  display: flex;
  gap: 10px;
  color: #cfcfcf;
  font-size: 13px;
  line-height: 1.45;
}

.feature-check {
  flex: 0 0 17px;
  width: 17px;
  height: 17px;
  margin-top: 1px;
  color: #98a2b3;
}

.feature-check svg {
  width: 100%;
  height: 100%;
}

.choose-btn {
  position: relative;
  margin-top: auto;
  width: 100%;
  height: 44px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  background: transparent;
  color: #f4f4f4;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.choose-btn:hover:not(:disabled) {
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.04);
}

.choose-btn--primary {
  border-color: #ffffff;
  background: #ffffff;
  color: #0a0a0a;
}

.choose-btn--primary:hover:not(:disabled) {
  background: #e8e8e8;
}

.choose-btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.plan-footnote {
  position: relative;
  margin: 16px 0 0;
  min-height: 48px;
  color: #777777;
  font-size: 12px;
  line-height: 1.5;
}

.pricing-error {
  margin: 22px auto 0;
  max-width: 640px;
  padding: 12px 16px;
  border: 1px solid rgba(255, 99, 99, 0.35);
  border-radius: 10px;
  background: rgba(255, 70, 70, 0.08);
  color: #ffb4b4;
  font-size: 13px;
  text-align: center;
}

.pricing-note {
  margin: 20px auto 0;
  max-width: 680px;
  color: #a3a3a3;
  font-size: 12px;
  text-align: center;
}

.pricing-legal {
  margin: 26px auto 0;
  color: #5f5f5f;
  font-size: 11px;
  text-align: center;
}

.skeleton-card {
  gap: 14px;
}

.skeleton {
  display: block;
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(90deg, #1d1d1d, #262626, #1d1d1d);
  background-size: 200% 100%;
  animation: shimmer 1.4s linear infinite;
}

.skeleton.line {
  width: 100%;
}

.skeleton.line.short {
  width: 42%;
  height: 20px;
}

.skeleton.line.tall {
  width: 60%;
  height: 44px;
  margin: 12px 0;
}

@keyframes shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}

@media (max-width: 980px) {
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 520px;
    margin: 0 auto;
  }

  .price-card {
    min-height: 0;
  }

  .plan-description,
  .plan-footnote {
    min-height: 0;
  }

  .pricing-close {
    top: 34px;
    right: 22px;
  }
}

@media (max-width: 560px) {
  .pricing-overlay {
    padding: 26px 14px 40px;
  }

  .billing-toggle {
    transform: scale(0.92);
  }

  .pricing-close {
    position: fixed;
    top: 14px;
    right: 14px;
    background: #111111;
  }
}
</style>
