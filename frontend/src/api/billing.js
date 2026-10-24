import service from './index'

export const billingApi = {
  getPlans() {
    return service.get('/api/billing/plans')
  },

  getMe() {
    return service.get('/api/billing/me')
  },

  subscribe(plan, interval) {
    return service.post('/api/billing/subscribe', { plan, interval })
  },

  verify(payload) {
    return service.post('/api/billing/verify', payload)
  },

  cancel() {
    return service.post('/api/billing/cancel')
  }
}

export default billingApi
