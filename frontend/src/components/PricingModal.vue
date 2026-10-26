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
              <span class="save-pill">SAVE UP TO 50%</span>
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
          Prices in USD (processed in equivalent INR via Razorpay). Subscriptions renew automatically until cancelled. Cancel any time from your profile.
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
    radial-gradient(60% 45% at 50% 0%, rgba(255, 255, 255, 0.45), transparent 70%),
    radial-gradient(45% 30% at 85% 15%, rgba(6, 65, 57, 0.08), transparent 70%),
    #A2F1DF;
  color: #073933;
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
  width: 38px;
  height: 38px;
  border: 1px solid rgba(7, 57, 51, 0.2);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.65);
  color: #073933;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.06);
}

.pricing-close:hover {
  background: #ffffff;
  border-color: #073933;
  color: #000000;
  transform: scale(1.05);
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
  gap: 3px;
  padding: 4px;
  border-radius: 999px;
  border: 1px solid rgba(7, 57, 51, 0.18);
  background: rgba(255, 255, 255, 0.55);
  box-shadow: 0 4px 15px rgba(7, 57, 51, 0.05);
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
  color: #163830;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-option.active {
  background: #073933;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(7, 57, 51, 0.2);
}

.save-pill {
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(7, 57, 51, 0.12);
  color: #073933;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.toggle-option.active .save-pill {
  background: rgba(162, 241, 223, 0.35);
  color: #A2F1DF;
}

.pricing-subtitle {
  margin: 0;
  color: #163830;
  font-size: 14px;
  font-weight: 500;
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
  padding: 32px 30px 28px;
  border: 1px solid rgba(7, 57, 51, 0.14);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 10px 30px rgba(7, 57, 51, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.price-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 36px rgba(7, 57, 51, 0.1);
}

.price-card--featured {
  border: 2px solid #073933;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 16px 42px rgba(7, 57, 51, 0.14);
}

.plan-badge {
  position: relative;
  align-self: flex-start;
  margin-bottom: 18px;
  padding: 5px 12px;
  border: 1px solid rgba(7, 57, 51, 0.25);
  border-radius: 999px;
  background: #A2F1DF;
  color: #073933;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.09em;
}

.plan-name {
  position: relative;
  margin: 0 0 12px;
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #073933;
}

.plan-description {
  position: relative;
  margin: 0 0 24px;
  min-height: 54px;
  color: #1d483f;
  font-size: 13.5px;
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
  font-weight: 700;
  color: #073933;
}

.plan-amount {
  font-size: 48px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #073933;
}

.plan-period {
  align-self: flex-end;
  margin-bottom: 7px;
  margin-left: 6px;
  color: #2d554c;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.plan-strike {
  margin-top: 8px;
  color: #65857e;
  font-size: 14px;
  font-weight: 600;
  text-decoration: line-through;
}

.included-label {
  margin: 24px 0 14px;
  color: #073933;
  font-size: 10px;
  font-weight: 800;
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
  color: #163830;
  font-size: 13px;
  line-height: 1.45;
}

.feature-check {
  flex: 0 0 17px;
  width: 17px;
  height: 17px;
  margin-top: 1px;
  color: #073933;
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
  border: 1px solid #073933;
  border-radius: 999px;
  background: #ffffff;
  color: #073933;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.choose-btn:hover:not(:disabled) {
  background: #073933;
  color: #ffffff;
}

.choose-btn--primary {
  border-color: #073933;
  background: #073933;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(7, 57, 51, 0.25);
}

.choose-btn--primary:hover:not(:disabled) {
  background: #032420;
  border-color: #032420;
  transform: translateY(-1px);
}

.choose-btn:disabled {
  cursor: not-allowed;
  opacity: 0.45;
  border-color: rgba(7, 57, 51, 0.2);
  background: rgba(7, 57, 51, 0.05);
  color: #163830;
}

.plan-footnote {
  position: relative;
  margin: 16px 0 0;
  min-height: 48px;
  color: #3b6158;
  font-size: 12px;
  line-height: 1.5;
}

.pricing-error {
  margin: 22px auto 0;
  max-width: 640px;
  padding: 12px 16px;
  border: 1px solid rgba(220, 38, 38, 0.35);
  border-radius: 10px;
  background: rgba(220, 38, 38, 0.08);
  color: #b91c1c;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
}

.pricing-note {
  margin: 20px auto 0;
  max-width: 680px;
  color: #1d483f;
  font-size: 12.5px;
  text-align: center;
  font-weight: 500;
}

.pricing-legal {
  margin: 26px auto 0;
  color: #2d554c;
  font-size: 11.5px;
  text-align: center;
}

.skeleton-card {
  gap: 14px;
}

.skeleton {
  display: block;
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(7, 57, 51, 0.06), rgba(7, 57, 51, 0.14), rgba(7, 57, 51, 0.06));
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
    background: #ffffff;
  }
}
</style>
