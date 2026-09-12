import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../router/useAuth'

const Home = () => import('../views/Home.vue')
const About = () => import('../views/About.vue')
const Login = () => import('../views/Login.vue')
const Registration = () => import('../views/Registration.vue')
const Cabinet = () => import('../views/Cabinet.vue')

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registration', name: 'Registration', component: Registration },
  { path: '/cabinet', name: 'Cabinet', component: Cabinet, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true

  const { authState, fetchUser } = useAuth()

  if (!authState.isAuthenticated) {
    const ok = await fetchUser()
    if (!ok) return { name: 'Login', query: { redirect: to.fullPath } }
  }

  return true
})

export default router