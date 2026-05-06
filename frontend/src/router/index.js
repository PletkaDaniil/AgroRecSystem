import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('../views/Home.vue')
const About = () => import('../views/About.vue')
const Login = () => import('../views/Login.vue')
const Registration = () => import('../views/Registration.vue')

const routes = [
  { path: '/', name: 'Home', component: Home },

  { path: '/about', name: 'About', component: About },

  { path: '/login', name: 'Login', component: Login },

  { path: '/registration', name: 'Registration', component: Registration }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router