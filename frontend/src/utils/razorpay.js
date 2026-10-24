const SCRIPT_URL = 'https://checkout.razorpay.com/v1/checkout.js'

let scriptPromise = null

function loadScript() {
  if (window.Razorpay) return Promise.resolve(window.Razorpay)
  if (scriptPromise) return scriptPromise

  scriptPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = SCRIPT_URL
    script.async = true
    script.onload = () => {
      if (window.Razorpay) resolve(window.Razorpay)
      else reject(new Error('Razorpay Checkout did not load.'))
    }
    script.onerror = () => reject(new Error('Could not load Razorpay Checkout. Check your connection.'))
    document.body.appendChild(script)
  })

  scriptPromise.catch(() => {
    scriptPromise = null
  })
  return scriptPromise
}

export async function openRazorpayCheckout({ keyId, subscriptionId, prefill, onSuccess, onFailure }) {
  const Razorpay = await loadScript()

  return new Promise((resolve, reject) => {
    const checkout = new Razorpay({
      key: keyId,
      subscription_id: subscriptionId,
      name: 'Brain',
      description: 'Simulation plan',
      image: '/obrive-logo.svg',
      prefill: prefill || {},
      theme: { color: '#ffffff' },
      handler: (response) => {
        Promise.resolve(onSuccess?.(response)).then(resolve).catch(reject)
      },
      modal: {
        ondismiss: () => {
          onFailure?.(new Error('Checkout closed before payment was completed.'))
          resolve(null)
        }
      }
    })

    checkout.on('payment.failed', (response) => {
      const message = response?.error?.description || 'Payment failed. Please try again.'
      onFailure?.(new Error(message))
      reject(new Error(message))
    })

    checkout.open()
  })
}
