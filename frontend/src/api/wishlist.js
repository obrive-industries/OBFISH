import service from './index'

export const wishlistApi = {
  subscribe(email, source = 'landing_hero') {
    return service.post('/api/wishlist/subscribe', { email, source })
  },

  getSubscribers() {
    return service.get('/api/wishlist/subscribers')
  },

  exportCsv() {
    return service.get('/api/wishlist/export', { responseType: 'blob' })
  }
}

export default wishlistApi
