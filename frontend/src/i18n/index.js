import { createI18n } from 'vue-i18n'
import enMessages from '../../../locales/en.json'

const messages = {
  en: enMessages
}

const availableLocales = [
  { key: 'en', label: 'English' }
]

localStorage.setItem('locale', 'en')

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages
})

export { availableLocales }
export default i18n
