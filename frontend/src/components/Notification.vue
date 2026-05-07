<template>
  <Transition name="notification">
    <div v-if="visible" :class="['notification', type]">
      <div class="content">
        <div class="icon-wrap">
          <svg v-if="type === 'error'" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <p class="text">{{ message }}</p>
        <button @click="close" class="close-btn">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :class="type"></div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('error')

const show = ({ msg, t = 'error' }) => {
  message.value = msg
  type.value = t
  visible.value = true
  setTimeout(() => { visible.value = false }, 5000)
}

const close = () => { visible.value = false }

window.addEventListener('auth-error', e => {
  const detail = e.detail
  let msg = detail
  if (detail === 'Missing refresh token') {
    msg = 'Пожалуйста, войдите в личный кабинет'
  }
  show({ msg, t: 'error' })
})

defineExpose({ show })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600&family=JetBrains+Mono:wght@400&display=swap');

.notification {
  position: fixed;
  top: 80px;
  right: 32px;
  min-width: 300px;
  max-width: 400px;
  background: #ffffff;
  border: 1px solid #e8eaee;
  border-radius: 10px;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.07),
    0 10px 32px -4px rgba(0, 0, 0, 0.1);
  z-index: 10000;
  overflow: hidden;
  font-family: 'Manrope', sans-serif;
}

.notification.error { border-left: 3px solid #e85d4a; }
.notification.success { border-left: 3px solid #4a9e6b; }

.content {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 14px;
}

.icon-wrap {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error .icon-wrap {
  background: rgba(232, 93, 74, 0.08);
  color: #e85d4a;
}

.success .icon-wrap {
  background: rgba(74, 158, 107, 0.08);
  color: #4a9e6b;
}

.text {
  flex: 1;
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #1a1d23;
  line-height: 1.5;
}

.close-btn {
  flex-shrink: 0;
  background: none;
  border: none;
  padding: 4px;
  color: #c5c9d4;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s, background 0.15s;
}

.close-btn:hover {
  color: #6b7280;
  background: #f3f4f6;
}

.progress-bar {
  height: 2px;
  background: transparent;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  width: 100%;
  transform-origin: left center;
  animation: drain 5s linear forwards;
}

.progress-fill.error   { background: #e85d4a; }
.progress-fill.success { background: #4a9e6b; }

@keyframes drain {
  from { transform: scaleX(1); }
  to   { transform: scaleX(0); }
}

.notification-enter-active {
  animation: slideIn 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}
.notification-leave-active {
  animation: slideOut 0.2s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0)     scale(1);    }
}

@keyframes slideOut {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-6px); }
}
</style>