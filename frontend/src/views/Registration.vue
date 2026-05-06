<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Регистрация</h2>
        <p class="auth-subtitle">Создайте аккаунт для начала работы</p>
      </div>

      <transition name="error-slide">
        <div v-if="errorMessage" class="error-notification">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="2"/>
            <path d="M10 6v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          {{ errorMessage }}
        </div>
      </transition>

      <form @submit.prevent="handleRegistration">
        <div class="input-group">
          <label for="username">Имя пользователя</label>
          <input 
            id="username"
            v-model="username" 
            type="text" 
            placeholder="Введите имя пользователя"
            :class="{ 'input-error': highlightedFields.username }"
          />
          <div class="hint-text">Минимум 5 символов</div>
        </div>

        <div class="input-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="text" 
            placeholder="Введите email"
            :class="{ 'input-error': highlightedFields.email }"
          />
        </div>

        <div class="input-group">
          <label for="password">Пароль</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Придумайте пароль"
            :class="{ 'input-error': highlightedFields.password }"
          />
          <div class="hint-text">Минимум 8 символов</div>
        </div>

        <div class="input-group">
          <label for="confirmPassword">Подтвердите пароль</label>
          <input 
            id="confirmPassword"
            v-model="confirmPassword" 
            type="password" 
            placeholder="Повторите пароль"
            :class="{ 'input-error': highlightedFields.confirmPassword }"
          />
        </div>

        <button type="submit" class="primary-btn">Зарегистрироваться</button>
      </form>

      <div class="divider">или</div>

      <router-link to="/login" class="secondary-btn">
        Уже есть аккаунт? Войти
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth.api'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')

const highlightedFields = reactive({
  username: false,
  email: false,
  password: false,
  confirmPassword: false
})

const showError = (message, fields = []) => {
  errorMessage.value = message

  Object.keys(highlightedFields).forEach(key => {
    highlightedFields[key] = false
  })

  fields.forEach(field => {
    if (highlightedFields.hasOwnProperty(field)) {
      highlightedFields[field] = true
    }
  })

  setTimeout(() => {
    errorMessage.value = ''
    Object.keys(highlightedFields).forEach(key => {
      highlightedFields[key] = false
    })
  }, 3000)
}

const handleRegistration = async () => {
  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    const emptyFields = []
    if (!username.value) emptyFields.push('username')
    if (!email.value) emptyFields.push('email')
    if (!password.value) emptyFields.push('password')
    if (!confirmPassword.value) emptyFields.push('confirmPassword')

    showError('Пожалуйста, заполните все поля', emptyFields)
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    showError('Пожалуйста, введите корректный email адрес', ['email'])
    return
  }

  if (username.value.length < 5) {
    showError('Имя пользователя должно содержать минимум 5 символов', ['username'])
    return
  }

  if (password.value.length < 8) {
    showError('Пароль должен содержать минимум 8 символов', ['password'])
    return
  }

  if (password.value !== confirmPassword.value) {
    showError('Пароли не совпадают', ['password', 'confirmPassword'])
    return
  }

  try {
    await authApi.registration({
      username: username.value,
      email: email.value,
      password: password.value,
    })

    router.push('/')

  } catch (err) {
    const msg =
      err.response?.data?.detail ||
      'Ошибка регистрации. Попробуйте позже'

    showError(msg)
  }
}
</script>

<style scoped>
.auth-page {
  max-width: 520px;
  margin: 60px auto;
  padding: 0 20px;
}

.auth-card {
  background: white;
  padding: 36px;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.1);
  max-width: 420px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 4px;
}

.auth-header h2 {
  font-size: 26px;
  margin-bottom: 6px;
  color: #111827;
  font-weight: 700;
}

.auth-subtitle {
  color: #6b7280;
  font-size: 14px;
}

/* Красивое уведомление об ошибке */
.error-notification {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
}

.error-notification svg {
  flex-shrink: 0;
}

.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.3s ease;
}

.error-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.auth-card input[type="text"],
.auth-card input[type="email"],
.auth-card input[type="password"] {
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  font-size: 15px;
  transition: all 0.2s;
}

.auth-card input[type="text"]:focus,
.auth-card input[type="email"]:focus,
.auth-card input[type="password"]:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.auth-card input.input-error {
  border-color: #dc2626;
  background: #fef2f2;
}

.hint-text {
  font-size: 12px;
  color: #9ca3af;
  margin-top: -2px;
}

.primary-btn {
  background: linear-gradient(135deg, #6366f1, #3b82f6);
  color: white;
  border: none;
  padding: 12px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.2s;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

.primary-btn:active {
  transform: translateY(0);
}

.secondary-btn {
  text-decoration: none;
  text-align: center;
  display: block;
  border: 2px solid #6366f1;
  color: #6366f1;
  padding: 12px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background: #6366f1;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
}

.divider {
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
  position: relative;
  margin: 4px 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #e5e7eb;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 28px 20px;
  }
  
  .auth-header h2 {
    font-size: 24px;
  }
}
</style>