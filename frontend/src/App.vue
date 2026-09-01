<template>
  <AppHeader @login="showLogin = true" />

  <router-view />

  <Notification ref="notification" />

  <div v-if="showLogin" class="fullscreen-overlay">
    <div class="auth-card">
      <h2>Вход в аккаунт</h2>
      <input placeholder="Email" />
      <input type="password" placeholder="Пароль" />
      <button class="primary-btn">Войти</button>
    </div>
  </div>
  
  <CookieConsent />
</template>

<script setup>
import { ref, watch } from 'vue'
import AppHeader from './components/AppHeader.vue'
import Notification from './components/Notification.vue'
import CookieConsent from './components/CookieConsent.vue'

const showLogin = ref(false)

watch(showLogin, val => {
  document.body.style.overflow = val ? 'hidden' : ''
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