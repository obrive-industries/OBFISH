import { createRouter, createWebHistory } from 'vue-router'
import authStore from '../store/auth'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/LandingView.vue')
  },
  {
    path: '/console',
    name: 'Console',
    component: () => import('../views/ConsoleView.vue')
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: () => import('../views/MainView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: () => import('../views/SimulationView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: () => import('../views/SimulationRunView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: () => import('../views/ReportView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: () => import('../views/InteractionView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/main',
    name: 'Main',
    redirect: '/console'
  },
  {
    path: '/engine',
    name: 'Engine',
    redirect: '/console'
  },
  {
    path: '/simulation',
    redirect: '/console'
  },
  {
    path: '/report',
    redirect: '/console'
  },
  {
    path: '/interaction',
    redirect: '/console'
  },
  {
    path: '/verify-email',
    name: 'VerifyEmail',
    component: () => import('../views/VerifyEmailView.vue')
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('../views/ResetPasswordView.vue')
  },
  {
    path: '/home',
    redirect: '/'
  },
  {
    path: '/app',
    redirect: '/console'
  },
  {
    path: '/dashboard',
    redirect: '/console'
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0, behavior: 'smooth' }
  }
})

// Route guard: protect internal engine views and require authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta?.requiresAuth)
  if (requiresAuth) {
    const token = localStorage.getItem('brain_access_token') || localStorage.getItem('obmind_access_token') || localStorage.getItem('token')
    const user = localStorage.getItem('brain_user') || localStorage.getItem('obmind_user') || localStorage.getItem('user')
    if (!token || !user) {
      try {
        authStore.openAuthModal('login', 'Please sign in to access this feature.')
      } catch (e) {
        // ignore
      }
      return next({ path: '/', query: { auth: 'login', redirect: to.fullPath } })
    }
  }
  next()
})

export default router
