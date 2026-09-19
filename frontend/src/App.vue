<template>
  <AppHeader @login="showLogin = true" />

  <router-view />

  <Notification ref="notification" />
  
  <CookieConsent />
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import Notification from './components/Notification.vue'
import CookieConsent from './components/CookieConsent.vue'
import { useAuth } from './router/useAuth'

const showLogin = ref(false)
const router = useRouter()
const { authState, resetAuth } = useAuth()

watch(showLogin, val => {
  document.body.style.overflow = val ? 'hidden' : ''
})

const handleAuthError = () => {
  if (!authState.isAuthenticated) return
  resetAuth()
  router.push({ name: 'Login' })
}

onMounted(() => {
  window.addEventListener('auth-error', handleAuthError)
})

onUnmounted(() => {
  window.removeEventListener('auth-error', handleAuthError)
})
</script>

<style>
body {
  margin: 0;
  background: #f3f4f6;
  color: #111827;
  font-family: Inter, Arial, sans-serif;
}
</style>