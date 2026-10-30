import { computed, reactive } from 'vue'
import router from '../router'
import billingApi from '../api/billing'
import { openRazorpayCheckout } from '../utils/razorpay'
import authStore from './auth'
import defaultPlans from '../data/defaultPlans.json'

const FREE_ENTITLEMENT = {
  plan: 'free',
  plan_name: 'Free demo',
  status: 'none',
  interval: null,
  is_admin: false,
  runs_used: 0,
  runs_limit: 1,
  max_rounds: 5,
  period_end: null,
  renews_at: null,
  cancel_at_period_end: false,
  can_start: true,
  unlimited: false,
  configured: false
}

const state = reactive({
  catalog: null,
  plans: defaultPlans,
  entitlement: { ...FREE_ENTITLEMENT },
  subscription: null,
  loading: false,
  loaded: false,
  error: '',
  interval: 'monthly',
  pricingOpen: false,
  checkoutLoading: false,
  checkingOutPlan: null,
  configured: false,
  pendingResume: false,
  purchaseVersion: 0
})

let loadPromise = null
let refreshPromise = null

const money = (cents) => {
  const value = Number(cents || 0) / 100
  return Number.isInteger(value) ? String(value) : value.toFixed(2)
}

export const billingStore = {
  state,

  entitlement: computed(() => state.entitlement),
  plans: computed(() => state.plans),
  isPaid: computed(() => ['starter', 'pro', 'premium', 'admin'].includes(state.entitlement.plan)),
  canStart: computed(() => Boolean(state.entitlement.unlimited || state.entitlement.can_start)),

  money,
  monthlyPrice(plan) {
    return state.interval === 'annual'
      ? money(plan.monthly_equivalent_cents)
      : money(plan.monthly_cents)
  },
  strikePrice(plan) {
    return money(plan.annual_strike_cents || plan.monthly_cents)
  },

  async ensurePlans() {
    if (state.loaded && state.plans?.length) return state.plans
    if (loadPromise) return loadPromise
    state.loading = true
    state.error = ''
    loadPromise = billingApi
      .getPlans()
      .then((res) => {
        if (res.data?.plans && res.data.plans.length) {
          state.catalog = res.data
          state.plans = res.data.plans
        }
        state.configured = Boolean(res.data?.configured)
        state.loaded = true
        return state.plans
      })
      .catch((err) => {
        // Fall back gracefully to default catalog so pricing is always present
        if (!state.plans || !state.plans.length) {
          state.plans = defaultPlans
        }
        state.loaded = true
        return state.plans
      })
      .finally(() => {
        state.loading = false
        loadPromise = null
      })
    return loadPromise
  },

  async refresh() {
    if (!authStore.isAuthenticated.value) {
      state.entitlement = { ...FREE_ENTITLEMENT }
      state.subscription = null
      state.error = ''
      return state.entitlement
    }
    if (refreshPromise) return refreshPromise
    state.error = ''
    refreshPromise = (async () => {
      try {
        const res = await billingApi.getMe()
        state.entitlement = { ...FREE_ENTITLEMENT, ...(res.entitlement || {}) }
        state.subscription = res.subscription || null
        state.configured = Boolean(res.entitlement?.configured)
        state.error = ''
      } catch (err) {
        console.warn('Billing refresh warning:', err?.message)
      } finally {
        refreshPromise = null
      }
      return state.entitlement
    })()
    return refreshPromise
  },

  openPricing({ resume = false } = {}) {
    state.error = ''
    state.pricingOpen = false
    state.pendingResume = resume
    this.ensurePlans()
    if (authStore.isAuthenticated.value) this.refresh()
    if (router && router.currentRoute.value.path !== '/pricing') {
      router.push('/pricing')
    }
  },

  closePricing() {
    state.pricingOpen = false
    state.error = ''
    state.pendingResume = false
    state.checkingOutPlan = null
  },

  setInterval(interval) {
    state.interval = interval === 'annual' ? 'annual' : 'monthly'
  },

  async subscribe(planId) {
    if (state.checkoutLoading) return false
    state.checkoutLoading = true
    state.checkingOutPlan = planId
    state.error = ''

    try {
      const session = await billingApi.subscribe(planId, state.interval)
      await openRazorpayCheckout({
        keyId: session.key_id,
        subscriptionId: session.subscription_id,
        prefill: session.prefill,
        onSuccess: async (response) => {
          await billingApi.verify({
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_subscription_id: response.razorpay_subscription_id,
            razorpay_signature: response.razorpay_signature
          })
          await this.refresh()
          state.purchaseVersion += 1
          state.pricingOpen = false
          state.pendingResume = false
          if (router && router.currentRoute.value.path === '/pricing') {
            router.push('/console')
          }
        },
        onFailure: (err) => {
          state.error = err.message
        }
      })
      return this.isPaid.value
    } catch (err) {
      state.error = err.message || 'Could not start checkout.'
      return false
    } finally {
      state.checkoutLoading = false
      state.checkingOutPlan = null
    }
  },

  async cancel() {
    state.error = ''
    try {
      await billingApi.cancel()
      await this.refresh()
      return true
    } catch (err) {
      state.error = err.message || 'Could not cancel the subscription.'
      return false
    }
  }
}

export default billingStore
